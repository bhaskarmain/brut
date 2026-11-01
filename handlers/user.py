"""
User panel message and callback handlers.
Handles /start with referral tracking, main menu, account profile, statistics, and help.
"""

import logging
from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from database import db
from services.referral_service import referral_service
from keyboards.user import (
    get_main_menu_keyboard,
    get_account_keyboard,
    get_help_keyboard,
    get_back_to_menu_keyboard
)

logger = logging.getLogger(__name__)
router = Router(name="user_router")


@router.message(CommandStart())
async def handle_start(message: Message, bot: Bot):
    """
    Handles /start command.
    Detects deep link referral code, creates user, notifies referrer,
    and displays the main dashboard.
    """
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name or "Friend"
    last_name = message.from_user.last_name

    # Check for referral payload in /start <payload>
    referrer_id = None
    args = message.text.split(maxsplit=1)
    if len(args) > 1:
        referrer_id = referral_service.parse_referrer_id(args[1])

    # Get or create user
    user, is_new, referral_credited = await db.get_or_create_user(
        user_id=user_id,
        username=username,
        first_name=first_name,
        last_name=last_name,
        referrer_id=referrer_id
    )

    # If this was a successful new referral, notify the referrer
    if is_new and referral_credited and referrer_id:
        try:
            ref_stats = await db.get_referral_stats(referrer_id)
            unclaimed = ref_stats["unclaimed_rewards"]
            until_next = ref_stats["referrals_until_next"]
            req = ref_stats["required_per_reward"]

            reward_alert = (
                f"\n\n🎁 <b>Awesome! You just unlocked a free video reward!</b> Tap /start and claim it now!"
                if unclaimed > 0 and (ref_stats["valid_referrals"] % req == 0)
                else f"\n\n🎯 <i>Only {until_next} more invite(s) to unlock your next free video reward!</i>"
            )

            await bot.send_message(
                chat_id=referrer_id,
                text=(
                    f"🎉 <b>New Referral Joined!</b>\n\n"
                    f"User <b>{first_name}</b> has joined the bot using your invitation link.\n"
                    f"• Total Valid Referrals: <b>{ref_stats['valid_referrals']}</b>"
                    f"{reward_alert}"
                ),
                parse_mode="HTML"
            )
        except Exception as e:
            logger.warning("Could not notify referrer %s: %s", referrer_id, e)

    welcome_text = (
        f"👋 <b>Welcome, {first_name}!</b>\n\n"
        f"🎬 <b>Smart Video Reward Bot</b> is your premium hub for discovering high-quality videos and earning rewards!\n\n"
        f"📌 <b>What you can do:</b>\n"
        f"• 📂 <b>Browse Categories:</b> Explore hand-picked video categories.\n"
        f"• 🎁 <b>Referral Rewards:</b> Invite friends & earn <b>1 free video every 2 referrals</b>!\n"
        f"• 📊 <b>Track Stats:</b> Monitor your views, referrals, and rewards.\n\n"
        f"Select an option below to get started 👇"
    )

    keyboard = get_main_menu_keyboard(user_id)
    await message.answer(welcome_text, reply_markup=keyboard, parse_mode="HTML")


@router.callback_query(F.data == "main_menu")
async def handle_main_menu_callback(callback: CallbackQuery):
    """Returns to the user main menu."""
    user_id = callback.from_user.id
    first_name = callback.from_user.first_name or "Friend"

    welcome_text = (
        f"👋 <b>Welcome back, {first_name}!</b>\n\n"
        f"🎬 <b>Smart Video Reward Bot</b>\n\n"
        f"Select an option below to browse videos or manage your account 👇"
    )
    keyboard = get_main_menu_keyboard(user_id)

    try:
        await callback.message.edit_text(welcome_text, reply_markup=keyboard, parse_mode="HTML")
    except TelegramBadRequest:
        # If the original message cannot be edited (e.g. was a video/photo), send a fresh message
        await callback.message.answer(welcome_text, reply_markup=keyboard, parse_mode="HTML")

    await callback.answer()


@router.callback_query(F.data == "my_account")
async def handle_my_account_callback(callback: CallbackQuery, bot: Bot):
    """Displays user profile, member details, and referral status."""
    user_id = callback.from_user.id
    bot_info = await bot.get_me()

    user = await db.get_user(user_id)
    watched_count = await db.get_user_watched_count(user_id)
    ref_stats = await db.get_referral_stats(user_id)
    referral_link = referral_service.build_referral_link(bot_info.username, user_id)

    name = callback.from_user.full_name or "Valued User"
    uname = f"@{callback.from_user.username}" if callback.from_user.username else "Not set"
    joined_date = user["joined_at"][:10] if user and user.get("joined_at") else "Today"

    text = (
        f"👤 <b>My Account Profile</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"🆔 <b>User ID:</b> <code>{user_id}</code>\n"
        f"👤 <b>Name:</b> {name}\n"
        f"🏷 <b>Username:</b> {uname}\n"
        f"📅 <b>Member Since:</b> {joined_date}\n\n"
        f"🎬 <b>Videos Watched:</b> {watched_count}\n"
        f"👥 <b>Successful Referrals:</b> {ref_stats['valid_referrals']}\n"
        f"🎁 <b>Rewards Claimed:</b> {ref_stats['rewards_claimed']}\n"
        f"⏳ <b>Unclaimed Rewards:</b> {ref_stats['unclaimed_rewards']}\n\n"
        f"🔗 <b>Your Referral Link:</b>\n"
        f"<code>{referral_link}</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"<i>Tip: Tap the link above to copy it automatically!</i>"
    )

    try:
        await callback.message.edit_text(text, reply_markup=get_account_keyboard(), parse_mode="HTML")
    except TelegramBadRequest:
        await callback.message.answer(text, reply_markup=get_account_keyboard(), parse_mode="HTML")

    await callback.answer()


@router.callback_query(F.data == "my_statistics")
async def handle_my_statistics_callback(callback: CallbackQuery):
    """Displays user's personal activity statistics."""
    user_id = callback.from_user.id
    watched_count = await db.get_user_watched_count(user_id)
    ref_stats = await db.get_referral_stats(user_id)

    text = (
        f"📊 <b>My Personal Statistics</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"🎬 <b>Videos Watched:</b> {watched_count}\n"
        f"👥 <b>Invited Friends:</b> {ref_stats['total_referrals']}\n"
        f"✅ <b>Successful Referrals:</b> {ref_stats['valid_referrals']}\n"
        f"🏆 <b>Total Video Rewards Earned:</b> {ref_stats['total_rewards_earned']}\n"
        f"🎁 <b>Claimed Rewards:</b> {ref_stats['rewards_claimed']}\n"
        f"✨ <b>Available to Claim:</b> {ref_stats['unclaimed_rewards']}\n"
        f"🎯 <b>Next Reward In:</b> {ref_stats['referrals_until_next']} more invite(s)\n\n"
        f"⚡ <b>Account Status:</b> 🟢 Active & In Good Standing\n"
        f"━━━━━━━━━━━━━━━━━━━━━"
    )

    try:
        await callback.message.edit_text(text, reply_markup=get_account_keyboard(), parse_mode="HTML")
    except TelegramBadRequest:
        await callback.message.answer(text, reply_markup=get_account_keyboard(), parse_mode="HTML")

    await callback.answer()


@router.callback_query(F.data == "help_menu")
async def handle_help_callback(callback: CallbackQuery):
    """Displays detailed help and usage guide."""
    help_text = (
        f"ℹ️ <b>Bot Help & Guidelines</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"<b>1. How to Watch Videos:</b>\n"
        f"Tap <b>📂 Browse Categories</b> or <b>🎬 Watch Videos</b> from the main menu, pick a category, and choose any video to stream it directly in Telegram.\n\n"
        f"<b>2. How to Earn Free Video Rewards:</b>\n"
        f"• Open <b>🎁 Referral Rewards</b> and copy your personal link.\n"
        f"• Share your link with friends or channels.\n"
        f"• For every <b>2 genuine new users</b> who join via your link, you unlock <b>1 free exclusive video reward</b>!\n"
        f"• The rewards are <b>unlimited</b>: 4 referrals = 2 videos, 6 referrals = 3 videos, etc.\n\n"
        f"<b>3. Rules & Fair Play:</b>\n"
        f"• Self-referrals and duplicate accounts are strictly blocked.\n"
        f"• Fake accounts will result in account suspension.\n\n"
        f"<b>4. Need Assistance?</b>\n"
        f"If you encounter any issues or want to report a broken video, contact an administrator."
    )

    try:
        await callback.message.edit_text(help_text, reply_markup=get_help_keyboard(), parse_mode="HTML")
    except TelegramBadRequest:
        await callback.message.answer(help_text, reply_markup=get_help_keyboard(), parse_mode="HTML")

    await callback.answer()


@router.callback_query(F.data == "noop")
async def handle_noop(callback: CallbackQuery):
    """Handles inert pagination counters."""
    await callback.answer()

