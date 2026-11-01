"""
Admin Panel Keyboards.
Complete navigation, management buttons, and FSM controls for administrators.
"""

from typing import List, Dict, Any, Optional
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_admin_dashboard_keyboard() -> InlineKeyboardMarkup:
    """Main administrative dashboard with all required management modules."""
    builder = InlineKeyboardBuilder()

    # Video & Category Management
    builder.row(
        InlineKeyboardButton(text="📤 Upload Video", callback_data="admin_upload_video"),
        InlineKeyboardButton(text="📂 Add Category", callback_data="admin_add_category")
    )
    builder.row(
        InlineKeyboardButton(text="📋 Manage Videos", callback_data="admin_manage_videos_1"),
        InlineKeyboardButton(text="✏️ Edit Category", callback_data="admin_edit_categories")
    )
    builder.row(
        InlineKeyboardButton(text="🗑 Delete Video", callback_data="admin_delete_video_pick"),
        InlineKeyboardButton(text="👥 All Users", callback_data="admin_users_1")
    )
    builder.row(
        InlineKeyboardButton(text="📊 Bot Statistics", callback_data="admin_stats"),
        InlineKeyboardButton(text="🎁 Referral Settings", callback_data="admin_referral_settings")
    )
    builder.row(
        InlineKeyboardButton(text="📢 Broadcast Message", callback_data="admin_broadcast"),
        InlineKeyboardButton(text="🚫 Ban/Unban User", callback_data="admin_ban_user")
    )
    builder.row(
        InlineKeyboardButton(text="⚙️ Bot Settings", callback_data="admin_bot_settings"),
        InlineKeyboardButton(text="🔙 User Panel", callback_data="main_menu")
    )

    return builder.as_markup()


def get_admin_category_select_keyboard(
    categories: List[Dict[str, Any]],
    action_prefix: str
) -> InlineKeyboardMarkup:
    """Category selector for uploading videos, editing, or deleting."""
    builder = InlineKeyboardBuilder()

    for cat in categories:
        builder.button(
            text=f"{cat.get('emoji', '📁')} {cat['name']} ({cat.get('video_count', 0)})",
            callback_data=f"{action_prefix}_{cat['id']}"
        )
    builder.adjust(2)

    builder.row(
        InlineKeyboardButton(text="❌ Cancel & Return", callback_data="admin_cancel")
    )

    return builder.as_markup()


def get_admin_edit_category_actions_keyboard(category_id: int) -> InlineKeyboardMarkup:
    """Options for modifying a selected category."""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text="✏️ Rename Category", callback_data=f"admin_rename_cat_{category_id}"),
        InlineKeyboardButton(text="🎨 Change Emoji", callback_data=f"admin_reemoji_cat_{category_id}")
    )
    builder.row(
        InlineKeyboardButton(text="🗑 Delete Category (All Videos)", callback_data=f"admin_del_cat_confirm_{category_id}")
    )
    builder.row(
        InlineKeyboardButton(text="🔙 Back to Categories", callback_data="admin_edit_categories"),
        InlineKeyboardButton(text="🛠 Admin Menu", callback_data="admin_dashboard")
    )

    return builder.as_markup()


def get_admin_manage_videos_keyboard(
    videos: List[Dict[str, Any]],
    page: int,
    total_pages: int
) -> InlineKeyboardMarkup:
    """Paginated list of all videos for management."""
    builder = InlineKeyboardBuilder()

    for vid in videos:
        builder.row(
            InlineKeyboardButton(
                text=f"🎬 [{vid.get('category_emoji', '📁')}] {vid['title'][:28]} ({vid.get('views_count', 0)} views)",
                callback_data=f"admin_vid_detail_{vid['id']}"
            )
        )

    # Pagination row
    nav_row = []
    if page > 1:
        nav_row.append(
            InlineKeyboardButton(text="◀️ Prev", callback_data=f"admin_manage_videos_{page - 1}")
        )
    nav_row.append(
        InlineKeyboardButton(text=f"📄 {page}/{total_pages}", callback_data="noop")
    )
    if page < total_pages:
        nav_row.append(
            InlineKeyboardButton(text="Next ▶️", callback_data=f"admin_manage_videos_{page + 1}")
        )
    builder.row(*nav_row)

    builder.row(
        InlineKeyboardButton(text="📤 Upload New Video", callback_data="admin_upload_video"),
        InlineKeyboardButton(text="🛠 Admin Menu", callback_data="admin_dashboard")
    )

    return builder.as_markup()


def get_admin_video_actions_keyboard(video_id: int) -> InlineKeyboardMarkup:
    """Action buttons for a single video in admin panel."""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text="👁 Preview Video", callback_data=f"admin_preview_vid_{video_id}"),
        InlineKeyboardButton(text="✏️ Edit Title", callback_data=f"admin_edit_vid_title_{video_id}")
    )
    builder.row(
        InlineKeyboardButton(text="🗑 Delete This Video", callback_data=f"admin_del_vid_confirm_{video_id}")
    )
    builder.row(
        InlineKeyboardButton(text="🔙 Back to Videos List", callback_data="admin_manage_videos_1"),
        InlineKeyboardButton(text="🛠 Admin Menu", callback_data="admin_dashboard")
    )

    return builder.as_markup()


def get_admin_users_keyboard(
    users: List[Dict[str, Any]],
    page: int,
    has_next: bool
) -> InlineKeyboardMarkup:
    """Paginated list of users."""
    builder = InlineKeyboardBuilder()

    for u in users:
        ban_mark = "🚫 " if u.get("is_banned") else ""
        name = u.get("first_name") or u.get("username") or f"ID {u['user_id']}"
        builder.row(
            InlineKeyboardButton(
                text=f"{ban_mark}{name[:16]} | Refs: {u.get('referral_count', 0)} | Vids: {u.get('watched_count', 0)}",
                callback_data=f"admin_user_info_{u['user_id']}"
            )
        )

    nav_row = []
    if page > 1:
        nav_row.append(
            InlineKeyboardButton(text="◀️ Prev", callback_data=f"admin_users_{page - 1}")
        )
    nav_row.append(
        InlineKeyboardButton(text=f"📄 Page {page}", callback_data="noop")
    )
    if has_next:
        nav_row.append(
            InlineKeyboardButton(text="Next ▶️", callback_data=f"admin_users_{page + 1}")
        )
    builder.row(*nav_row)

    builder.row(
        InlineKeyboardButton(text="🚫 Ban/Unban by ID", callback_data="admin_ban_user"),
        InlineKeyboardButton(text="🛠 Admin Menu", callback_data="admin_dashboard")
    )

    return builder.as_markup()


def get_admin_user_card_keyboard(target_user_id: int, is_banned: bool) -> InlineKeyboardMarkup:
    """Action buttons for viewing a specific user."""
    builder = InlineKeyboardBuilder()

    ban_text = "✅ Unban User" if is_banned else "🚫 Ban User"
    ban_action = f"admin_toggle_ban_{target_user_id}"

    builder.row(
        InlineKeyboardButton(text=ban_text, callback_data=ban_action)
    )
    builder.row(
        InlineKeyboardButton(text="🔙 Users List", callback_data="admin_users_1"),
        InlineKeyboardButton(text="🛠 Admin Menu", callback_data="admin_dashboard")
    )

    return builder.as_markup()


def get_referral_settings_keyboard(is_enabled: bool, req: int) -> InlineKeyboardMarkup:
    """Referral management controls."""
    builder = InlineKeyboardBuilder()

    toggle_text = "🔴 Disable Referral System" if is_enabled else "🟢 Enable Referral System"
    builder.row(
        InlineKeyboardButton(text=toggle_text, callback_data="admin_toggle_referral")
    )
    builder.row(
        InlineKeyboardButton(text=f"✏️ Change Requirement ({req} refs/reward)", callback_data="admin_set_ref_req")
    )
    builder.row(
        InlineKeyboardButton(text="🏆 View Leaderboard", callback_data="referral_leaderboard")
    )
    builder.row(
        InlineKeyboardButton(text="🔙 Back to Admin", callback_data="admin_dashboard")
    )

    return builder.as_markup()


def get_admin_confirm_keyboard(confirm_action: str, cancel_action: str = "admin_dashboard") -> InlineKeyboardMarkup:
    """Generic confirmation keyboard."""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text="✅ Confirm", callback_data=confirm_action),
        InlineKeyboardButton(text="❌ Cancel", callback_data=cancel_action)
    )

    return builder.as_markup()


def get_admin_cancel_keyboard(return_action: str = "admin_dashboard") -> InlineKeyboardMarkup:
    """Cancel button for interactive FSM states."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="❌ Cancel Operation", callback_data=return_action)
    )
    return builder.as_markup()


def get_admin_back_keyboard() -> InlineKeyboardMarkup:
    """Simple back to admin dashboard keyboard."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🔙 Back to Admin Dashboard", callback_data="admin_dashboard")
    )
    return builder.as_markup()

