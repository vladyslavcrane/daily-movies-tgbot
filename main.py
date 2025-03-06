import argparse
import pdb
import asyncio
import logging
from logging.handlers import RotatingFileHandler
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.handlers import router, set_default_commands
from app.jobs import post_movie
from app.config import config
from app.scheduler import setup_scheduler
from app.db import init_mongodb

# Bot token can be obtained via https://t.me/BotFather
TOKEN = getenv("TG_BOT_TOKEN")

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()
dp.include_router(router)


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    jobs = [
        (post_movie, config.CRON_SCHEDULE["POST_MOVIE"]),
    ]

    setup_scheduler(bot, jobs)

    ########## Mongo
    await init_mongodb()

    await set_default_commands(bot)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mock-data", action="store_true", help="Use mock data for testing"
    )

    args = parser.parse_args()
    config.mock_data = args.mock_data

    log_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler = RotatingFileHandler(
        config.LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=5
    )
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.INFO)

    logging.basicConfig(level=logging.INFO, handlers=[file_handler, console_handler])
    asyncio.run(main())
