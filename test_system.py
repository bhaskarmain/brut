"""
Automated System Verification Script.
Tests all database queries, referral rules, reward calculations, and video mechanics.
"""

import sys
import asyncio
import os
import shutil
from pathlib import Path

# Ensure UTF-8 output encoding on Windows consoles
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

# Use a test database
TEST_DB_PATH = "data/test_bot.db"
os.environ["DATABASE_PATH"] = TEST_DB_PATH
os.environ["BOT_TOKEN"] = "123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ"
os.environ["ADMIN_IDS"] = "111222333,999888777"

from database import Database
from services.video_service import VideoService
from services.referral_service import ReferralService
from config import is_admin


async def run_tests():
    print("=" * 60)
    print("🚀 STARTING SMART VIDEO BOT AUTOMATED TESTS")
    print("=" * 60)

    # Clean previous test database if exists
    if Path(TEST_DB_PATH).exists():
        Path(TEST_DB_PATH).unlink()

    test_db = Database(TEST_DB_PATH)
    await test_db.init_db()
    print("✅ 1. Database schema & indices created successfully.")

    # -------------------------------------------------------------
    # 2. Test Admin Check
    # -------------------------------------------------------------
    assert is_admin(111222333) is True
    assert is_admin(999888777) is True
    assert is_admin(555555555) is False
    print("✅ 2. Admin verification logic verified.")

    # -------------------------------------------------------------
    # 3. Test Categories
    # -------------------------------------------------------------
    cat_id1 = await test_db.add_category("Action", "💥")
    cat_id2 = await test_db.add_category("Comedy", "😂")
    assert cat_id1 is not None and cat_id2 is not None

    cats = await test_db.get_categories()
    assert len(cats) == 2
    assert cats[0]["name"] == "Action" and cats[0]["emoji"] == "💥"

    await test_db.update_category(cat_id1, "Action & Sci-Fi", "🚀")
    updated_cat = await test_db.get_category(cat_id1)
    assert updated_cat["name"] == "Action & Sci-Fi" and updated_cat["emoji"] == "🚀"
    print("✅ 3. Category creation, listing, and updates verified.")

    # -------------------------------------------------------------
    # 4. Test User Registration First (Satisfies foreign keys)
    # -------------------------------------------------------------
    # User 1001 registers (primary referrer)
    u1, is_new, ref_credited = await test_db.get_or_create_user(1001, "alex", "Alex", None, None)
    assert is_new is True and ref_credited is False

    # -------------------------------------------------------------
    # 5. Test Video Uploads and Viewing
    # -------------------------------------------------------------
    vid1 = await test_db.add_video(
        category_id=cat_id1,
        file_id="BAACAgIAAxkBAAIBY1...",
        file_unique_id="uniq_111",
        title="Top 10 Movie Stunts",
        description="Epic movie scenes"
    )
    vid2 = await test_db.add_video(
        category_id=cat_id1,
        file_id="BAACAgIAAxkBAAIBY2...",
        file_unique_id="uniq_222",
        title="Speed Car Chase",
        description="High speed thrill"
    )
    vid3 = await test_db.add_video(
        category_id=cat_id2,
        file_id="BAACAgIAAxkBAAIBY3...",
        file_unique_id="uniq_333",
        title="Funniest Fails 2026",
        description="Hilarious moments"
    )

    total_vids = await test_db.get_total_videos_count()
    assert total_vids == 3

    vids_cat1, cat1_total = await test_db.get_videos_by_category(cat_id1, limit=5, offset=0)
    assert cat1_total == 2
    assert len(vids_cat1) == 2

    # View record for registered user 1001
    await test_db.record_video_watch(user_id=1001, video_id=vid1, is_reward=0)
    watched_video = await test_db.get_video(vid1)
    assert watched_video["views_count"] == 1

    # Test random video by category (prioritizes unwatched vid2)
    rand_cat1 = await test_db.get_random_video_by_category(cat_id1, user_id=1001)
    assert rand_cat1 is not None
    assert rand_cat1["category_id"] == cat_id1
    assert rand_cat1["id"] == vid2
    print("✅ 4. Video upload, categorization, random by category, and view tracking verified.")

    # -------------------------------------------------------------
    # 6. Test Referral System & Anti-Cheat Rules
    # -------------------------------------------------------------

    # Rule A: Prevent self-referral
    u1_again, is_new, ref_credited = await test_db.get_or_create_user(1001, "alex", "Alex", None, referrer_id=1001)
    assert is_new is False and ref_credited is False

    # Rule B: Non-existent referrer
    u_ghost, is_new, ref_credited = await test_db.get_or_create_user(9999, "ghost", "Ghost", None, referrer_id=888888)
    assert is_new is True and ref_credited is False

    # Rule C: Genuine new user referral 1
    u2, is_new, ref_credited = await test_db.get_or_create_user(1002, "bob", "Bob", None, referrer_id=1001)
    assert is_new is True and ref_credited is True

    # Rule D: Prevent duplicate referral (if user 1002 clicks referral link again)
    u2_again, is_new, ref_credited = await test_db.get_or_create_user(1002, "bob", "Bob", None, referrer_id=1001)
    assert is_new is False and ref_credited is False

    # Check stats for User 1001: 1 referral
    stats1 = await test_db.get_referral_stats(1001)
    assert stats1["valid_referrals"] == 1
    assert stats1["unclaimed_rewards"] == 0
    assert stats1["referrals_until_next"] == 1

    # Genuine new user referral 2
    u3, is_new, ref_credited = await test_db.get_or_create_user(1003, "charlie", "Charlie", None, referrer_id=1001)
    assert is_new is True and ref_credited is True

    # Check stats for User 1001: 2 referrals -> 1 UNCLAIMED REWARD!
    stats2 = await test_db.get_referral_stats(1001)
    assert stats2["valid_referrals"] == 2
    assert stats2["total_rewards_earned"] == 1
    assert stats2["unclaimed_rewards"] == 1

    # Add 2 more referrals -> total 4 referrals -> 2 rewards!
    await test_db.get_or_create_user(1004, "david", "David", None, referrer_id=1001)
    await test_db.get_or_create_user(1005, "elena", "Elena", None, referrer_id=1001)

    stats4 = await test_db.get_referral_stats(1001)
    assert stats4["valid_referrals"] == 4
    assert stats4["total_rewards_earned"] == 2
    assert stats4["unclaimed_rewards"] == 2
    print("✅ 5. Referral anti-cheat (self-referral, duplicate prevention, non-existent referrers) and rewards calculation verified.")

    # -------------------------------------------------------------
    # 6. Test Atomic Reward Claims & Random Unwatched Video
    # -------------------------------------------------------------
    # User 1001 already watched vid1 above.
    # Claim 1: Should receive an unwatched video (either vid2 or vid3)
    success, claim1_vid, msg = await test_db.claim_reward_transaction(1001)
    assert success is True
    assert claim1_vid["id"] in [vid2, vid3]
    first_claimed_id = claim1_vid["id"]

    # Check unclaimed rewards now = 1
    stats_after_claim1 = await test_db.get_referral_stats(1001)
    assert stats_after_claim1["rewards_claimed"] == 1
    assert stats_after_claim1["unclaimed_rewards"] == 1

    # Claim 2: Must distribute the remaining unwatched video
    success, claim2_vid, msg = await test_db.claim_reward_transaction(1001)
    assert success is True
    assert claim2_vid["id"] in [vid2, vid3]
    assert claim2_vid["id"] != first_claimed_id  # Distributed different video!

    # Check unclaimed rewards now = 0
    stats_after_claim2 = await test_db.get_referral_stats(1001)
    assert stats_after_claim2["rewards_claimed"] == 2
    assert stats_after_claim2["unclaimed_rewards"] == 0

    # Claim 3: Should fail because 0 unclaimed rewards left!
    success, claim3_vid, msg = await test_db.claim_reward_transaction(1001)
    assert success is False
    assert "No unclaimed rewards" in msg
    print("✅ 6. Atomic reward claim, unique unwatched video selection, and claim limits verified.")

    # -------------------------------------------------------------
    # 7. Test Referral Leaderboard
    # -------------------------------------------------------------
    leaderboard = await test_db.get_referral_leaderboard(limit=5)
    assert len(leaderboard) >= 1
    assert leaderboard[0]["user_id"] == 1001
    assert leaderboard[0]["successful_referrals"] == 4
    print("✅ 7. Referral leaderboard verified.")

    # -------------------------------------------------------------
    # 8. Test Ban and Unban Functionality
    # -------------------------------------------------------------
    assert await test_db.is_user_banned(1002) is False
    await test_db.set_user_ban(1002, is_banned=True)
    assert await test_db.is_user_banned(1002) is True
    assert await test_db.get_banned_users_count() == 1

    await test_db.set_user_ban(1002, is_banned=False)
    assert await test_db.is_user_banned(1002) is False
    print("✅ 8. User ban/unban mechanism verified.")

    # -------------------------------------------------------------
    # 9. Test Bot Settings
    # -------------------------------------------------------------
    await test_db.set_setting("referrals_per_reward", "3")
    val = await test_db.get_setting("referrals_per_reward")
    assert val == "3"
    print("✅ 9. Bot settings storage and retrieval verified.")

    # Clean up test database
    if Path(TEST_DB_PATH).exists():
        Path(TEST_DB_PATH).unlink()

    print("=" * 60)
    print("🎉 ALL TESTS PASSED SUCCESSFULLY! 100% WORKING.")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(run_tests())
