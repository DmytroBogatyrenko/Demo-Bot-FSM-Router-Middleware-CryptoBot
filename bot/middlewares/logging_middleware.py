
import logging
from typing import Any, Awaitable, Callable, Dict
 
from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
 
logger = logging.getLogger(__name__)
 
 
class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:

        if isinstance(event, Message):
            logger.info(
                "Повідомлення від user_id=%s (%s): %s",
                event.from_user.id,
                event.from_user.username,
                event.text,
            )

        result = await handler(event, data)
        return result
 