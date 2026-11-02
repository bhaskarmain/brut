"""
Video and Category Service.
Handles business logic for category management, video uploads, browsing, and playback.
"""

from typing import List, Dict, Any, Optional, Tuple
from database import db


class VideoService:
    @staticmethod
    async def get_all_categories() -> List[Dict[str, Any]]:
        """Retrieve all categories with their video counts."""
        return await db.get_categories()

    @staticmethod
    async def get_category(category_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve a specific category."""
        return await db.get_category(category_id)

    @staticmethod
    async def create_category(name: str, emoji: str = "📁") -> int:
        """Create a new category."""
        return await db.add_category(name=name, emoji=emoji)

    @staticmethod
    async def update_category(category_id: int, name: str, emoji: str) -> bool:
        """Update category name and emoji."""
        return await db.update_category(category_id, name, emoji)

    @staticmethod
    async def delete_category(category_id: int) -> bool:
        """Delete category and its associated videos."""
        return await db.delete_category(category_id)

    @staticmethod
    async def add_video(
        category_id: int,
        file_id: str,
        file_unique_id: Optional[str],
        title: str,
        description: Optional[str] = None
    ) -> int:
        """Add a new video to a category."""
        return await db.add_video(
            category_id=category_id,
            file_id=file_id,
            file_unique_id=file_unique_id,
            title=title,
            description=description
        )

    @staticmethod
    async def get_video(video_id: int) -> Optional[Dict[str, Any]]:
        """Fetch video by ID with category info."""
        return await db.get_video(video_id)

    @staticmethod
    async def get_videos_by_category(
        category_id: int,
        page: int = 1,
        page_size: int = 5
    ) -> Tuple[List[Dict[str, Any]], int, int]:
        """
        Fetch paginated videos for a category.
        Returns: (videos_list, total_count, total_pages)
        """
        offset = (page - 1) * page_size
        videos, total_count = await db.get_videos_by_category(category_id, limit=page_size, offset=offset)
        total_pages = max(1, (total_count + page_size - 1) // page_size)
        return videos, total_count, total_pages

    @staticmethod
    async def get_all_videos_paginated(
        page: int = 1,
        page_size: int = 6
    ) -> Tuple[List[Dict[str, Any]], int, int]:
        """
        Fetch all videos in the system with pagination.
        Returns: (videos_list, total_count, total_pages)
        """
        offset = (page - 1) * page_size
        videos, total_count = await db.get_all_videos(limit=page_size, offset=offset)
        total_pages = max(1, (total_count + page_size - 1) // page_size)
        return videos, total_count, total_pages

    @staticmethod
    async def delete_video(video_id: int) -> bool:
        """Delete video by ID."""
        return await db.delete_video(video_id)

    @staticmethod
    async def update_video(video_id: int, title: str, description: Optional[str] = None) -> bool:
        """Update video title and description."""
        return await db.update_video(video_id, title, description)

    @staticmethod
    async def record_watch(user_id: int, video_id: int, is_reward: int = 0) -> None:
        """Record video view and update stats."""
        await db.record_video_watch(user_id, video_id, is_reward)

    @staticmethod
    async def get_random_video(user_id: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """Get random video, prioritizing unwatched videos for this user."""
        return await db.get_random_video(user_id)

    @staticmethod
    async def get_random_video_by_category(
        category_id: int, user_id: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        """Get random video from a category, prioritizing unwatched videos."""
        return await db.get_random_video_by_category(category_id, user_id)

    @staticmethod
    async def get_video_stats() -> Dict[str, int]:
        """Aggregate video, category, and view counts."""
        total_videos = await db.get_total_videos_count()
        total_views = await db.get_total_views_count()
        categories = await db.get_categories()
        return {
            "total_videos": total_videos,
            "total_categories": len(categories),
            "total_views": total_views
        }


video_service = VideoService()

