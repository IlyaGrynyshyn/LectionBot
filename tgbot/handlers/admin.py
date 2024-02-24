from aiogram import Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from tgbot.config import load_config
from tgbot.db.sqllite import Database
from tgbot.filters.admin import AdminFilter
from tgbot.misc.states import AdminMakePost
from tgbot.services.broadcaster import broadcast

admin_router = Router()
admin_router.message.filter(AdminFilter())

config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode="HTML")


@admin_router.message(CommandStart())
async def admin_start(message: Message):
    await message.reply("Вітаю, адміне!")


@admin_router.message(Command("post"))
async def admin_post(message: Message, state: FSMContext):
    await state.set_state(AdminMakePost.make_post)
    await message.answer(
        "⚠ Будь обережна, ти в такому місці, де кожне повідомлення побачить кожен користувач боту, тому будь обережна 😄. "
        "А тепер напиши мені пост, і я його опублікую."
    )


@admin_router.message(AdminMakePost.make_post)
async def admin_make_post(message: Message, state: FSMContext):
    db = Database()
    telegram_users = db.select_all_users_by_user_id()
    result_list = [item[0] for item in telegram_users]
    print(result_list)
    admin_ids =  result_list
    if message.from_user.id not in admin_ids:
        return
    if not message.text and not message.photo and not message.video:
        await message.reply(
            "‼ Ви не вказали текст або не прикріпили медіафайл для розсилки."
        )
        return
    await broadcast(bot, admin_ids, message=message, content_type=message.content_type)

    await message.reply("🎉 Розсилка завершена! Для повторної розсилки вокористай /post")
    await state.clear()
