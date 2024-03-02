import asyncio
import re
from datetime import datetime, timedelta

from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from apscheduler.schedulers import SchedulerAlreadyRunningError
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from tgbot.config import load_config, Config
from tgbot.db.sqllite import Database
from tgbot.misc.states import RegisterUser

user_router = Router()
db = Database()
config = load_config(".env")
bot = Bot(token=config.tg_bot.token)


async def send_message_in_5_sec(bot: Bot, user_id):
    text = """Спрацюємось з тобою💆🏼‍♀️♥️. За твій виділений час - тримай авторську систему від Альони по фокусуванню та самодисципліні \n\nhttps://alennamaer.notion.site/SELF-DISCIPLINE-alennamaer-4aad21cbbf39480189ab16bec7f48e46?pvs=4"""
    await bot.send_message(user_id, text=text)


async def send_message_in_20_sec(bot: Bot, user_id):
    text = """
Привіт, привіт✨ - Лекція 1 «ЯК НОВАЧКУ ВИСТРОЇТИ СИСТЕМУ РОСТУ»

🪄Ціль лекції - допомогти тобі отримати чітку структуру та ясність в роботі з клієнтом, щоб ти могла планувати кожен етап роботи з легкістю, жити життя та екологічно насолоджуватися кожною сферою

Просто тицяй і переходь до перегляду [не забудь про зручний одяг, кавочку/какао і записник - нотувати прийдеться багато🥹] https://youtu.be/3-nKftP7Fm4?si=zWQPCv0JeTm4Cint

https://alennamaer.notion.site/1-0b9fddda26904b75a10bb153e7ca1462?pvs=4

*і не забувай відмічати в сторіс, якщо ловиш інсайти - нам буде приємно♥️

А посилання на те, щоб приєднатися до нашої академії зараз ЗА НАЙНИЖЧИМИ ЦІНАМИ вже тут 👉🏼 https://womensfreelanceclub.site/

А всі питання пиши сюди у наш відділі турботи https://t.me/smmandpsychology
    """
    await bot.send_message(user_id, text=text)


async def send_message_in_1_day(bot: Bot, user_id):
    text = """
    Лекція 2 - Ефективні сторітелінги💌
     https://www.notion.so/alennamaer/fa4d31ed002640c78f52380e1bb71769?pvs=4

https://youtu.be/A2YY6qLEJDY?si=QRD5P5sdEqzxcKN5

Посилання на те щоб потрапити в академію https://womensfreelanceclub.site/
    """
    await bot.send_message(user_id, text=text)


@user_router.message(CommandStart())
async def user_start(message: Message, state: FSMContext):
    if db.exist_user(telegram_id=message.from_user.id):
        await message.answer("Привіт, я особистий бот alennamaer 💌")
        await state.clear()
    else:
        await state.set_state(RegisterUser.registration_email)
        await message.answer(
            "Привіт, я особистий бот alennamaer 💌\nДля початку поділись своєю поштою, щоб я точно більше не загубив тебе"
        )


@user_router.message(RegisterUser.registration_email)
async def register_phone(
    message: Message, state: FSMContext, apscheduler: AsyncIOScheduler
):
    email = message.text
    if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
        db.add_user(
            name=message.from_user.full_name,
            username=message.from_user.username,
            telegram_id=message.from_user.id,
            email=email,
            date=datetime.now()
        )
        await asyncio.sleep(2)
        await state.clear()
        await send_message_in_5_sec(bot, message.from_user.id)
        apscheduler.add_job(
            send_message_in_20_sec,
            trigger="date",
            run_date=datetime.now() + timedelta(seconds=10),
            kwargs={"bot": bot, "user_id": message.from_user.id},
        )
        apscheduler.add_job(
            send_message_in_1_day,
            trigger="date",
            run_date=datetime.now() + timedelta(hours=24),
            kwargs={"bot": bot, "user_id": message.from_user.id},
        )
        try:
            if apscheduler.state == 0:
                apscheduler.start()
        except SchedulerAlreadyRunningError as e:
            print(e)
    else:
        await message.answer(
            "❗️Будь ласка, введи свою email адресу в форматі example@ex.com"
        )
