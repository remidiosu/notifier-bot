import logging
import os

def setup_logger():
    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("logs/bot.log", mode='a', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
