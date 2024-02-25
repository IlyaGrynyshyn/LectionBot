from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def make_post_keyboard():
    buttons = [
        [
            InlineKeyboardButton(
                text="📝 Вийти звідси", callback_data="cancel_make_post"
            ),
        ],
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
    return keyboard
