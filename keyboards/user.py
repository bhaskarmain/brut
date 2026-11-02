"""
User Panel Keyboards.
Clean, modern, emoji-enhanced inline keyboards for the user experience.
"""

from typing import List, Dict, Any, Optional
from urllib.parse import quote
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import is_admin


def get_main_menu_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """Main menu keyboard shown after /start."""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text="🎬 Watch Videos", callback_data="watch_videos_menu")
    )
    builder.row(
        InlineKeyboardButton(text="🎁 Referral Rewards", callback_data="referral_dashboard"),
        InlineKeyboardButton(text="👤 My Account", callback_data="my_account")
    )
    builder.row(
        InlineKeyboardButton(text="📊 My Statistics", callback_data="my_statistics"),
        InlineKeyboardButton(text="ℹ️ Help", callback_data="help_menu")
    )

    # If the user is an admin, show a quick shortcut to the Admin Panel
    if is_admin(user_id):
        builder.row(
            InlineKeyboardButton(text="🛠 Open Admin Panel", callback_data="admin_dashboard")
        )

    return builder.as_markup()


def get_categories_keyboard(categories: List[Dict[str, Any]]) -> InlineKeyboardMarkup:
    """Keyboard displaying all available video categories without video counts."""
    builder = InlineKeyboardBuilder()

    for cat in categories:
        builder.button(
            text=f"{cat.get('emoji', '📁')} {cat['name']}",
            callback_data=f"play_cat_{cat['id']}"
        )
    builder.adjust(2)  # 2 categories per row

    # Bottom helper buttons (Random button removed as requested)
    builder.row(
        InlineKeyboardButton(text="🔙 Back to Main Menu", callback_data="main_menu")
    )

    return builder.as_markup()


def get_category_videos_keyboard(
    category_id: int,
    videos: List[Dict[str, Any]],
    page: int,
    total_pages: int
) -> InlineKeyboardMarkup:
    """Keyboard listing videos within a specific category with pagination."""
    builder = InlineKeyboardBuilder()

    for vid in videos:
        builder.row(
            InlineKeyboardButton(
                text=f"▶️ {vid['title'][:32]}",
                callback_data=f"show_vid_{vid['id']}"
            )
        )

    # Pagination navigation row
    nav_row = []
    if page > 1:
        nav_row.append(
            InlineKeyboardButton(text="◀️ Prev", callback_data=f"cat_{category_id}_{page - 1}")
        )
    nav_row.append(
        InlineKeyboardButton(text=f"📄 {page}/{total_pages}", callback_data="noop")
    )
    if page < total_pages:
        nav_row.append(
            InlineKeyboardButton(text="Next ▶️", callback_data=f"cat_{category_id}_{page + 1}")
        )
    builder.row(*nav_row)

    # Navigation buttons
    builder.row(
        InlineKeyboardButton(text="📂 All Categories", callback_data="browse_categories"),
        InlineKeyboardButton(text="🏠 Main Menu", callback_data="main_menu")
    )

    return builder.as_markup()


def get_video_view_keyboard(
    video_id: int,
    category_id: int
) -> InlineKeyboardMarkup:
    """Action buttons for a single video preview card."""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text="▶️ Watch Now", callback_data=f"play_vid_{video_id}")
    )
    builder.row(
        InlineKeyboardButton(text="🔙 Back to Category", callback_data=f"cat_{category_id}_1"),
        InlineKeyboardButton(text="🏠 Main Menu", callback_data="main_menu")
    )

    return builder.as_markup()


def get_video_player_keyboard(category_id: int) -> InlineKeyboardMarkup:
    """Controls shown underneath the sent video player."""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text="▶️ Next Video", callback_data=f"play_cat_{category_id}"),
        InlineKeyboardButton(text="🎬 Watch Videos", callback_data="watch_videos_menu")
    )
    builder.row(
        InlineKeyboardButton(text="🏠 Main Menu", callback_data="main_menu")
    )

    return builder.as_markup()


def get_referral_dashboard_keyboard(
    unclaimed_rewards: int,
    referral_link: str
) -> InlineKeyboardMarkup:
    """Referral dashboard with claim button, share button, and leaderboard."""
    builder = InlineKeyboardBuilder()

    # If unclaimed rewards are ready, show claim button prominently at top
    if unclaimed_rewards > 0:
        builder.row(
            InlineKeyboardButton(
                text=f"🎁 Claim Free Video Reward ({unclaimed_rewards} Ready!)",
                callback_data="claim_reward"
            )
        )

    # Share referral link directly in Telegram
    share_text = quote("🎬 Join this Telegram Video Bot to watch amazing videos and unlock free video rewards! Tap the link below to get started:")
    share_url = f"https://t.me/share/url?url={quote(referral_link)}&text={share_text}"

    builder.row(
        InlineKeyboardButton(text="📤 Share Referral Link", url=share_url),
        InlineKeyboardButton(text="🏆 Leaderboard", callback_data="referral_leaderboard")
    )
    builder.row(
        InlineKeyboardButton(text="🔄 Refresh Stats", callback_data="referral_dashboard"),
        InlineKeyboardButton(text="🔙 Back to Main Menu", callback_data="main_menu")
    )

    return builder.as_markup()


def get_leaderboard_keyboard() -> InlineKeyboardMarkup:
    """Leaderboard navigation."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🔙 Back to Referral Dashboard", callback_data="referral_dashboard"),
        InlineKeyboardButton(text="🏠 Main Menu", callback_data="main_menu")
    )
    return builder.as_markup()


def get_account_keyboard() -> InlineKeyboardMarkup:
    """Account & Statistics navigation."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🎁 Referral Rewards", callback_data="referral_dashboard"),
        InlineKeyboardButton(text="🎬 Watch Videos", callback_data="watch_videos_menu")
    )
    builder.row(
        InlineKeyboardButton(text="🔄 Refresh", callback_data="my_account"),
        InlineKeyboardButton(text="🏠 Main Menu", callback_data="main_menu")
    )
    return builder.as_markup()


def get_help_keyboard() -> InlineKeyboardMarkup:
    """Help menu navigation."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🎬 Watch Videos", callback_data="watch_videos_menu"),
        InlineKeyboardButton(text="🎁 Referral Program", callback_data="referral_dashboard")
    )
    builder.row(
        InlineKeyboardButton(text="🔙 Back to Main Menu", callback_data="main_menu")
    )
    return builder.as_markup()


def get_back_to_menu_keyboard() -> InlineKeyboardMarkup:
    """Simple back to main menu keyboard."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🔙 Back to Main Menu", callback_data="main_menu")
    )
    return builder.as_markup()

