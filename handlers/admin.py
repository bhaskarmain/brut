"""
Admin panel message and callback handlers.
Includes video upload, category management, video management, user administration,
broadcasting, referral configuration, and bot statistics.
"""

import asyncio
import logging
from typing import Optional
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError

from config import is_admin, ADMIN_IDS, DATABASE_PATH
from database import db
from services.video_service import video_service
from services.referral_service import referral_service
from keyboards.admin import (
    get_admin_dashboard_keyboard,
    get_admin_category_select_keyboard,
    get_admin_edit_category_actions_keyboard,
    get_admin_manage_videos_keyboard,
    get_admin_video_actions_keyboard,
    get_admin_users_keyboard,
    get_admin_user_card_keyboard,
    get_referral_settings_keyboard,
    get_admin_confirm_keyboard,
    get_admin_cancel_keyboard,
    get_admin_back_keyboard
)

logger = logging.getLogger(__name__)
router = Router(name="admin_router")


# =========================================================================
# FSM STATES DEFINITIONS
# =========================================================================

class AdminUploadStates(StatesGroup):
    waiting_for_category = State()
    waiting_for_video = State()
    waiting_for_title = State()
    waiting_for_description = State()


class AdminCategoryStates(StatesGroup):
    waiting_for_add_name = State()
    waiting_for_add_emoji = State()
    waiting_for_rename = State()
    waiting_for_reemoji = State()


class AdminVideoStates(StatesGroup):
    waiting_for_edit_title = State()


class AdminBroadcastStates(StatesGroup):
    waiting_for_content = State()
    waiting_for_confirmation = State()


class AdminBanStates(StatesGroup):
    waiting_for_user_id = State()


class AdminReferralStates(StatesGroup):
    waiting_for_requirement = State()


# =========================================================================
# MAIN ADMIN DASHBOARD ENTRY POINTS
# =========================================================================

@router.message(Command("admin"))
async def handle_admin_command(message: Message, state: FSMContext):
    """Command /admin to launch admin panel."""
    await state.clear()
    if not is_admin(message.from_user.id):
        await message.answer("🚫 <b>Access Denied:</b> You are not authorized to use the Admin Panel.", parse_mode="HTML")
        return

    text = (
        "🛠 <b>Smart Video Bot — Admin Dashboard</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "Welcome Administrator! Select a management module below 👇"
    )
    await message.answer(text, reply_markup=get_admin_dashboard_keyboard(), parse_mode="HTML")


@router.callback_query(F.data == "admin_dashboard")
async def handle_admin_dashboard_callback(callback: CallbackQuery, state: FSMContext):
    """Returns to the admin dashboard."""
    await state.clear()
    if not is_admin(callback.from_user.id):
        await callback.answer("🚫 Access denied.", show_alert=True)
        return

    text = (
        "🛠 <b>Smart Video Bot — Admin Dashboard</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "Welcome Administrator! Select a management module below 👇"
    )
    try:
        await callback.message.edit_text(text, reply_markup=get_admin_dashboard_keyboard(), parse_mode="HTML")
    except TelegramBadRequest:
        await callback.message.answer(text, reply_markup=get_admin_dashboard_keyboard(), parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "admin_cancel")
async def handle_admin_cancel(callback: CallbackQuery, state: FSMContext):
    """Cancels current FSM operation and returns to admin dashboard."""
    await state.clear()
    await callback.answer("Action cancelled.")
    text = (
        "🛠 <b>Smart Video Bot — Admin Dashboard</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "Current action cancelled. Select an option below 👇"
    )
    try:
        await callback.message.edit_text(text, reply_markup=get_admin_dashboard_keyboard(), parse_mode="HTML")
    except TelegramBadRequest:
        await callback.message.answer(text, reply_markup=get_admin_dashboard_keyboard(), parse_mode="HTML")


# =========================================================================
# 1. VIDEO UPLOAD WORKFLOW
# =========================================================================

@router.callback_query(F.data == "admin_upload_video")
async def handle_admin_upload_video_start(callback: CallbackQuery, state: FSMContext):
    """Step 1 of Video Upload: Select Category."""
    if not is_admin(callback.from_user.id):
        await callback.answer("🚫 Access denied.", show_alert=True)
        return

    categories = await video_service.get_all_categories()
    if not categories:
        await callback.answer("⚠️ No categories found. Please add a category first!", show_alert=True)
        return

    await state.set_state(AdminUploadStates.waiting_for_category)
    text = (
        "📤 <b>Upload Video — Step 1 of 4</b>\n\n"
        "Select the category for this video:"
    )
    keyboard = get_admin_category_select_keyboard(categories, action_prefix="admin_upcat")
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()


@router.callback_query(AdminUploadStates.waiting_for_category, F.data.startswith("admin_upcat_"))
async def handle_admin_upload_category_selected(callback: CallbackQuery, state: FSMContext):
    """Step 2 of Video Upload: Prompt for Video File."""
    cat_id = int(callback.data.split("_")[2])
    category = await video_service.get_category(cat_id)

    if not category:
        await callback.answer("Category not found.", show_alert=True)
        return

    await state.update_data(category_id=cat_id, category_name=category["name"])
    await state.set_state(AdminUploadStates.waiting_for_video)

    text = (
        f"📤 <b>Upload Video — Step 2 of 4</b>\n"
        f"Category: <b>{category.get('emoji', '📁')} {category['name']}</b>\n\n"
        f"Now send or forward the <b>video file</b> directly in this chat:"
    )
    await callback.message.edit_text(text, reply_markup=get_admin_cancel_keyboard(), parse_mode="HTML")
    await callback.answer()


@router.message(AdminUploadStates.waiting_for_video, F.video)
async def handle_admin_upload_video_file(message: Message, state: FSMContext):
    """Step 3 of Video Upload: Video received, prompt for Title."""
    video = message.video
    file_id = video.file_id
    file_unique_id = video.file_unique_id

    await state.update_data(file_id=file_id, file_unique_id=file_unique_id)
    await state.set_state(AdminUploadStates.waiting_for_title)

    text = (
        "📤 <b>Upload Video — Step 3 of 4</b>\n\n"
        "✅ Video file received!\n"
        "Now enter a <b>Title</b> for this video:"
    )
    await message.answer(text, reply_markup=get_admin_cancel_keyboard(), parse_mode="HTML")


@router.message(AdminUploadStates.waiting_for_video)
async def handle_admin_upload_video_invalid(message: Message):
    """Handles invalid non-video messages."""
    await message.answer(
        "⚠️ Please send a valid <b>video</b> file (MP4/MOV). Other file formats or text messages are not accepted.",
        reply_markup=get_admin_cancel_keyboard(),
        parse_mode="HTML"
    )


@router.message(AdminUploadStates.waiting_for_title, F.text)
async def handle_admin_upload_video_title(message: Message, state: FSMContext):
    """Step 4 of Video Upload: Title received, prompt for Description."""
    title = message.text.strip()
    if len(title) < 2:
        await message.answer("⚠️ Title must be at least 2 characters long. Please enter a valid title:")
        return

    await state.update_data(title=title)
    await state.set_state(AdminUploadStates.waiting_for_description)

    text = (
        f"📤 <b>Upload Video — Step 4 of 4</b>\n"
        f"Title: <b>{title}</b>\n\n"
        f"Enter a <b>Description</b> for this video, or send <code>/skip</code> if you don't want a description:"
    )
    await message.answer(text, reply_markup=get_admin_cancel_keyboard(), parse_mode="HTML")


@router.message(AdminUploadStates.waiting_for_description, F.text)
async def handle_admin_upload_video_description(message: Message, state: FSMContext):
    """Final Step: Save Video to Database."""
    data = await state.get_data()
    description = None if message.text.strip() == "/skip" else message.text.strip()

    category_id = data["category_id"]
    file_id = data["file_id"]
    file_unique_id = data["file_unique_id"]
    title = data["title"]

    video_id = await video_service.add_video(
        category_id=category_id,
        file_id=file_id,
        file_unique_id=file_unique_id,
        title=title,
        description=description
    )

    await state.clear()

    text = (
        f"🎉 <b>Video Uploaded Successfully!</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"🆔 <b>Video ID:</b> {video_id}\n"
        f"📂 <b>Category:</b> {data.get('category_name')}\n"
        f"🎬 <b>Title:</b> {title}\n"
        f"📝 <b>Description:</b> {description or 'None'}\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"The video is now live and available to all users!"
    )
    await message.answer(text, reply_markup=get_admin_dashboard_keyboard(), parse_mode="HTML")


# =========================================================================
# 2. CATEGORY MANAGEMENT WORKFLOW
# =========================================================================

@router.callback_query(F.data == "admin_add_category")
async def handle_admin_add_category_start(callback: CallbackQuery, state: FSMContext):
    """Prompt for new Category Name."""
    if not is_admin(callback.from_user.id):
        await callback.answer("🚫 Access denied.", show_alert=True)
        return

    await state.set_state(AdminCategoryStates.waiting_for_add_name)
    text = (
        "📂 <b>Add New Category — Step 1 of 2</b>\n\n"
        "Enter the <b>name</b> of the new category (e.g. <i>Action, Comedy, Tutorials</i>):"
    )
    await callback.message.edit_text(text, reply_markup=get_admin_cancel_keyboard(), parse_mode="HTML")
    await callback.answer()


@router.message(AdminCategoryStates.waiting_for_add_name, F.text)
async def handle_admin_add_category_name(message: Message, state: FSMContext):
    """Prompt for Category Emoji."""
    name = message.text.strip()
    if len(name) < 2:
        await message.answer("⚠️ Category name must be at least 2 characters. Try again:")
        return

    await state.update_data(cat_name=name)
    await state.set_state(AdminCategoryStates.waiting_for_add_emoji)

    text = (
        f"📂 <b>Add New Category — Step 2 of 2</b>\n"
        f"Name: <b>{name}</b>\n\n"
        f"Send an <b>emoji</b> for this category (e.g. 🎬, 🔥, 🎭, 🍿) or send <code>/skip</code> for default 📁:"
    )
    await message.answer(text, reply_markup=get_admin_cancel_keyboard(), parse_mode="HTML")


@router.message(AdminCategoryStates.waiting_for_add_emoji, F.text)
async def handle_admin_add_category_emoji(message: Message, state: FSMContext):
    """Save new category to database."""
    data = await state.get_data()
    name = data["cat_name"]
    emoji = "📁" if message.text.strip() == "/skip" else message.text.strip()[:4]

    cat_id = await video_service.create_category(name=name, emoji=emoji)
    await state.clear()

    text = (
        f"✅ <b>Category Created Successfully!</b>\n\n"
        f"🆔 ID: {cat_id}\n"
        f"📂 Name: {emoji} {name}"
    )
    await message.answer(text, reply_markup=get_admin_dashboard_keyboard(), parse_mode="HTML")


@router.callback_query(F.data == "admin_edit_categories")
async def handle_admin_edit_categories_list(callback: CallbackQuery):
    """List categories to edit."""
    if not is_admin(callback.from_user.id):
        await callback.answer("🚫 Access denied.", show_alert=True)
        return

    categories = await video_service.get_all_categories()
    if not categories:
        await callback.answer("⚠️ No categories to edit.", show_alert=True)
        return

    text = (
        "✏️ <b>Select a Category to Edit or Manage:</b>"
    )
    keyboard = get_admin_category_select_keyboard(categories, action_prefix="admin_pickcat")
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data.startswith("admin_pickcat_"))
async def handle_admin_pick_category(callback: CallbackQuery):
    """Show options for selected category."""
    cat_id = int(callback.data.split("_")[2])
    cat = await video_service.get_category(cat_id)
    if not cat:
        await callback.answer("Category not found.", show_alert=True)
        return

    text = (
        f"📂 <b>Category Details:</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"🆔 ID: {cat['id']}\n"
        f"🏷 Name: {cat.get('emoji', '📁')} {cat['name']}\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"What would you like to do with this category?"
    )
    keyboard = get_admin_edit_category_actions_keyboard(cat_id)
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data.startswith("admin_rename_cat_"))
async def handle_admin_rename_category_start(callback: CallbackQuery, state: FSMContext):
    """Start renaming category."""
    cat_id = int(callback.data.split("_")[3])
    await state.update_data(target_cat_id=cat_id)
    await state.set_state(AdminCategoryStates.waiting_for_rename)

    text = "✏️ Enter the <b>new name</b> for this category:"
    await callback.message.edit_text(text, reply_markup=get_admin_cancel_keyboard(), parse_mode="HTML")
    await callback.answer()


@router.message(AdminCategoryStates.waiting_for_rename, F.text)
async def handle_admin_rename_category_save(message: Message, state: FSMContext):
    """Save new category name."""
    data = await state.get_data()
    cat_id = data["target_cat_id"]
    new_name = message.text.strip()

    cat = await video_service.get_category(cat_id)
    if not cat:
        await message.answer("Category not found.", reply_markup=get_admin_dashboard_keyboard())
        await state.clear()
        return

    await video_service.update_category(cat_id, name=new_name, emoji=cat.get("emoji", "📁"))
    await state.clear()

    await message.answer(
        f"✅ Category renamed to: <b>{cat.get('emoji', '📁')} {new_name}</b>",
        reply_markup=get_admin_dashboard_keyboard(),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("admin_reemoji_cat_"))
async def handle_admin_reemoji_category_start(callback: CallbackQuery, state: FSMContext):
    """Start changing category emoji."""
    cat_id = int(callback.data.split("_")[3])
    await state.update_data(target_cat_id=cat_id)
    await state.set_state(AdminCategoryStates.waiting_for_reemoji)

    text = "🎨 Send the <b>new emoji</b> for this category:"
    await callback.message.edit_text(text, reply_markup=get_admin_cancel_keyboard(), parse_mode="HTML")
    await callback.answer()


@router.message(AdminCategoryStates.waiting_for_reemoji, F.text)
async def handle_admin_reemoji_category_save(message: Message, state: FSMContext):
    """Save new category emoji."""
    data = await state.get_data()
    cat_id = data["target_cat_id"]
    new_emoji = message.text.strip()[:4]

    cat = await video_service.get_category(cat_id)
    if not cat:
        await message.answer("Category not found.", reply_markup=get_admin_dashboard_keyboard())
        await state.clear()
        return

    await video_service.update_category(cat_id, name=cat["name"], emoji=new_emoji)
    await state.clear()

    await message.answer(
        f"✅ Category updated to: <b>{new_emoji} {cat['name']}</b>",
        reply_markup=get_admin_dashboard_keyboard(),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("admin_del_cat_confirm_"))
async def handle_admin_delete_cat_confirm(callback: CallbackQuery):
    """Confirm category deletion."""
    cat_id = int(callback.data.split("_")[4])
    cat = await video_service.get_category(cat_id)
    if not cat:
        await callback.answer("Category not found.", show_alert=True)
        return

    text = (
        f"⚠️ <b>Delete Category Confirmation</b>\n\n"
        f"Are you sure you want to permanently delete category <b>{cat.get('emoji', '📁')} {cat['name']}</b>?\n"
        f"<b>WARNING:</b> All videos inside this category will also be deleted!"
    )
    keyboard = get_admin_confirm_keyboard(
        confirm_action=f"admin_del_cat_do_{cat_id}",
        cancel_action="admin_edit_categories"
    )
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data.startswith("admin_del_cat_do_"))
async def handle_admin_delete_cat_perform(callback: CallbackQuery):
    """Execute category deletion."""
    cat_id = int(callback.data.split("_")[4])
    success = await video_service.delete_category(cat_id)

    if success:
        await callback.answer("✅ Category deleted successfully!", show_alert=True)
        text = "✅ <b>Category and its videos were permanently deleted.</b>"
    else:
        await callback.answer("⚠️ Failed to delete category.", show_alert=True)
        text = "⚠️ <b>Could not delete category.</b>"

    await callback.message.edit_text(text, reply_markup=get_admin_dashboard_keyboard(), parse_mode="HTML")


# =========================================================================
# 3. VIDEO MANAGEMENT & DELETION
# =========================================================================

@router.callback_query(F.data.startswith("admin_manage_videos_"))
async def handle_admin_manage_videos_list(callback: CallbackQuery):
    """Paginated list of all videos in the admin panel."""
    if not is_admin(callback.from_user.id):
        await callback.answer("🚫 Access denied.", show_alert=True)
        return

    page = int(callback.data.split("_")[3])
    videos, total_count, total_pages = await video_service.get_all_videos_paginated(page=page, page_size=6)

    if not videos:
        text = "📋 <b>Manage Videos</b>\n\nNo videos uploaded yet. Use <b>Upload Video</b> to add some!"
        await callback.message.edit_text(text, reply_markup=get_admin_back_keyboard(), parse_mode="HTML")
        await callback.answer()
        return

    text = (
        f"📋 <b>Manage Videos</b> (Total: <b>{total_count}</b>)\n"
        f"Page <b>{page}/{total_pages}</b>\n\n"
        f"Click any video to inspect, edit, or delete:"
    )
    keyboard = get_admin_manage_videos_keyboard(videos, page, total_pages)
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data.startswith("admin_vid_detail_"))
async def handle_admin_video_detail(callback: CallbackQuery):
    """Inspect a single video."""
    vid_id = int(callback.data.split("_")[3])
    video = await video_service.get_video(vid_id)

    if not video:
        await callback.answer("Video not found.", show_alert=True)
        return

    text = (
        f"🎬 <b>Video Information:</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"🆔 <b>ID:</b> {video['id']}\n"
        f"📂 <b>Category:</b> {video.get('category_emoji', '📁')} {video.get('category_name')}\n"
        f"🎬 <b>Title:</b> {video['title']}\n"
        f"👁 <b>Views:</b> {video.get('views_count', 0)}\n"
        f"📅 <b>Uploaded:</b> {video.get('created_at', '')[:19]}\n"
        f"📝 <b>Description:</b>\n{video.get('description') or 'None'}\n"
        f"━━━━━━━━━━━━━━━━━━━━━"
    )
    keyboard = get_admin_video_actions_keyboard(vid_id)
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data.startswith("admin_preview_vid_"))
async def handle_admin_preview_video(callback: CallbackQuery):
    """Sends preview of the video to admin."""
    vid_id = int(callback.data.split("_")[3])
    video = await video_service.get_video(vid_id)

    if not video:
        await callback.answer("Video not found.", show_alert=True)
        return

    await callback.answer("Sending preview...")
    await callback.message.answer_video(
        video=video["file_id"],
        caption=f"👁 <b>Admin Preview:</b> {video['title']}\nID: {video['id']}",
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("admin_edit_vid_title_"))
async def handle_admin_edit_vid_title_start(callback: CallbackQuery, state: FSMContext):
    """Prompt for new video title."""
    vid_id = int(callback.data.split("_")[4])
    await state.update_data(target_vid_id=vid_id)
    await state.set_state(AdminVideoStates.waiting_for_edit_title)

    text = "✏️ Enter the <b>new title</b> for this video:"
    await callback.message.edit_text(text, reply_markup=get_admin_cancel_keyboard(), parse_mode="HTML")
    await callback.answer()


@router.message(AdminVideoStates.waiting_for_edit_title, F.text)
async def handle_admin_edit_vid_title_save(message: Message, state: FSMContext):
    """Save new video title."""
    data = await state.get_data()
    vid_id = data["target_vid_id"]
    new_title = message.text.strip()

    video = await video_service.get_video(vid_id)
    if not video:
        await message.answer("Video not found.", reply_markup=get_admin_dashboard_keyboard())
        await state.clear()
        return

    await video_service.update_video(vid_id, title=new_title, description=video.get("description"))
    await state.clear()

    await message.answer(
        f"✅ Video title updated to: <b>{new_title}</b>",
        reply_markup=get_admin_dashboard_keyboard(),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("admin_del_vid_confirm_"))
async def handle_admin_del_vid_confirm(callback: CallbackQuery):
    """Confirm video deletion."""
    vid_id = int(callback.data.split("_")[4])
    video = await video_service.get_video(vid_id)
    if not video:
        await callback.answer("Video not found.", show_alert=True)
        return

    text = (
        f"⚠️ <b>Delete Video Confirmation</b>\n\n"
        f"Are you sure you want to permanently delete: <b>{video['title']}</b> (ID: {vid_id})?"
    )
    keyboard = get_admin_confirm_keyboard(
        confirm_action=f"admin_del_vid_do_{vid_id}",
        cancel_action="admin_manage_videos_1"
    )
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data.startswith("admin_del_vid_do_"))
async def handle_admin_del_vid_perform(callback: CallbackQuery):
    """Execute video deletion."""
    vid_id = int(callback.data.split("_")[4])
    success = await video_service.delete_video(vid_id)

    if success:
        await callback.answer("✅ Video deleted successfully!", show_alert=True)
        text = "✅ <b>Video was permanently removed from database.</b>"
    else:
        await callback.answer("⚠️ Could not delete video.", show_alert=True)
        text = "⚠️ <b>Could not delete video.</b>"

    await callback.message.edit_text(text, reply_markup=get_admin_dashboard_keyboard(), parse_mode="HTML")


@router.callback_query(F.data == "admin_delete_video_pick")
async def handle_admin_delete_video_shortcut(callback: CallbackQuery):
    """Shortcut: redirects to manage videos list where delete buttons are placed."""
    await handle_admin_manage_videos_list(callback)


# =========================================================================
# 4. USER ADMINISTRATION & BANNING
# =========================================================================

@router.callback_query(F.data.startswith("admin_users_"))
async def handle_admin_users_list(callback: CallbackQuery):
    """Displays paginated list of registered bot users."""
    if not is_admin(callback.from_user.id):
        await callback.answer("🚫 Access denied.", show_alert=True)
        return

    page = int(callback.data.split("_")[2])
    page_size = 10
    offset = (page - 1) * page_size

    users = await db.get_users_list(limit=page_size + 1, offset=offset)
    has_next = len(users) > page_size
    display_users = users[:page_size]

    if not display_users:
        text = "👥 <b>Users List:</b>\n\nNo users found."
        await callback.message.edit_text(text, reply_markup=get_admin_back_keyboard(), parse_mode="HTML")
        await callback.answer()
        return

    total_count = await db.get_total_users_count()
    text = (
        f"👥 <b>Registered Users Directory</b>\n"
        f"Total Registered: <b>{total_count}</b> | Page <b>{page}</b>\n\n"
        f"Tap any user to view profile or change ban status:"
    )
    keyboard = get_admin_users_keyboard(display_users, page, has_next)
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data.startswith("admin_user_info_"))
async def handle_admin_user_info(callback: CallbackQuery):
    """Displays detailed card for a single user."""
    target_id = int(callback.data.split("_")[3])
    user = await db.get_user(target_id)

    if not user:
        await callback.answer("User not found in database.", show_alert=True)
        return

    watched_count = await db.get_user_watched_count(target_id)
    ref_stats = await db.get_referral_stats(target_id)

    ban_badge = "🔴 BANNED" if user.get("is_banned") else "🟢 ACTIVE"
    name = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip() or "Unnamed"
    uname = f"@{user.get('username')}" if user.get("username") else "No username"

    text = (
        f"👤 <b>User Inspection Card:</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"🆔 <b>Telegram ID:</b> <code>{target_id}</code>\n"
        f"👤 <b>Name:</b> {name}\n"
        f"🏷 <b>Username:</b> {uname}\n"
        f"⚡ <b>Status:</b> {ban_badge}\n"
        f"📅 <b>Joined:</b> {user.get('joined_at', '')[:19]}\n"
        f"🕒 <b>Last Active:</b> {user.get('last_active', '')[:19]}\n\n"
        f"👥 <b>Successful Referrals:</b> {ref_stats['valid_referrals']}\n"
        f"🎁 <b>Rewards Claimed:</b> {ref_stats['rewards_claimed']}\n"
        f"🎬 <b>Videos Watched:</b> {watched_count}\n"
        f"━━━━━━━━━━━━━━━━━━━━━"
    )
    keyboard = get_admin_user_card_keyboard(target_id, bool(user.get("is_banned")))
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data.startswith("admin_toggle_ban_"))
async def handle_admin_toggle_ban(callback: CallbackQuery):
    """Toggles ban status of a user."""
    target_id = int(callback.data.split("_")[3])
    user = await db.get_user(target_id)

    if not user:
        await callback.answer("User not found.", show_alert=True)
        return

    new_ban_state = not bool(user.get("is_banned"))
    await db.set_user_ban(target_id, new_ban_state)

    state_text = "banned" if new_ban_state else "unbanned"
    await callback.answer(f"User {target_id} has been {state_text}!", show_alert=True)

    # Refresh card
    await handle_admin_user_info(callback)


@router.callback_query(F.data == "admin_ban_user")
async def handle_admin_ban_user_prompt(callback: CallbackQuery, state: FSMContext):
    """Prompt for user ID to ban or unban."""
    if not is_admin(callback.from_user.id):
        await callback.answer("🚫 Access denied.", show_alert=True)
        return

    await state.set_state(AdminBanStates.waiting_for_user_id)
    text = (
        "🚫 <b>Ban/Unban User by Telegram ID</b>\n\n"
        "Enter the numeric <b>Telegram User ID</b> to inspect and toggle ban status:"
    )
    await callback.message.edit_text(text, reply_markup=get_admin_cancel_keyboard(), parse_mode="HTML")
    await callback.answer()


@router.message(AdminBanStates.waiting_for_user_id, F.text)
async def handle_admin_ban_user_received(message: Message, state: FSMContext):
    """Process user ID input."""
    raw = message.text.strip()
    if not raw.isdigit():
        await message.answer("⚠️ Please enter a valid numeric Telegram ID (e.g. 12345678):", reply_markup=get_admin_cancel_keyboard())
        return

    target_id = int(raw)
    user = await db.get_user(target_id)
    await state.clear()

    if not user:
        await message.answer(
            f"⚠️ User ID <code>{target_id}</code> was not found in the bot's database.",
            reply_markup=get_admin_dashboard_keyboard(),
            parse_mode="HTML"
        )
        return

    # Render card
    ban_badge = "🔴 BANNED" if user.get("is_banned") else "🟢 ACTIVE"
    name = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip() or "Unnamed"

    text = (
        f"👤 <b>User Found:</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"🆔 ID: <code>{target_id}</code>\n"
        f"👤 Name: {name}\n"
        f"⚡ Status: {ban_badge}\n"
        f"━━━━━━━━━━━━━━━━━━━━━"
    )
    keyboard = get_admin_user_card_keyboard(target_id, bool(user.get("is_banned")))
    await message.answer(text, reply_markup=keyboard, parse_mode="HTML")


# =========================================================================
# 5. BOT STATISTICS
# =========================================================================

@router.callback_query(F.data == "admin_stats")
async def handle_admin_stats(callback: CallbackQuery):
    """Displays global bot metrics and health status."""
    if not is_admin(callback.from_user.id):
        await callback.answer("🚫 Access denied.", show_alert=True)
        return

    total_users = await db.get_total_users_count()
    banned_users = await db.get_banned_users_count()
    active_24h = await db.get_active_users_24h_count()

    video_stats = await video_service.get_video_stats()
    total_referrals = await db.get_total_referrals_count()

    text = (
        f"📊 <b>Bot Global Statistics & Analytics</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"👥 <b>Total Users:</b> {total_users}\n"
        f"⚡ <b>Active Users (Last 24h):</b> {active_24h}\n"
        f"🚫 <b>Banned Users:</b> {banned_users}\n\n"
        f"📂 <b>Total Categories:</b> {video_stats['total_categories']}\n"
        f"🎬 <b>Total Videos:</b> {video_stats['total_videos']}\n"
        f"👁 <b>Total Video Views:</b> {video_stats['total_views']}\n\n"
        f"🤝 <b>Total Successful Referrals:</b> {total_referrals}\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"🟢 <b>Bot Status:</b> Operational & Healthy"
    )
    await callback.message.edit_text(text, reply_markup=get_admin_back_keyboard(), parse_mode="HTML")
    await callback.answer()


# =========================================================================
# 6. REFERRAL SETTINGS
# =========================================================================

@router.callback_query(F.data == "admin_referral_settings")
async def handle_admin_referral_settings(callback: CallbackQuery):
    """Displays referral configuration panel."""
    if not is_admin(callback.from_user.id):
        await callback.answer("🚫 Access denied.", show_alert=True)
        return

    settings = await referral_service.get_system_settings()
    is_enabled = settings["is_enabled"]
    req = settings["required_per_reward"]

    status_str = "🟢 Enabled (Active)" if is_enabled else "🔴 Disabled (Paused)"

    text = (
        f"🎁 <b>Referral Rewards Configuration</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"⚙️ <b>Current Status:</b> {status_str}\n"
        f"🎯 <b>Requirement:</b> <b>{req}</b> referrals per reward\n"
        f"🏆 <b>Reward Type:</b> Random Video Distribution\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"Modify settings using the buttons below:"
    )
    keyboard = get_referral_settings_keyboard(is_enabled, req)
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "admin_toggle_referral")
async def handle_admin_toggle_referral(callback: CallbackQuery):
    """Toggle referral system on or off."""
    settings = await referral_service.get_system_settings()
    new_state = not settings["is_enabled"]
    await referral_service.toggle_referral_system(new_state)

    state_text = "enabled" if new_state else "disabled"
    await callback.answer(f"Referral system {state_text}!", show_alert=True)
    await handle_admin_referral_settings(callback)


@router.callback_query(F.data == "admin_set_ref_req")
async def handle_admin_set_ref_req_start(callback: CallbackQuery, state: FSMContext):
    """Prompt for new referral requirement number."""
    if not is_admin(callback.from_user.id):
        await callback.answer("🚫 Access denied.", show_alert=True)
        return

    await state.set_state(AdminReferralStates.waiting_for_requirement)
    text = (
        "✏️ <b>Change Referral Requirement</b>\n\n"
        "Enter how many referrals are required to unlock 1 free video (e.g. 1, 2, 3, 5):"
    )
    await callback.message.edit_text(text, reply_markup=get_admin_cancel_keyboard("admin_referral_settings"), parse_mode="HTML")
    await callback.answer()


@router.message(AdminReferralStates.waiting_for_requirement, F.text)
async def handle_admin_set_ref_req_save(message: Message, state: FSMContext):
    """Save new referral requirement number."""
    val = message.text.strip()
    if not val.isdigit() or int(val) < 1:
        await message.answer("⚠️ Please enter a positive integer (at least 1):")
        return

    new_req = int(val)
    await referral_service.update_requirement(new_req)
    await state.clear()

    await message.answer(
        f"✅ Referral requirement updated to: <b>{new_req} referrals = 1 reward</b>",
        reply_markup=get_admin_dashboard_keyboard(),
        parse_mode="HTML"
    )


# =========================================================================
# 7. BROADCAST MESSAGE TO ALL USERS
# =========================================================================

@router.callback_query(F.data == "admin_broadcast")
async def handle_admin_broadcast_start(callback: CallbackQuery, state: FSMContext):
    """Step 1 of Broadcast: Prompt for content."""
    if not is_admin(callback.from_user.id):
        await callback.answer("🚫 Access denied.", show_alert=True)
        return

    await state.set_state(AdminBroadcastStates.waiting_for_content)
    text = (
        "📢 <b>Broadcast Announcement to All Users</b>\n\n"
        "Send the message you want to broadcast.\n"
        "Supports:\n"
        "• Plain text with HTML formatting\n"
        "• Photo with caption\n"
        "• Video with caption"
    )
    await callback.message.edit_text(text, reply_markup=get_admin_cancel_keyboard(), parse_mode="HTML")
    await callback.answer()


@router.message(AdminBroadcastStates.waiting_for_content)
async def handle_admin_broadcast_content(message: Message, state: FSMContext):
    """Step 2 of Broadcast: Preview and Ask Confirmation."""
    # Store message details
    if message.photo:
        await state.update_data(
            msg_type="photo",
            file_id=message.photo[-1].file_id,
            caption=message.caption or ""
        )
    elif message.video:
        await state.update_data(
            msg_type="video",
            file_id=message.video.file_id,
            caption=message.caption or ""
        )
    elif message.text:
        await state.update_data(
            msg_type="text",
            text=message.text
        )
    else:
        await message.answer("⚠️ Unsupported message format. Please send text, photo, or video.", reply_markup=get_admin_cancel_keyboard())
        return

    await state.set_state(AdminBroadcastStates.waiting_for_confirmation)

    total_users = await db.get_total_users_count()
    confirm_text = (
        f"📢 <b>Broadcast Preview Confirmed</b>\n\n"
        f"This announcement will be delivered to approximately <b>{total_users} users</b>.\n"
        f"Are you sure you want to proceed?"
    )
    keyboard = get_admin_confirm_keyboard(
        confirm_action="admin_broadcast_execute",
        cancel_action="admin_cancel"
    )
    await message.answer(confirm_text, reply_markup=keyboard, parse_mode="HTML")


@router.callback_query(AdminBroadcastStates.waiting_for_confirmation, F.data == "admin_broadcast_execute")
async def handle_admin_broadcast_execute(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """Step 3 of Broadcast: Safe asynchronous delivery to all users."""
    data = await state.get_data()
    await state.clear()

    user_ids = await db.get_all_user_ids()
    total = len(user_ids)

    status_msg = await callback.message.edit_text(
        f"⏳ <b>Broadcasting in progress...</b>\n0/{total} delivered.",
        parse_mode="HTML"
    )

    success_count = 0
    fail_count = 0

    msg_type = data.get("msg_type")
    caption = data.get("caption", "")
    file_id = data.get("file_id")
    text_content = data.get("text", "")

    for idx, uid in enumerate(user_ids, 1):
        try:
            if msg_type == "text":
                await bot.send_message(chat_id=uid, text=text_content, parse_mode="HTML")
            elif msg_type == "photo":
                await bot.send_photo(chat_id=uid, photo=file_id, caption=caption, parse_mode="HTML")
            elif msg_type == "video":
                await bot.send_video(chat_id=uid, video=file_id, caption=caption, parse_mode="HTML")

            success_count += 1
        except (TelegramForbiddenError, TelegramBadRequest) as e:
            # User blocked the bot or chat not found
            fail_count += 1
            logger.debug("Failed sending to user %s: %s", uid, e)
        except Exception as e:
            fail_count += 1
            logger.warning("Unexpected error during broadcast to %s: %s", uid, e)

        # Rate-limiting: sleep 0.05s between sends to avoid 429 Too Many Requests
        await asyncio.sleep(0.05)

        # Update progress report every 25 messages
        if idx % 25 == 0 or idx == total:
            try:
                await status_msg.edit_text(
                    f"⏳ <b>Broadcasting in progress...</b>\n{idx}/{total} processed.\n"
                    f"✅ Success: {success_count} | ❌ Failed/Blocked: {fail_count}",
                    parse_mode="HTML"
                )
            except Exception:
                pass

    summary = (
        f"📢 <b>Broadcast Completed!</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"👥 <b>Total Attempted:</b> {total}\n"
        f"✅ <b>Successfully Delivered:</b> {success_count}\n"
        f"❌ <b>Blocked or Failed:</b> {fail_count}\n"
        f"━━━━━━━━━━━━━━━━━━━━━"
    )
    await callback.message.answer(summary, reply_markup=get_admin_dashboard_keyboard(), parse_mode="HTML")
    await callback.answer()


# =========================================================================
# 8. BOT SETTINGS
# =========================================================================

@router.callback_query(F.data == "admin_bot_settings")
async def handle_admin_bot_settings(callback: CallbackQuery):
    """Displays core bot environment settings."""
    if not is_admin(callback.from_user.id):
        await callback.answer("🚫 Access denied.", show_alert=True)
        return

    all_settings = await db.get_all_settings()
    admin_count = len(ADMIN_IDS)

    text = (
        f"⚙️ <b>Bot System Settings</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"📁 <b>Database Path:</b> <code>{DATABASE_PATH}</code>\n"
        f"👑 <b>Authorized Admins:</b> {admin_count}\n"
        f"🎁 <b>Referral Requirement:</b> {all_settings.get('referrals_per_reward', '2')} refs/reward\n"
        f"⚡ <b>Referral System Active:</b> {'Yes' if all_settings.get('referral_enabled') == '1' else 'No'}\n"
        f"🏆 <b>Reward Distribution:</b> {all_settings.get('reward_type', 'video').capitalize()}\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"<i>To modify bot token or admin IDs, update the .env file.</i>"
    )
    await callback.message.edit_text(text, reply_markup=get_admin_back_keyboard(), parse_mode="HTML")
    await callback.answer()

