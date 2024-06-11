import asyncio
import logging
import sys
import io

from pathlib import Path


from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, Voice
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile


from config import Settings
from ai_recognition import VocalAssistance

settings = Settings()

dp = Dispatcher()

bot = Bot(token=settings.bot_token)


voice_helper = VocalAssistance(settings.open_ai_token)

async def save_voice_as_ogg(bot: Bot, voice: Voice) -> str:
    voice_file_info = await bot.get_file(voice.file_id)
    voice_ogg_path = Path("files", f"{voice.file_unique_id}.ogg")
    path = await bot.download_file(voice_file_info.file_path, voice_ogg_path)
    
    print(voice_ogg_path)

    return voice_ogg_path


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("This is a bot that receives voice message and answer for it in voice message")

@dp.message(F.voice)
async def answer_audio(message: Message) -> None:
    voice_path = await save_voice_as_ogg(bot, message.voice)
    voice_text = await voice_helper.speech_to_text(voice_path)
    text_answer = await voice_helper.answer_question(voice_text)
    
    await voice_helper.text_to_speech(text_answer)

    voice_file = Path("files", "speech.ogg")
    voice = FSInputFile(voice_file)


    await message.answer_voice(voice)

@dp.message()
async def answer_default(message: Message) -> None:
    await message.answer("Send voice message")

async def main():

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())