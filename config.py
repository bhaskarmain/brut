"""
Configuration module for Smart Video Reward Telegram Bot.
Loads environment variables and validates critical settings.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Base Directory
BASE_DIR = Path(__file__).resolve().parent

# Load .env file
ENV_PATH = BASE_DIR / ".env"
if ENV_PATH.exists():
    load_dotenv(ENV_PATH)
else:
    load_dotenv()

# Telegram Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

# Admin IDs list (Default authorized admin: 8789936408)
raw_admin_ids = os.getenv("ADMIN_IDS", "8789936408").strip()
ADMIN_IDS = set()
if raw_admin_ids:
    for aid in raw_admin_ids.split(","):
        aid = aid.strip()
        if aid.isdigit():
            ADMIN_IDS.add(int(aid))
ADMIN_IDS.add(8789936408)

# Database Path
DATABASE_PATH = os.getenv("DATABASE_PATH", str(BASE_DIR / "data" / "bot.db"))
# Ensure directory exists
Path(DATABASE_PATH).parent.mkdir(parents=True, exist_ok=True)

# Referral Settings Defaults
DEFAULT_REFERRALS_PER_REWARD = int(os.getenv("DEFAULT_REFERRALS_PER_REWARD", "2"))
DEFAULT_REFERRAL_ENABLED = int(os.getenv("DEFAULT_REFERRAL_ENABLED", "1"))


def is_admin(user_id: int) -> bool:
    """Check if a given user_id is in the ADMIN_IDS set."""
    return user_id in ADMIN_IDS


def validate_config() -> None:
    """Validate that required configuration options are set."""
    if not BOT_TOKEN or BOT_TOKEN == "123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ":
        raise ValueError(
            "❌ ERROR: BOT_TOKEN is missing or using default placeholder!\n"
            "Please create a .env file and set your actual Telegram Bot Token from @BotFather.\n"
            "Example: BOT_TOKEN=7123456789:AAH..."
        )
    if not ADMIN_IDS:
        print(
            "⚠️ WARNING: No ADMIN_IDS specified in .env. Admin panel will not be accessible to anyone!\n"
            "Add your Telegram ID to ADMIN_IDS in .env (get it from @userinfobot)."
        )

