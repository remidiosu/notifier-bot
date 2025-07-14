import aiohttp
from aiohttp import ClientTimeout


async def check_site(url: str) -> bool:
    try:
        timeout = ClientTimeout(total=5)
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=timeout) as resp:
                return resp.status == 200
    except Exception:
        return False
