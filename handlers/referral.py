"""
Referral system handlers.
Referral dashboard, automated reward calculation, atomic claims, and leaderboard.
"""

import logging
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from database import db
from services.referral_service import referral_service
from keyboards.user import (
    get_referral_dashboard_keyboard,
    get_leaderboard_keyboard,
    get_video_player_keyboard,
    get_back_to_menu_keyboard
)

logger = logging.getLogger(__name__)
router = Router(name="referral_router")


@router.callback_query(F.data == "referral_dashboard")
async def handle_referral_dashboard(callback: CallbackQuery, bot: Bot):
    """
    Displays personal referral dashboard with real-time counters,
    referral link, and claim button when rewards are ready.
    """
    user_id = callback.from_user.id
    bot_info = await bot.get_me()

    dashboard = await referral_service.get_dashboard_data(user_id, bot_info.username)

    status_badge = "🟢 Active" if dashboard["is_enabled"] else "🔴 Paused by Admin"
    req = dashboard["required_per_reward"]
    unclaimed = dashboard["unclaimed_rewards"]

    claim_banner = ""
    if unclaimed > 0:
        claim_banner = (
            f"🎁 <b>YOU HAVE {unclaimed} UNCLAIMED REWARD(S)!</b>\n"
            f"<i>Tap the 'Claim Free Video Reward' button below!</i>\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
        )

    text = (
        f"🎁 <b>Referral Rewards Dashboard</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"{claim_banner}"
        f"👥 <b>Total Invited:</b> {dashboard['total_referrals']}\n"
        f"✅ <b>Successful Referrals:</b> {dashboard['valid_referrals']}\n"
        f"🏆 <b>Total Videos Earned:</b> {dashboard['total_rewards_earned']}\n"
        f"🎁 <b>Rewards Claimed:</b> {dashboard['rewards_claimed']}\n"
        f"⏳ <b>Unclaimed Rewards:</b> <b>{unclaimed}</b>\n"
        f"🎯 <b>Next Reward In:</b> {dashboard['referrals_until_next']} more referral(s)\n"
        f"⚡ <b>Program Status:</b> {status_badge}\n\n"
        f"📜 <b>Reward Rules:</b>\n"
        f"• <b>{req} Referrals</b> = <b>1 Free Random Video</b>\n"
        f"• <b>{req * 2} Referrals</b> = <b>2 Free Videos</b>\n"
        f"• <b>{req * 3} Referrals</b> = <b>3 Free Videos</b>\n"
        f"• <i>No limits! Keep inviting to unlock unlimited videos!</i>\n\n"
        f"🔗 <b>Your Exclusive Referral Link:</b>\n"
        f"<code>{dashboard['referral_link']}</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"<i>Tip: Tap the link above to copy it to your clipboard.</i>"
    )

    keyboard = get_referral_dashboard_keyboard(
        unclaimed_rewards=unclaimed,
        referral_link=dashboard["referral_link"]
    )

    try:
        await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    except TelegramBadRequest:
        await callback.message.answer(text, reply_markup=keyboard, parse_mode="HTML")

    await callback.answer()


@router.callback_query(F.data == "claim_reward")
async def handle_claim_reward(callback: CallbackQuery, bot: Bot):
    """
    Atomically claims one free reward video and streams it to the user.
    """
    user_id = callback.from_user.id
    success, video, message = await referral_service.claim_reward(user_id)

    if not success or not video:
        await callback.answer(f"⚠️ {message}", show_alert=True)
        return

    await callback.answer("🎉 Reward verified! Sending your unlocked video...", show_alert=False)

    caption = (
        f"🎁 <b>FREE REFERRAL REWARD UNLOCKED!</b> 🏆\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"🎬 <b>{video['title']}</b>\n"
        f"📂 Category: {video.get('category_emoji', '📁')} {video.get('category_name', '')}\n\n"
        f"<i>{video.get('description') or 'Enjoy your exclusive reward video!'}</i>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"🎉 <i>Thank you for supporting our community by inviting friends!</i>"
    )

    try:
        await callback.message.answer_video(
            video=video["file_id"],
            caption=caption,
            parse_mode="HTML",
            reply_markup=get_video_player_keyboard(video["category_id"])
        )

        # Refresh dashboard message to update unclaimed count
        bot_info = await bot.get_me()
        dashboard = await referral_service.get_dashboard_data(user_id, bot_info.username)
        unclaimed = dashboard["unclaimed_rewards"]

        if unclaimed > 0:
            await callback.message.answer(
                f"✨ You still have <b>{unclaimed}</b> unclaimed reward(s) available!",
                reply_markup=get_referral_dashboard_keyboard(unclaimed, dashboard["referral_link"]),
                parse_mode="HTML"
            )
    except Exception as e:
        logger.error("Error distributing reward video %s to user %s: %s", video.get("id"), user_id, e)
        await callback.message.answer(
            f"🎉 <b>Reward Claimed!</b>\n"
            f"Your reward was registered in the database, but video streaming encountered a network issue: {e}",
            reply_markup=get_back_to_menu_keyboard(),
            parse_mode="HTML"
        )


@router.callback_query(F.data == "referral_leaderboard")
async def handle_referral_leaderboard(callback: CallbackQuery):
    """Displays top 10 referrers leaderboard."""
    leaderboard = await referral_service.get_leaderboard(limit=10)

    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    rows_text = []

    if not leaderboard:
        rows_text.append("<i>No referrals yet. Be the first to join the leaderboard!</i>")
    else:
        for idx, entry in enumerate(leaderboard):
            medal = medals[idx] if idx < len(medals) else f"#{idx+1}"
            name = entry.get("first_name") or entry.get("username") or f"User {entry['user_id']}"
            refs = entry.get("successful_referrals", 0)
            claimed = entry.get("rewards_claimed", 0)
            rows_text.append(f"{medal} <b>{name[:20]}</b> — <b>{refs}</b> refs | <b>{claimed}</b> rewards")

    text = (
        f"🏆 <b>Top Referral Leaderboard</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        + "\n".join(rows_text) +
        f"\n━━━━━━━━━━━━━━━━━━━━━\n"
        f"<i>Invite more friends to climb the leaderboard!</i>"
    )

    try:
        await callback.message.edit_text(text, reply_markup=get_leaderboard_keyboard(), parse_mode="HTML")
    except TelegramBadRequest:
        await callback.message.answer(text, reply_markup=get_leaderboard_keyboard(), parse_mode="HTML")

    await callback.answer()

