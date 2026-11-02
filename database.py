"""
Database layer for Smart Video Reward Telegram Bot.
Uses aiosqlite for non-blocking asynchronous database operations.
"""

import aiosqlite
from contextlib import asynccontextmanager
from typing import Optional, List, Dict, Any, Tuple, AsyncGenerator
import datetime
from config import DATABASE_PATH, DEFAULT_REFERRALS_PER_REWARD, DEFAULT_REFERRAL_ENABLED


class Database:
    def __init__(self, db_path: str = DATABASE_PATH):
        self.db_path = db_path

    @asynccontextmanager
    async def connect(self) -> AsyncGenerator[aiosqlite.Connection, None]:
        """Async context manager that yields a connection with foreign keys and row_factory enabled."""
        async with aiosqlite.connect(self.db_path) as conn:
            conn.row_factory = aiosqlite.Row
            await conn.execute("PRAGMA foreign_keys = ON;")
            yield conn

    async def init_db(self) -> None:
        """Initialize database schema, tables, indices, and default settings."""
        async with self.connect() as conn:
            # Users table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    referrer_id INTEGER,
                    is_banned INTEGER DEFAULT 0,
                    rewards_claimed INTEGER DEFAULT 0,
                    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (referrer_id) REFERENCES users(user_id) ON DELETE SET NULL
                );
            """)

            # Categories table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    emoji TEXT DEFAULT '📁',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # Videos table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS videos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_id INTEGER NOT NULL,
                    file_id TEXT NOT NULL,
                    file_unique_id TEXT,
                    title TEXT NOT NULL,
                    description TEXT,
                    views_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
                );
            """)

            # Watched / Distributed videos table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS watched_videos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    video_id INTEGER NOT NULL,
                    is_reward INTEGER DEFAULT 0,
                    watched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                    FOREIGN KEY (video_id) REFERENCES videos(id) ON DELETE CASCADE
                );
            """)

            # Referrals history table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS referrals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    referrer_id INTEGER NOT NULL,
                    referred_id INTEGER NOT NULL UNIQUE,
                    status TEXT DEFAULT 'valid',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (referrer_id) REFERENCES users(user_id) ON DELETE CASCADE,
                    FOREIGN KEY (referred_id) REFERENCES users(user_id) ON DELETE CASCADE
                );
            """)

            # Bot Settings key-value table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS bot_settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                );
            """)

            # Create indices for high performance queries
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_users_referrer ON users(referrer_id);")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_videos_category ON videos(category_id);")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_watched_user_vid ON watched_videos(user_id, video_id);")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_referrals_referrer ON referrals(referrer_id);")

            # Seed default settings if not exists
            default_settings = [
                ("referrals_per_reward", str(DEFAULT_REFERRALS_PER_REWARD)),
                ("referral_enabled", str(DEFAULT_REFERRAL_ENABLED)),
                ("reward_type", "video"),
                ("welcome_text", "Welcome to Smart Video Bot! Browse top categories or invite friends to unlock exclusive video rewards!")
            ]
            for key, val in default_settings:
                await conn.execute("""
                    INSERT OR IGNORE INTO bot_settings (key, value) VALUES (?, ?)
                """, (key, val))

            # Commit schema
            await conn.commit()

    # =========================================================================
    # USER OPERATIONS
    # =========================================================================

    async def get_or_create_user(
        self,
        user_id: int,
        username: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        referrer_id: Optional[int] = None
    ) -> Tuple[Dict[str, Any], bool, bool]:
        """
        Retrieves existing user or creates a new one.
        Handles referral relationship if valid.
        Returns: (user_dict, is_new_user, referral_credited)
        """
        async with self.connect() as conn:
            cursor = await conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            row = await cursor.fetchone()

            if row:
                # User already exists - update name/activity timestamp
                await conn.execute("""
                    UPDATE users
                    SET username = ?, first_name = ?, last_name = ?, last_active = CURRENT_TIMESTAMP
                    WHERE user_id = ?
                """, (username, first_name, last_name, user_id))
                await conn.commit()
                return dict(row), False, False

            # New user registration
            is_referral_valid = False
            valid_referrer_id = None

            # Validate referral:
            # 1. referrer_id must be provided
            # 2. Cannot refer self
            if referrer_id and referrer_id != user_id:
                # 3. Referrer must exist in database
                ref_cur = await conn.execute("SELECT user_id, is_banned FROM users WHERE user_id = ?", (referrer_id,))
                referrer_row = await ref_cur.fetchone()
                if referrer_row and not referrer_row["is_banned"]:
                    # Check referral setting is enabled
                    setting_cur = await conn.execute("SELECT value FROM bot_settings WHERE key = 'referral_enabled'")
                    setting_row = await setting_cur.fetchone()
                    ref_enabled = setting_row["value"] == "1" if setting_row else True

                    if ref_enabled:
                        valid_referrer_id = referrer_id
                        is_referral_valid = True

            # Insert new user
            await conn.execute("""
                INSERT INTO users (user_id, username, first_name, last_name, referrer_id)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, username, first_name, last_name, valid_referrer_id))

            # If referral is valid, record in referrals table
            if is_referral_valid and valid_referrer_id:
                await conn.execute("""
                    INSERT OR IGNORE INTO referrals (referrer_id, referred_id, status)
                    VALUES (?, ?, 'valid')
                """, (valid_referrer_id, user_id))

            await conn.commit()

            cursor = await conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            new_row = await cursor.fetchone()
            return dict(new_row), True, is_referral_valid

    async def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Fetch user by Telegram ID."""
        async with self.connect() as conn:
            cursor = await conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            row = await cursor.fetchone()
            return dict(row) if row else None

    async def update_user_activity(self, user_id: int) -> None:
        """Update user last active timestamp."""
        async with self.connect() as conn:
            await conn.execute("UPDATE users SET last_active = CURRENT_TIMESTAMP WHERE user_id = ?", (user_id,))
            await conn.commit()

    async def set_user_ban(self, user_id: int, is_banned: bool) -> bool:
        """Ban or unban a user. Returns True if user found and updated."""
        async with self.connect() as conn:
            cursor = await conn.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
            if not await cursor.fetchone():
                return False
            await conn.execute("UPDATE users SET is_banned = ? WHERE user_id = ?", (1 if is_banned else 0, user_id))
            await conn.commit()
            return True

    async def is_user_banned(self, user_id: int) -> bool:
        """Check if user is banned."""
        async with self.connect() as conn:
            cursor = await conn.execute("SELECT is_banned FROM users WHERE user_id = ?", (user_id,))
            row = await cursor.fetchone()
            return bool(row["is_banned"]) if row else False

    async def get_all_user_ids(self) -> List[int]:
        """Fetch all non-banned user IDs for broadcasting."""
        async with self.connect() as conn:
            cursor = await conn.execute("SELECT user_id FROM users WHERE is_banned = 0")
            rows = await cursor.fetchall()
            return [row["user_id"] for row in rows]

    async def get_users_list(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """Get paginated list of users."""
        async with self.connect() as conn:
            cursor = await conn.execute("""
                SELECT u.*, 
                       (SELECT COUNT(*) FROM referrals r WHERE r.referrer_id = u.user_id AND r.status = 'valid') AS referral_count,
                       (SELECT COUNT(*) FROM watched_videos w WHERE w.user_id = u.user_id) AS watched_count
                FROM users u
                ORDER BY u.joined_at DESC
                LIMIT ? OFFSET ?
            """, (limit, offset))
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]

    async def get_total_users_count(self) -> int:
        """Get total count of users registered."""
        async with self.connect() as conn:
            cursor = await conn.execute("SELECT COUNT(*) AS total FROM users")
            row = await cursor.fetchone()
            return row["total"] if row else 0

    async def get_banned_users_count(self) -> int:
        """Get count of banned users."""
        async with self.connect() as conn:
            cursor = await conn.execute("SELECT COUNT(*) AS total FROM users WHERE is_banned = 1")
            row = await cursor.fetchone()
            return row["total"] if row else 0

    async def get_active_users_24h_count(self) -> int:
        """Get count of users active within the last 24 hours."""
        async with self.connect() as conn:
            cursor = await conn.execute("""
                SELECT COUNT(*) AS total FROM users 
                WHERE last_active >= datetime('now', '-1 day')
            """)
            row = await cursor.fetchone()
            return row["total"] if row else 0

    # =========================================================================
    # REFERRAL OPERATIONS
    # =========================================================================

    async def get_referral_stats(self, user_id: int) -> Dict[str, Any]:
        """
        Calculate total referrals, successful referrals, rewards claimed,
        and unclaimed reward count for a given user.
        """
        async with self.connect() as conn:
            # Get user info
            u_cur = await conn.execute("SELECT rewards_claimed FROM users WHERE user_id = ?", (user_id,))
            u_row = await u_cur.fetchone()
            rewards_claimed = u_row["rewards_claimed"] if u_row else 0

            # Get total referrals count
            r_cur = await conn.execute("""
                SELECT 
                    COUNT(*) AS total_referrals,
                    SUM(CASE WHEN status = 'valid' THEN 1 ELSE 0 END) AS valid_referrals
                FROM referrals
                WHERE referrer_id = ?
            """, (user_id,))
            r_row = await r_cur.fetchone()
            total_referrals = r_row["total_referrals"] if r_row and r_row["total_referrals"] else 0
            valid_referrals = r_row["valid_referrals"] if r_row and r_row["valid_referrals"] else 0

            # Get setting: referrals required per reward
            s_cur = await conn.execute("SELECT value FROM bot_settings WHERE key = 'referrals_per_reward'")
            s_row = await s_cur.fetchone()
            req_per_reward = int(s_row["value"]) if s_row and s_row["value"].isdigit() else DEFAULT_REFERRALS_PER_REWARD
            if req_per_reward < 1:
                req_per_reward = 1

            # Total rewards earned based on valid referrals
            total_rewards_earned = valid_referrals // req_per_reward
            unclaimed_rewards = max(0, total_rewards_earned - rewards_claimed)
            referrals_until_next = req_per_reward - (valid_referrals % req_per_reward)

            return {
                "total_referrals": total_referrals,
                "valid_referrals": valid_referrals,
                "required_per_reward": req_per_reward,
                "total_rewards_earned": total_rewards_earned,
                "rewards_claimed": rewards_claimed,
                "unclaimed_rewards": unclaimed_rewards,
                "referrals_until_next": referrals_until_next
            }

    async def claim_reward_transaction(self, user_id: int) -> Tuple[bool, Optional[Dict[str, Any]], str]:
        """
        Atomically claim 1 reward:
        1. Checks unclaimed reward balance inside a transaction.
        2. Finds an eligible random video (prioritizing unwatched).
        3. Records reward in watched_videos.
        4. Increments rewards_claimed.
        Returns: (success, video_dict_or_none, message)
        """
        async with self.connect() as conn:
            try:
                await conn.execute("BEGIN TRANSACTION;")

                # Check user exists and get claimed
                u_cur = await conn.execute("SELECT rewards_claimed FROM users WHERE user_id = ?", (user_id,))
                u_row = await u_cur.fetchone()
                if not u_row:
                    await conn.execute("ROLLBACK;")
                    return False, None, "User not found."

                rewards_claimed = u_row["rewards_claimed"]

                # Check valid referrals
                r_cur = await conn.execute("""
                    SELECT COUNT(*) as valid_cnt FROM referrals 
                    WHERE referrer_id = ? AND status = 'valid'
                """, (user_id,))
                r_row = await r_cur.fetchone()
                valid_referrals = r_row["valid_cnt"] if r_row else 0

                # Get setting
                s_cur = await conn.execute("SELECT value FROM bot_settings WHERE key = 'referrals_per_reward'")
                s_row = await s_cur.fetchone()
                req = int(s_row["value"]) if s_row and s_row["value"].isdigit() else DEFAULT_REFERRALS_PER_REWARD

                total_rewards_earned = valid_referrals // req
                unclaimed = total_rewards_earned - rewards_claimed

                if unclaimed <= 0:
                    await conn.execute("ROLLBACK;")
                    return False, None, "No unclaimed rewards available."

                # Find unwatched video
                v_cur = await conn.execute("""
                    SELECT v.*, c.name as category_name, c.emoji as category_emoji
                    FROM videos v
                    JOIN categories c ON v.category_id = c.id
                    WHERE v.id NOT IN (
                        SELECT video_id FROM watched_videos WHERE user_id = ?
                    )
                    ORDER BY RANDOM()
                    LIMIT 1
                """, (user_id,))
                video_row = await v_cur.fetchone()

                # If user watched all videos, distribute any random video from library
                if not video_row:
                    v_all_cur = await conn.execute("""
                        SELECT v.*, c.name as category_name, c.emoji as category_emoji
                        FROM videos v
                        JOIN categories c ON v.category_id = c.id
                        ORDER BY RANDOM()
                        LIMIT 1
                    """)
                    video_row = await v_all_cur.fetchone()

                if not video_row:
                    await conn.execute("ROLLBACK;")
                    return False, None, "No videos are currently uploaded in the library. Contact admin!"

                video_dict = dict(video_row)
                video_id = video_dict["id"]

                # Record watched video as reward
                await conn.execute("""
                    INSERT INTO watched_videos (user_id, video_id, is_reward)
                    VALUES (?, ?, 1)
                """, (user_id, video_id))

                # Increment video view count
                await conn.execute("UPDATE videos SET views_count = views_count + 1 WHERE id = ?", (video_id,))

                # Increment user claimed count
                await conn.execute("UPDATE users SET rewards_claimed = rewards_claimed + 1 WHERE user_id = ?", (user_id,))

                await conn.commit()
                return True, video_dict, "Reward claimed successfully!"

            except Exception as e:
                await conn.execute("ROLLBACK;")
                return False, None, f"Database error: {str(e)}"

    async def get_referral_leaderboard(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top referrers by valid referral count."""
        async with self.connect() as conn:
            cursor = await conn.execute("""
                SELECT 
                    u.user_id,
                    u.first_name,
                    u.username,
                    u.rewards_claimed,
                    COUNT(r.id) AS successful_referrals
                FROM users u
                JOIN referrals r ON u.user_id = r.referrer_id AND r.status = 'valid'
                WHERE u.is_banned = 0
                GROUP BY u.user_id
                ORDER BY successful_referrals DESC
                LIMIT ?
            """, (limit,))
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]

    async def get_total_referrals_count(self) -> int:
        """Get total successful referrals across entire bot."""
        async with self.connect() as conn:
            cursor = await conn.execute("SELECT COUNT(*) AS total FROM referrals WHERE status = 'valid'")
            row = await cursor.fetchone()
            return row["total"] if row else 0

    # =========================================================================
    # CATEGORY OPERATIONS
    # =========================================================================

    async def add_category(self, name: str, emoji: str = "📁") -> int:
        """Add new category and return its ID."""
        async with self.connect() as conn:
            cursor = await conn.execute("""
                INSERT INTO categories (name, emoji) VALUES (?, ?)
            """, (name.strip(), emoji.strip()))
            await conn.commit()
            return cursor.lastrowid

    async def get_categories(self) -> List[Dict[str, Any]]:
        """Fetch all categories with video count."""
        async with self.connect() as conn:
            cursor = await conn.execute("""
                SELECT c.id, c.name, c.emoji, c.created_at,
                       COUNT(v.id) AS video_count
                FROM categories c
                LEFT JOIN videos v ON c.id = v.category_id
                GROUP BY c.id
                ORDER BY c.id ASC
            """)
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]

    async def get_category(self, category_id: int) -> Optional[Dict[str, Any]]:
        """Fetch a single category by ID."""
        async with self.connect() as conn:
            cursor = await conn.execute("SELECT * FROM categories WHERE id = ?", (category_id,))
            row = await cursor.fetchone()
            return dict(row) if row else None

    async def update_category(self, category_id: int, name: str, emoji: str) -> bool:
        """Update category name and emoji."""
        async with self.connect() as conn:
            cursor = await conn.execute("""
                UPDATE categories SET name = ?, emoji = ? WHERE id = ?
            """, (name.strip(), emoji.strip(), category_id))
            await conn.commit()
            return cursor.rowcount > 0

    async def delete_category(self, category_id: int) -> bool:
        """Delete category and cascade delete its videos."""
        async with self.connect() as conn:
            cursor = await conn.execute("DELETE FROM categories WHERE id = ?", (category_id,))
            await conn.commit()
            return cursor.rowcount > 0

    # =========================================================================
    # VIDEO OPERATIONS
    # =========================================================================

    async def add_video(
        self,
        category_id: int,
        file_id: str,
        file_unique_id: Optional[str],
        title: str,
        description: Optional[str] = None
    ) -> int:
        """Insert uploaded video details."""
        async with self.connect() as conn:
            cursor = await conn.execute("""
                INSERT INTO videos (category_id, file_id, file_unique_id, title, description)
                VALUES (?, ?, ?, ?, ?)
            """, (category_id, file_id, file_unique_id, title.strip(), description.strip() if description else None))
            await conn.commit()
            return cursor.lastrowid

    async def get_video(self, video_id: int) -> Optional[Dict[str, Any]]:
        """Fetch video by ID with category info."""
        async with self.connect() as conn:
            cursor = await conn.execute("""
                SELECT v.*, c.name AS category_name, c.emoji AS category_emoji
                FROM videos v
                JOIN categories c ON v.category_id = c.id
                WHERE v.id = ?
            """, (video_id,))
            row = await cursor.fetchone()
            return dict(row) if row else None

    async def get_videos_by_category(
        self,
        category_id: int,
        limit: int = 6,
        offset: int = 0
    ) -> Tuple[List[Dict[str, Any]], int]:
        """Fetch videos for a category with pagination. Returns (videos, total_count)."""
        async with self.connect() as conn:
            count_cur = await conn.execute("SELECT COUNT(*) AS total FROM videos WHERE category_id = ?", (category_id,))
            count_row = await count_cur.fetchone()
            total_count = count_row["total"] if count_row else 0

            cursor = await conn.execute("""
                SELECT * FROM videos 
                WHERE category_id = ?
                ORDER BY id DESC
                LIMIT ? OFFSET ?
            """, (category_id, limit, offset))
            rows = await cursor.fetchall()
            return [dict(r) for r in rows], total_count

    async def get_all_videos(self, limit: int = 10, offset: int = 0) -> Tuple[List[Dict[str, Any]], int]:
        """Fetch all videos with pagination."""
        async with self.connect() as conn:
            count_cur = await conn.execute("SELECT COUNT(*) AS total FROM videos")
            count_row = await count_cur.fetchone()
            total_count = count_row["total"] if count_row else 0

            cursor = await conn.execute("""
                SELECT v.*, c.name AS category_name, c.emoji AS category_emoji
                FROM videos v
                JOIN categories c ON v.category_id = c.id
                ORDER BY v.id DESC
                LIMIT ? OFFSET ?
            """, (limit, offset))
            rows = await cursor.fetchall()
            return [dict(r) for r in rows], total_count

    async def delete_video(self, video_id: int) -> bool:
        """Delete a video."""
        async with self.connect() as conn:
            cursor = await conn.execute("DELETE FROM videos WHERE id = ?", (video_id,))
            await conn.commit()
            return cursor.rowcount > 0

    async def update_video(self, video_id: int, title: str, description: Optional[str] = None) -> bool:
        """Update title and description of a video."""
        async with self.connect() as conn:
            cursor = await conn.execute("""
                UPDATE videos SET title = ?, description = ? WHERE id = ?
            """, (title.strip(), description.strip() if description else None, video_id))
            await conn.commit()
            return cursor.rowcount > 0

    async def record_video_watch(self, user_id: int, video_id: int, is_reward: int = 0) -> None:
        """Record video view and increment view count."""
        async with self.connect() as conn:
            await conn.execute("""
                INSERT INTO watched_videos (user_id, video_id, is_reward)
                VALUES (?, ?, ?)
            """, (user_id, video_id, is_reward))
            await conn.execute("UPDATE videos SET views_count = views_count + 1 WHERE id = ?", (video_id,))
            await conn.commit()

    async def get_user_watched_count(self, user_id: int) -> int:
        """Get count of videos watched by a user."""
        async with self.connect() as conn:
            cursor = await conn.execute("SELECT COUNT(*) AS total FROM watched_videos WHERE user_id = ?", (user_id,))
            row = await cursor.fetchone()
            return row["total"] if row else 0

    async def get_total_videos_count(self) -> int:
        """Get total count of videos in system."""
        async with self.connect() as conn:
            cursor = await conn.execute("SELECT COUNT(*) AS total FROM videos")
            row = await cursor.fetchone()
            return row["total"] if row else 0

    async def get_total_views_count(self) -> int:
        """Get sum of all video views."""
        async with self.connect() as conn:
            cursor = await conn.execute("SELECT COALESCE(SUM(views_count), 0) AS total FROM videos")
            row = await cursor.fetchone()
            return row["total"] if row else 0

    async def get_random_video(self, user_id: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """
        Get random video from library.
        If user_id provided, prioritizes unwatched videos.
        """
        async with self.connect() as conn:
            if user_id:
                cursor = await conn.execute("""
                    SELECT v.*, c.name AS category_name, c.emoji AS category_emoji
                    FROM videos v
                    JOIN categories c ON v.category_id = c.id
                    WHERE v.id NOT IN (
                        SELECT video_id FROM watched_videos WHERE user_id = ?
                    )
                    ORDER BY RANDOM()
                    LIMIT 1
                """, (user_id,))
                row = await cursor.fetchone()
                if row:
                    return dict(row)

            # Fallback to any random video
            cursor = await conn.execute("""
                SELECT v.*, c.name AS category_name, c.emoji AS category_emoji
                FROM videos v
                JOIN categories c ON v.category_id = c.id
                ORDER BY RANDOM()
                LIMIT 1
            """)
            row = await cursor.fetchone()
            return dict(row) if row else None

    async def get_random_video_by_category(
        self, category_id: int, user_id: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Get random video from a specific category.
        Prioritizes unwatched videos for this user.
        """
        async with self.connect() as conn:
            if user_id:
                cursor = await conn.execute("""
                    SELECT v.*, c.name AS category_name, c.emoji AS category_emoji
                    FROM videos v
                    JOIN categories c ON v.category_id = c.id
                    WHERE v.category_id = ? AND v.id NOT IN (
                        SELECT video_id FROM watched_videos WHERE user_id = ?
                    )
                    ORDER BY RANDOM()
                    LIMIT 1
                """, (category_id, user_id))
                row = await cursor.fetchone()
                if row:
                    return dict(row)

            # Fallback to any random video from that category
            cursor = await conn.execute("""
                SELECT v.*, c.name AS category_name, c.emoji AS category_emoji
                FROM videos v
                JOIN categories c ON v.category_id = c.id
                WHERE v.category_id = ?
                ORDER BY RANDOM()
                LIMIT 1
            """, (category_id,))
            row = await cursor.fetchone()
            return dict(row) if row else None

    # =========================================================================
    # SETTINGS OPERATIONS
    # =========================================================================

    async def get_setting(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Fetch a setting value by key."""
        async with self.connect() as conn:
            cursor = await conn.execute("SELECT value FROM bot_settings WHERE key = ?", (key,))
            row = await cursor.fetchone()
            return row["value"] if row else default

    async def set_setting(self, key: str, value: str) -> None:
        """Upsert a setting value."""
        async with self.connect() as conn:
            await conn.execute("""
                INSERT INTO bot_settings (key, value) VALUES (?, ?)
                ON CONFLICT(key) DO UPDATE SET value = excluded.value
            """, (key, str(value)))
            await conn.commit()

    async def get_all_settings(self) -> Dict[str, str]:
        """Get all settings as a dict."""
        async with self.connect() as conn:
            cursor = await conn.execute("SELECT key, value FROM bot_settings")
            rows = await cursor.fetchall()
            return {row["key"]: row["value"] for row in rows}


# Singleton database instance
db = Database()
