from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message

from tgbot.config import load_config
from tgbot.db.sqllite import Database
from tgbot.filters.admin import AdminFilter

import asyncio
import aioschedule
from datetime import datetime, timedelta

user_router = Router()
db = Database()
config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode="HTML")

async def job(user_id):
    admin_ids=298933005
    await asyncio.create_task(bot.send_message( user_id, "da"))


@user_router.message(CommandStart())
async def user_start(message: Message):
    if db.exist_user(telegram_id=message.from_user.id):
        await message.answer("Привіт, прекрасна 💌")
    else:
        db.add_user(name=message.from_user.full_name, telegram_id=message.from_user.id)
        await message.answer("Ща зарегаю тебе))")
        aioschedule

