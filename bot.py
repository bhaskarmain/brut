"""
Main entry point for Smart Video Reward Telegram Bot.
Initializes aiogram Dispatcher, attaches routers, middlewares, and starts polling.
"""

import sys
import asyncio
import logging

# Ensure UTF-8 output encoding on Windows consoles
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommand, BotCommandScopeDefault

from config import BOT_TOKEN, ADMIN_IDS, validate_config
from database import db
from middlewares.auth import BannedUserMiddleware
from handlers import user, admin, videos, referral

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("SmartVideoBot")


async def setup_bot_commands(bot: Bot) -> None:
    """Register default slash commands visible in Telegram UI."""
    commands = [
        BotCommand(command="start", description="🎬 Open Main Dashboard"),
        BotCommand(command="admin", description="🛠 Admin Panel (Admins Only)")
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())


async def main() -> None:
    """Starts the bot with polling."""
    logger.info("Initializing Smart Video Reward Bot...")

    # Validate environment settings
    try:
        validate_config()
    except ValueError as e:
        logger.critical(str(e))
        sys.exit(1)

    # Initialize Database Schema
    logger.info("Verifying and initializing database schema...")
    await db.init_db()
    logger.info("Database schema initialized successfully.")

    # Initialize Bot instance
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    # Initialize Dispatcher
    dp = Dispatcher()

    # Register Middlewares
    dp.message.middleware(BannedUserMiddleware())
    dp.callback_query.middleware(BannedUserMiddleware())

    # Register Handler Routers (Admin first, then specialized modules, then general user)
    dp.include_router(admin.router)
    dp.include_router(referral.router)
    dp.include_router(videos.router)
    dp.include_router(user.router)

    # Setup Commands
    await setup_bot_commands(bot)

    # Fetch bot identity
    bot_info = await bot.get_me()
    logger.info("=" * 60)
    logger.info("🤖 Bot Username: @%s", bot_info.username)
    logger.info("👑 Authorized Admin IDs: %s", list(ADMIN_IDS) if ADMIN_IDS else "None")
    logger.info("⚡ Bot is running and polling for updates... Press Ctrl+C to stop.")
    logger.info("=" * 60)

    try:
        # Delete any pending webhook updates and start polling
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        logger.info("Bot stopped gracefully.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Process terminated by user.")
