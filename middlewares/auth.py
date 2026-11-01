"""
Authentication and Security Middlewares for aiogram 3.x.
Ensures banned users cannot interact with the bot.
"""

from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from database import db
from config import is_admin


class BannedUserMiddleware(BaseMiddleware):
    """Checks whether the requesting user is banned."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user = data.get("event_from_user")
        if not user:
            return await handler(event, data)

        # Admins always bypass ban check
        if is_admin(user.id):
            return await handler(event, data)

        is_banned = await db.is_user_banned(user.id)
        if is_banned:
            if isinstance(event, Message):
                await event.answer(
                    "🚫 <b>Access Denied</b>\n\n"
                    "Your account has been suspended by the bot administrator.\n"
                    "If you believe this is an error, please reach out to support.",
                    parse_mode="HTML"
                )
            elif isinstance(event, CallbackQuery):
                await event.answer(
                    "🚫 Access Denied: Your account has been suspended.",
                    show_alert=True
                )
            return

        return await handler(event, data)

