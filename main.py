import asyncio
import logging
import sys
from os import getenv
import openai
from dotenv import load_dotenv


from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message


load_dotenv()


TOKEN = getenv('BOT_TOKEN')
openai.api_key = getenv('OPENAI_API_KEY')


dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!\n"
                          "Bu 234GPT, savolingizni kiriting👇")


@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": message.text}
            ]
        )
        reply = response.choices[0].message.content
        await message.answer(reply)
    except openai.error.RateLimitError:
        await message.answer("Juda ko'p so'rovlar. Iltimos, keyinroq sinab ko'ring.")
    except Exception as e:
        await message.answer(f"Xatolik yuz berdi. Iltimos qayta urunib ko'ring.{{e}}")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
