import asyncio
import logging
import sys
from pathlib import Path

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, Voice
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile


from config import Settings

settings = Settings()

dp = Dispatcher()

voice = FSInputFile(Path("files", "sample.ogg"))

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("This is a bot that receives voice message and answer for it in voice message")

@dp.message(F.voice)
async def answer_audio(message: Message) -> None:
    await message.answer_voice(voice=voice)

@dp.message()
async def answer_default(message: Message) -> None:
    await message.answer("Send voice message")

async def main():
    bot = Bot(token=settings.bot_token)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())