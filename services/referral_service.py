"""
Referral Reward Service.
Handles referral tracking, rewards calculation, anti-cheat validation, and reward claims.
"""

from typing import Dict, Any, Optional, Tuple, List
from database import db


class ReferralService:
    @staticmethod
    def parse_referrer_id(payload: Optional[str]) -> Optional[int]:
        """
        Parses referrer user ID from start payload.
        Supports formats:
        - "ref_12345678"
        - "ref12345678"
        - "12345678"
        """
        if not payload:
            return None

        clean_payload = payload.strip()
        if clean_payload.startswith("ref_"):
            clean_payload = clean_payload[4:]
        elif clean_payload.startswith("ref"):
            clean_payload = clean_payload[3:]

        if clean_payload.isdigit():
            return int(clean_payload)
        return None

    @staticmethod
    def build_referral_link(bot_username: str, user_id: int) -> str:
        """Constructs unique referral link."""
        return f"https://t.me/{bot_username}?start=ref_{user_id}"

    @staticmethod
    async def get_dashboard_data(user_id: int, bot_username: str) -> Dict[str, Any]:
        """
        Retrieves all dashboard metrics for the user:
        - Total referrals
        - Successful referrals
        - Unclaimed rewards
        - Total videos earned
        - Personal referral link
        """
        stats = await db.get_referral_stats(user_id)
        referral_link = ReferralService.build_referral_link(bot_username, user_id)

        # Check if referral system is enabled
        ref_enabled_str = await db.get_setting("referral_enabled", "1")
        is_enabled = ref_enabled_str == "1"

        return {
            **stats,
            "referral_link": referral_link,
            "is_enabled": is_enabled
        }

    @staticmethod
    async def claim_reward(user_id: int) -> Tuple[bool, Optional[Dict[str, Any]], str]:
        """
        Processes reward claim atomically.
        Returns: (success, video_dict_or_none, message)
        """
        # Check if referral rewards are currently enabled
        ref_enabled_str = await db.get_setting("referral_enabled", "1")
        if ref_enabled_str != "1":
            return False, None, "⚠️ Referral rewards are temporarily disabled by the administrator."

        return await db.claim_reward_transaction(user_id)

    @staticmethod
    async def get_leaderboard(limit: int = 10) -> List[Dict[str, Any]]:
        """Fetch top referrers leaderboard."""
        return await db.get_referral_leaderboard(limit)

    @staticmethod
    async def update_requirement(new_req: int) -> None:
        """Set new referral requirement per reward."""
        if new_req < 1:
            new_req = 1
        await db.set_setting("referrals_per_reward", str(new_req))

    @staticmethod
    async def toggle_referral_system(enable: bool) -> None:
        """Enable or disable referral rewards system."""
        await db.set_setting("referral_enabled", "1" if enable else "0")

    @staticmethod
    async def get_system_settings() -> Dict[str, Any]:
        """Get referral system settings."""
        req_str = await db.get_setting("referrals_per_reward", "2")
        enabled_str = await db.get_setting("referral_enabled", "1")
        reward_type = await db.get_setting("reward_type", "video")
        return {
            "required_per_reward": int(req_str) if req_str.isdigit() else 2,
            "is_enabled": enabled_str == "1",
            "reward_type": reward_type
        }


referral_service = ReferralService()

