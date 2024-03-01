import asyncio
import csv

from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from aiogram.types import Message, CallbackQuery

from tgbot.config import load_config
from tgbot.db.sqllite import Database
from tgbot.filters.admin import AdminFilter
from tgbot.keyboards.inline import make_post_keyboard
from tgbot.misc.states import AdminMakePost
from tgbot.services.broadcaster import broadcast

admin_router = Router()
admin_router.message.filter(AdminFilter())

config = load_config(".env")
bot = Bot(token=config.tg_bot.token)


@admin_router.message(CommandStart())
async def admin_start(message: Message):
    await message.reply("Вітаю, адміне!")


@admin_router.message(Command("post"))
async def admin_post(message: Message, state: FSMContext):
    await state.set_state(AdminMakePost.make_post)
    await message.answer(
        "⚠ Будь обережна, ти в такому місці, де кожне повідомлення побачить кожен користувач боту, тому будь обережна 😄. "
        "А тепер напиши мені пост, і я його опублікую.",
        reply_markup=make_post_keyboard(),
    )


@admin_router.callback_query(F.data == "cancel_make_post")
async def admin_cancel_make_post(query: CallbackQuery, state: FSMContext):
    await query.answer()
    await query.message.answer("Ти вийшла з режиму створення посту")
    await state.clear()


@admin_router.message(AdminMakePost.make_post)
async def admin_make_post(message: Message, state: FSMContext):
    db = Database()
    telegram_users: list[tuple] = db.select_all_users_by_user_id()
    admin_ids: list = [item[0] for item in telegram_users]
    if message.from_user.id not in config.tg_bot.admin_ids:
        return

    if not message.text and not (message.photo or message.video):
        await message.reply(
            "‼ Ти не ввела текст або не прикріпила медіафайл для розсилки."
        )
        return


    await broadcast(bot, admin_ids, message=message, content_type=message.content_type)

    await message.reply("🎉 Розсилка завершена! Для повторної розсилки використай /post")
    await state.clear()


@admin_router.message(Command("dump"))
async def admin_dump_db(message: Message):
    db = Database()
    dump_data = db.dump_db()

    with open("db_dump.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "telegram_id", "name", "username", "phone", "email"])
        writer.writerows(dump_data)

    await message.reply("Вже формую дамп бази даних")
    await asyncio.sleep(5)

    agenda = FSInputFile("db_dump.csv")

    await bot.send_document(chat_id=message.chat.id, document=agenda)
