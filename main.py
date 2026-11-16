import asyncio
import sys
from loguru import logger
from config import settings
from database import init_db
from bot import bot, dp

async def main():
    logger.remove()
    logger.add(sys.stdout, format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", level="INFO")
    
    logger.info("1. Инициализация локальной базы данных (SQLite)...")
    await init_db()

    logger.info("2. Запуск Telegram-бота...")
    try:
        bot_info = await bot.get_me()
        logger.info(f"Бот успешно подключен как @{bot_info.username}!")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка запуска бота: {e}")
    finally:
        await bot.session.close()
        logger.info("Бот остановлен.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Программа остановлена пользователем.")