import asyncio
import logging
 
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
 
from bot.config import settings
from bot.handlers import payments, registration, start, telegram_payments
from bot.middlewares.logging_middleware import LoggingMiddleware
 
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
 
 
async def main() -> None:
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())

    dp.message.middleware(LoggingMiddleware())
 
    dp.include_router(start.router)
    dp.include_router(registration.router)
    dp.include_router(payments.router)
    dp.include_router(telegram_payments.router)
 
    await bot.delete_webhook(drop_pending_updates=True)
 
    logging.info("Бот запускається")
    await dp.start_polling(bot)
 
 
if __name__ == "__main__":
    asyncio.run(main())
 