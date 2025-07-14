import logging
from aiogram import Bot, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import asyncio

from bot.db import UserURL
from bot.checker import check_site

CHECK_INTERVAL = 10
router = Router()


@router.message(CommandStart())
async def start_cmd(message: Message):
    say_hi = (
        "Этот бот отслеживает доступность ваших сайтов и сообщает о сбоях.\n\n"
        "Команды:\n"
        "/add <URL> – добавить сайт для мониторинга\n"
        "/delete <URL> – удалить сайт из мониторинга\n"
        "/list – показать все добавленные сайты"
    )
    await message.answer(say_hi)


@router.message(Command("add"))
async def add_cmd(message: Message):
    user_id = message.from_user.id
    parts = message.text.split(maxsplit=1)

    if len(parts) != 2:
        return await message.answer(
            "Введите URL после команды: /add https://example.com"
        )

    url = parts[1].strip()
    if not url.startswith("http"):
        return await message.answer("Некорректный URL. Добавьте http:// или https://")

    urls = await UserURL.filter(user_id=user_id).values_list("url", flat=True)
    if url in urls:
        return await message.answer("Этот сайт уже добавлен.")
    if len(urls) >= 5:
        return await message.answer("Можно добавить не более 5 сайтов.")

    await UserURL.create(user_id=user_id, url=url)
    await message.answer(f"✅ {url} добавлен в список для мониторинга.")
    logging.info(f"/add command used by user {user_id}: {message.text}")


@router.message(Command("delete"))
async def delete_cmd(message: Message):
    user_id = message.from_user.id
    parts = message.text.split(maxsplit=1)

    if len(parts) != 2:
        return await message.answer(
            "Введите URL после команды: /delete https://example.com"
        )

    url = parts[1].strip()
    urls = await UserURL.filter(user_id=user_id).values_list("url", flat=True)
    if url not in urls:
        return await message.answer("Этот сайт не найден в вашем списке.")

    await UserURL.filter(user_id=user_id, url=url).delete()
    await message.answer(f"❌ {url} удалён из списка.")
    logging.info(f"/delete command used by user {user_id}: {message.text}")


@router.message(Command("list"))
async def list_cmd(message: Message):
    user_id = message.from_user.id
    urls = await UserURL.filter(user_id=user_id).values_list("url", flat=True)

    if not urls:
        return await message.answer(
            "У вас нет сайтов в списке мониторинга. Используйте /add __ "
        )

    formatted = "\n".join(f"- {url}" for url in urls)
    await message.answer(f"Ваши сайты:\n{formatted}")


async def start_periodic_check(bot: Bot):
    while True:
        # Get all user-URL pairs
        entries = await UserURL.all().values("user_id", "url")
        for entry in entries:
            user_id = entry["user_id"]
            url = entry["url"]
            ok = await check_site(url)
            if not ok:
                await bot.send_message(user_id, f"⚠️ {url} недоступен!")
                logging.warning(f"Site DOWN: {url} for user {user_id}")
        await asyncio.sleep(CHECK_INTERVAL)
