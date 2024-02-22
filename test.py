import logging
from aiogram import Bot, Dispatcher, types

API_TOKEN = "6296590941:AAGE9bkcn2BGna2gL_pjuvSzneWjZE6F-RM"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Список ідентифікаторів адміністраторів
admin_ids = [123456789, 987654321]

# Обробник команди /broadcast
@dp.message_handler(commands=["broadcast"])
async def command_broadcast(message: types.Message):
    # Перевірка, чи відправник є адміністратором
    if message.from_user.id not in admin_ids:
        return

    # Отримання тексту повідомлення для розсилки
    text = message.get_args()
    if not text:
        await message.reply("Ви не вказали текст для розсилки.")
        return

    # Відправка повідомлення всім користувачам бота
    for user_id in admin_ids:
        try:
            await bot.send_message(user_id, text)
        except Exception as e:
            logging.exception(
                f"Помилка при відправці повідомлення користувачу {user_id}: {e}"
            )

    await message.reply("Розсилка завершена.")


if __name__ == "__main__":
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
