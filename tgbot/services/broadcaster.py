import asyncio
import logging
from typing import Union, List

from aiogram import Bot
from aiogram import exceptions
from aiogram.enums import ContentType
from aiogram.types import InlineKeyboardMarkup


async def send_message(
    bot: Bot,
    user_id: int,
    text: str,
    disable_notification: bool = False,
    reply_markup: InlineKeyboardMarkup = None,
) -> bool:
    """
    Safe messages sender

    :param bot: Bot instance.
    :param user_id: user id. If str - must contain only digits.
    :param text: text of the message.
    :param disable_notification: disable notification or not.
    :param reply_markup: reply markup.
    :return: success.
    """
    try:
        await bot.send_message(
            user_id,
            text,
            disable_notification=disable_notification,
            reply_markup=reply_markup,
        )
    except exceptions.TelegramBadRequest as e:
        logging.error("Telegram server says - Bad Request: chat not found")
    except exceptions.TelegramForbiddenError:
        logging.error(f"Target [ID:{user_id}]: got TelegramForbiddenError")
    except exceptions.TelegramRetryAfter as e:
        logging.error(
            f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.retry_after} seconds."
        )
        await asyncio.sleep(e.retry_after)
        return await send_message(
            bot, user_id, text, disable_notification, reply_markup
        )  # Recursive call
    except exceptions.TelegramAPIError:
        logging.exception(f"Target [ID:{user_id}]: failed")
    else:
        logging.info(f"Target [ID:{user_id}]: success")
        return True
    return False


async def send_photo(
    bot: Bot,
    user_id: int,
    photo: str,
    disable_notification: bool = False,
    reply_markup: InlineKeyboardMarkup = None,
    caption: str = None,
) -> bool:
    try:
        await bot.send_photo(
            user_id,
            photo,
            disable_notification=disable_notification,
            reply_markup=reply_markup,
            caption=caption,
        )
    except exceptions.TelegramBadRequest as e:
        logging.error("Telegram server says - Bad Request: chat not found")
    except exceptions.TelegramForbiddenError:
        logging.error(f"Target [ID:{user_id}]: got TelegramForbiddenError")
    except exceptions.TelegramRetryAfter as e:
        logging.error(
            f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.retry_after} seconds."
        )
        await asyncio.sleep(e.retry_after)
        return await send_photo(
            bot, user_id, photo, disable_notification, reply_markup, caption
        )  # Recursive call
    except exceptions.TelegramAPIError:
        logging.exception(f"Target [ID:{user_id}]: failed")
    else:
        logging.info(f"Target [ID:{user_id}]: success")
        return True
    return False


async def send_video(
    bot: Bot,
    user_id: int,
    video: str,
    disable_notification: bool = False,
    reply_markup: InlineKeyboardMarkup = None,
    caption: str = None,
) -> bool:
    try:
        await bot.send_video(
            user_id,
            video,
            disable_notification=disable_notification,
            reply_markup=reply_markup,
            caption=caption,
        )
    except exceptions.TelegramBadRequest as e:
        logging.error("Telegram server says - Bad Request: chat not found")
    except exceptions.TelegramForbiddenError:
        logging.error(f"Target [ID:{user_id}]: got TelegramForbiddenError")
    except exceptions.TelegramRetryAfter as e:
        logging.error(
            f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.retry_after} seconds."
        )
        await asyncio.sleep(e.retry_after)
        return await send_video(
            bot, user_id, video, disable_notification, reply_markup, caption
        )  # Recursive call
    except exceptions.TelegramAPIError:
        logging.exception(f"Target [ID:{user_id}]: failed")
    else:
        logging.info(f"Target [ID:{user_id}]: success")
        return True
    return False


async def broadcast(
    bot: Bot,
    users: List[Union[str, int]],
    message=None,
    text: str = None,
    disable_notification: bool = False,
    reply_markup: InlineKeyboardMarkup = None,
    content_type: str = ContentType.TEXT,
) -> int:
    """
    Simple broadcaster.
    :param bot: Bot instance.
    :param users: List of users.
    :param text: Text of the message.
    :param photo: Photo from message.
    :param disable_notification: Disable notification or not.
    :param reply_markup: Reply markup.
    :param content_type: Type of message.
    :return: Count of messages.
    """
    count = 0
    try:
        if content_type == ContentType.TEXT:
            for user_id in users:
                if await send_message(
                    bot, user_id, message.text, disable_notification, reply_markup
                ):
                    count += 1
                await asyncio.sleep(
                    0.05
                )  # 20 messages per second (Limit: 30 messages per second)
        elif content_type == ContentType.PHOTO:
            largest_photo = max(
                message.photo, key=lambda item: item.width * item.height
            )
            for user_id in users:
                if await send_photo(
                    bot,
                    user_id,
                    largest_photo.file_id,
                    disable_notification,
                    reply_markup,
                    caption=message.caption,
                ):
                    count += 1
                await asyncio.sleep(0.05)
        elif content_type == ContentType.VIDEO:
            for user_id in users:
                if await send_video(
                    bot,
                    user_id,
                    message.video.file_id,
                    disable_notification,
                    reply_markup,
                    caption=message.caption,
                ):
                    count += 1
                await asyncio.sleep(0.05)
    finally:
        logging.info(f"{count} messages successful sent.")

    return count
