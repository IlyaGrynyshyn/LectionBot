import asyncio
import re
from datetime import datetime, timedelta

from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from tgbot.config import load_config
from tgbot.db.sqllite import Database
from tgbot.misc.states import RegisterUser
from tgbot.services.broadcaster import send_message

scheduler = AsyncIOScheduler(timezone="Europe/Kyiv")

user_router = Router()
db = Database()
config = load_config(".env")
bot = Bot(token=config.tg_bot.token)


async def send_message_in_1_min(bot: Bot, user_id):
    await bot.send_message(user_id, "Message in 1 min")


async def send_message_in_5_min(bot: Bot, user_id):
    await bot.send_message(user_id, "I will send this message the next day")


@user_router.message(CommandStart())
async def user_start(message: Message, state: FSMContext):
    if db.exist_user(telegram_id=message.from_user.id):
        await message.answer("Привіт, прекрасна 💌")
        scheduler.add_job(
            send_message_in_1_min,
            trigger="date",
            run_date=datetime.now() + timedelta(seconds=30),
            kwargs={"bot": bot, "user_id": message.from_user.id},
        )
        scheduler.add_job(
            send_message_in_5_min,
            trigger="date",
            run_date=datetime.now() + timedelta(minutes=5),
            kwargs={"bot": bot, "user_id": message.from_user.id},
        )
        if scheduler.state == 0:
            scheduler.start()
        await state.clear()

    else:
        await state.set_state(RegisterUser.registration_email)
        await message.answer("✉️ Надішли мені свою пошту")


@user_router.message(RegisterUser.registration_email)
async def register_phone(message: Message, state: FSMContext):
    email = message.text
    if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
        db.add_user(
            name=message.from_user.full_name,
            username=message.from_user.username,
            telegram_id=message.from_user.id,
            email=email,
        )
        message_text = """
        🤗 Дякуємо, що залишила свою пошту
        """
        await message.answer(text=message_text)
        await asyncio.sleep(2)
        await send_message(
            bot, message.from_user.id, "I will send this message in 1 minute"
        )
        await state.clear()
    else:
        await message.answer(
            "❗️Будь ласка, введи свою email адресу в форматі example@ex.com"
        )
