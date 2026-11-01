"""
Video browsing, category navigation, and video playback handlers.
Direct Telegram video streaming and view tracking.
"""

import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from services.video_service import video_service
from keyboards.user import (
    get_categories_keyboard,
    get_category_videos_keyboard,
    get_video_view_keyboard,
    get_video_player_keyboard,
    get_back_to_menu_keyboard
)

logger = logging.getLogger(__name__)
router = Router(name="videos_router")


@router.callback_query(F.data.in_({"watch_videos_menu", "browse_categories"}))
async def handle_browse_categories(callback: CallbackQuery):
    """Displays all available video categories."""
    categories = await video_service.get_all_categories()

    if not categories:
        text = (
            "📂 <b>Video Categories</b>\n\n"
            "Currently, there are no categories available.\n"
            "Our administrators are uploading new content. Please check back soon!"
        )
        try:
            await callback.message.edit_text(text, reply_markup=get_back_to_menu_keyboard(), parse_mode="HTML")
        except TelegramBadRequest:
            await callback.message.answer(text, reply_markup=get_back_to_menu_keyboard(), parse_mode="HTML")
        await callback.answer()
        return

    text = (
        "📂 <b>Browse Video Categories</b>\n\n"
        "Select a category below to explore available videos or hit <b>Surprise Me</b> for a random pick 👇"
    )
    keyboard = get_categories_keyboard(categories)

    try:
        await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    except TelegramBadRequest:
        await callback.message.answer(text, reply_markup=keyboard, parse_mode="HTML")

    await callback.answer()


@router.callback_query(F.data.startswith("cat_"))
async def handle_category_videos(callback: CallbackQuery):
    """
    Displays paginated list of videos inside a selected category.
    Callback pattern: cat_{category_id}_{page}
    """
    parts = callback.data.split("_")
    if len(parts) < 3:
        await callback.answer("Invalid request.")
        return

    category_id = int(parts[1])
    page = int(parts[2])

    category = await video_service.get_category(category_id)
    if not category:
        await callback.answer("⚠️ Category not found.", show_alert=True)
        return

    videos, total_count, total_pages = await video_service.get_videos_by_category(
        category_id=category_id,
        page=page,
        page_size=6
    )

    cat_emoji = category.get("emoji", "📁")
    cat_name = category["name"]

    if not videos:
        text = (
            f"{cat_emoji} <b>{cat_name}</b>\n\n"
            f"This category doesn't have any videos uploaded yet.\n"
            f"Check back soon or explore other categories!"
        )
        try:
            await callback.message.edit_text(text, reply_markup=get_categories_keyboard(await video_service.get_all_categories()), parse_mode="HTML")
        except TelegramBadRequest:
            await callback.message.answer(text, reply_markup=get_categories_keyboard(await video_service.get_all_categories()), parse_mode="HTML")
        await callback.answer()
        return

    text = (
        f"{cat_emoji} <b>{cat_name}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"Total Videos: <b>{total_count}</b> | Page: <b>{page}/{total_pages}</b>\n\n"
        f"Select a video below to view details and stream 👇"
    )
    keyboard = get_category_videos_keyboard(
        category_id=category_id,
        videos=videos,
        page=page,
        total_pages=total_pages
    )

    try:
        await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    except TelegramBadRequest:
        await callback.message.answer(text, reply_markup=keyboard, parse_mode="HTML")

    await callback.answer()


@router.callback_query(F.data.startswith("show_vid_"))
async def handle_show_video_details(callback: CallbackQuery):
    """
    Displays preview details of a specific video.
    Callback pattern: show_vid_{video_id}
    """
    video_id = int(callback.data.split("_")[2])
    video = await video_service.get_video(video_id)

    if not video:
        await callback.answer("⚠️ Video not found or has been removed.", show_alert=True)
        return

    cat_emoji = video.get("category_emoji", "📁")
    cat_name = video.get("category_name", "General")
    views = video.get("views_count", 0)
    desc = video.get("description") or "No description provided."

    text = (
        f"🎬 <b>{video['title']}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"📂 <b>Category:</b> {cat_emoji} {cat_name}\n"
        f"👁 <b>Total Views:</b> {views}\n\n"
        f"📝 <b>Description:</b>\n"
        f"<i>{desc}</i>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"Tap <b>▶️ Watch Now</b> to stream this video directly in Telegram!"
    )
    keyboard = get_video_view_keyboard(video_id=video_id, category_id=video["category_id"])

    try:
        await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    except TelegramBadRequest:
        await callback.message.answer(text, reply_markup=keyboard, parse_mode="HTML")

    await callback.answer()


@router.callback_query(F.data.startswith("play_vid_"))
async def handle_play_video(callback: CallbackQuery):
    """
    Streams the video directly to the user in Telegram.
    Increments view count and records watch history.
    Callback pattern: play_vid_{video_id}
    """
    video_id = int(callback.data.split("_")[2])
    video = await video_service.get_video(video_id)

    if not video:
        await callback.answer("⚠️ Video not found or removed.", show_alert=True)
        return

    user_id = callback.from_user.id
    caption = (
        f"🎬 <b>{video['title']}</b>\n"
        f"📂 Category: {video.get('category_emoji', '📁')} {video.get('category_name', '')}\n\n"
        f"<i>{video.get('description') or ''}</i>"
    )

    await callback.answer("⏳ Sending video...")

    try:
        await callback.message.answer_video(
            video=video["file_id"],
            caption=caption,
            parse_mode="HTML",
            reply_markup=get_video_player_keyboard(video["category_id"])
        )
        # Record watch event in background
        await video_service.record_watch(user_id=user_id, video_id=video_id, is_reward=0)
    except Exception as e:
        logger.error("Error streaming video %s to user %s: %s", video_id, user_id, e)
        await callback.message.answer(
            "⚠️ Unable to stream video at this moment. The video file may be inaccessible.",
            reply_markup=get_back_to_menu_keyboard()
        )


@router.callback_query(F.data == "watch_random")
async def handle_watch_random(callback: CallbackQuery):
    """
    Selects a random unwatched video and streams it to the user.
    """
    user_id = callback.from_user.id
    video = await video_service.get_random_video(user_id=user_id)

    if not video:
        await callback.answer("⚠️ No videos available in the library yet.", show_alert=True)
        return

    await callback.answer("🎲 Picking a surprise video for you...")

    caption = (
        f"🎲 <b>Surprise Video Pick:</b>\n"
        f"🎬 <b>{video['title']}</b>\n"
        f"📂 Category: {video.get('category_emoji', '📁')} {video.get('category_name', '')}\n\n"
        f"<i>{video.get('description') or ''}</i>"
    )

    try:
        await callback.message.answer_video(
            video=video["file_id"],
            caption=caption,
            parse_mode="HTML",
            reply_markup=get_video_player_keyboard(video["category_id"])
        )
        await video_service.record_watch(user_id=user_id, video_id=video["id"], is_reward=0)
    except Exception as e:
        logger.error("Error streaming random video %s: %s", video.get("id"), e)
        await callback.message.answer(
            "⚠️ Unable to stream video. Please choose from categories directly.",
            reply_markup=get_back_to_menu_keyboard()
        )

