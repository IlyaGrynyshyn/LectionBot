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


async def send_message_in_1_min(bot: Bot, user_id):
    text = """Спрацюємось з тобою💆🏼‍♀️♥️. За твій виділений час - тримай безкоштовний урок і посібник по REELS. Кажуть, тобі важко створювати REELS і взагалі зрозуміти алгоритми інсти - тому в цьому уроці ти отримаєш стратегію і НАВІТЬ ТАБЛИЦЮ ДЛЯ РЕГУЛЯРНОСТІ\nhttps://shorturl.at/irJV3 \n\nВ цьому уроці Альона ділиться своїми кроками та досвідом, який актуальний зараз для блогів та бізнесів"""
    await bot.send_message(user_id, text=text)


async def send_message_in_2_min(bot: Bot, user_id):
    text = """
     ІНТЕНСИВ почнеться завтра, тому до цього часу ти можеш засвоїти попередній урок і готуватися🫂..
    """
    await bot.send_message(user_id, text=text)


async def send_message_in_5_min(bot: Bot, user_id):
    text = """
     1. Привіт, привіт✨ - Лекція 1 «ЯК НОВАЧКУ ВИСТРОЇТИ СИСТЕМУ РОСТУ»

🪄Ціль лекції - допомогти тобі отримати чітку структуру та ясність в роботі з клієнтом, щоб ти могла планувати кожен етап роботи з легкістю, жити життя та екологічно насолоджуватися кожною сферою

Просто тицяй і переходь до перегляду [не забудь про зручний одяг, кавочку/какао і записник - нотувати прийдеться багато🥹]

*і не забувай відмічати в сторіс, якщо ловиш інсайти - нам буде приємно♥️

А посилання на те, щоб приєднатися до нашої академії зараз ЗА НАЙНИЖЧИМИ ЦІНАМИ вже тут 👉🏼 https://womensfreelanceclub.site/

А всі питання пиши сюди у наш відділі турботи https://t.me/smmandpsychology
    """
    await bot.send_message(user_id, text=text)


@user_router.message(CommandStart())
async def user_start(message: Message, state: FSMContext):
    if db.exist_user(telegram_id=message.from_user.id):
        await message.answer("Привіт, я особистий бот alennamaer")
        await state.clear()
    else:
        await state.set_state(RegisterUser.registration_email)
        await message.answer(
            "Привіт, я особистий бот alennamaer\nДля початку поділись своєю поштою, щоб я точно більше не загубив тебе"
        )


@user_router.message(RegisterUser.registration_email)
async def register_phone(message: Message, state: FSMContext, apscheduler:AsyncIOScheduler):
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
        await state.clear()
        await send_message_in_1_min(bot, message.from_user.id)
        apscheduler.add_job(
            send_message_in_2_min,
            trigger="date",
            run_date=datetime.now() + timedelta(seconds=20),
            kwargs={"bot": bot, "user_id": message.from_user.id},
        )
        apscheduler.add_job(
            send_message_in_5_min,
            trigger="date",
            run_date=datetime.now() + timedelta(minutes=1),
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
