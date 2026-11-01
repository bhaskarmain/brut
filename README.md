# 🎬 Smart Video Reward Telegram Bot

A production-ready, asynchronous Telegram bot built with **Python 3.11+**, **aiogram 3.x**, and **SQLite**. Features an interactive **User Panel** with categorized video streaming, an automated **Referral Reward System** (every 2 successful referrals = 1 free random video reward), and a powerful **Admin Panel** with direct video upload, category management, user administration, broadcasting, and real-time statistics.

---

## 🌟 Key Features

### 👤 1. User Panel
- **Modern Inline UI:** Emoji-rich navigation with fluid back buttons.
- **Categorized Video Library:** Browse videos organized cleanly by category.
- **Direct Video Streaming:** Videos are delivered straight to Telegram chats via Telegram file IDs with zero server bandwidth load.
- **Smart Unwatched Distribution:** Avoids sending repeat videos until all available videos in the library have been watched.
- **Personal Statistics:** Track videos watched, invited friends, rewards earned, and account status.
- **Surprise Me / Random Mode:** Quick button to get an unwatched surprise video on demand.

### 🎁 2. Referral Reward System
- **Unique Referral Links:** Each user receives a dedicated link formatted as `https://t.me/<bot_username>?start=ref_<user_id>`.
- **Automated Reward Calculation:**
  - `2 Referrals` = 1 Free Random Video
  - `4 Referrals` = 2 Free Videos
  - `6 Referrals` = 3 Free Videos
  - `8 Referrals` = 4 Free Videos *(unlimited & repeatable)*
- **Interactive Referral Dashboard:**
  - Total referrals count
  - Successful (valid) referrals count
  - Unclaimed video rewards count
  - Next reward countdown tracker
  - One-tap "Claim Free Video Reward" button (visible when rewards are ready)
  - Native Telegram Share Link button
- **Anti-Cheat & Security:**
  - Prevents self-referral.
  - Prevents duplicate referrals (only genuine first-time users count).
  - Atomic database transactions ensure rewards cannot be double-claimed.
- **Referral Leaderboard:** Top referrers leaderboard with medals (🥇, 🥈, 🥉).

### 🛠 3. Admin Panel (Authorized Admins Only)
- **📤 Upload Video:** Guided FSM flow — select category, forward or send video file, enter title, and add description.
- **📂 Add Category:** Create categories with custom names and emojis.
- **✏️ Edit Category:** Rename, change emoji, or delete categories (with cascading video cleanup).
- **📋 Manage Videos:** Paginated catalog of all videos, view details, preview video, edit title, or delete.
- **👥 All Users:** Inspect registered users, view referral stats, and check activity.
- **🚫 Ban/Unban User:** Search by Telegram ID and instantly toggle ban status. Banned users are rejected via middleware.
- **📊 Bot Statistics:** Global real-time analytics (total users, active users in 24h, total videos, total views, total referrals).
- **🎁 Referral Settings:** Change referral requirement (e.g. 1, 2, 3, 5), toggle referral rewards on/off, and view leaderboard.
- **📢 Broadcast Message:** Send announcements (text, photo, or video) to all active users with live progress reports and rate-limiting.
- **⚙️ Bot Settings:** System overview and quick status check.

---

## 📁 Project Architecture

```
video-tg-bot/
├── bot.py                  # Bot bootstrap, dispatcher setup & polling loop
├── config.py               # Environment configuration & validation
├── database.py             # Asynchronous SQLite database layer (aiosqlite)
├── requirements.txt        # Python package dependencies
├── .env.example            # Environment variables template
├── .env                    # Your actual secrets (BOT_TOKEN, ADMIN_IDS)
├── README.md               # Complete documentation & guide
├── test_system.py          # Automated verification test suite
├── handlers/
│   ├── __init__.py
│   ├── user.py             # /start, main menu, account profile, help
│   ├── videos.py           # Category browsing, video details & playback
│   ├── referral.py         # Referral dashboard, reward claims & leaderboard
│   └── admin.py            # Complete admin control dashboard & FSM workflows
├── keyboards/
│   ├── __init__.py
│   ├── user.py             # User inline keyboards & navigation
│   └── admin.py            # Admin inline keyboards & actions
├── middlewares/
│   ├── __init__.py
│   └── auth.py             # Security & banned user check middleware
├── services/
│   ├── __init__.py
│   ├── video_service.py    # Business logic for videos & categories
│   └── referral_service.py # Business logic for referrals & claims
└── data/
    └── bot.db              # SQLite database storage (auto-created)
```

---

## 🚀 Setup & Installation Guide (Windows CMD)

Follow these step-by-step instructions to set up the bot from scratch on Windows.

### Step 1: Open Windows Command Prompt
Press `Win + R`, type `cmd`, and hit `Enter`. Navigate to your bot directory:
```cmd
cd "C:\Users\LENOVO\Downloads\video tg bot"
```

### Step 2: Create a Python Virtual Environment
Creating an isolated virtual environment is recommended to prevent dependency conflicts:
```cmd
python -m venv venv
```

Activate the virtual environment:
```cmd
venv\Scripts\activate
```
*(You will see `(venv)` appear at the start of your command prompt line).*

### Step 3: Install Required Packages
Install the required asynchronous dependencies:
```cmd
pip install -r requirements.txt
```

---

## 🤖 Obtaining Bot Token and Admin ID

### 1. How to Create a Telegram Bot and Get `BOT_TOKEN`:
1. Open Telegram and search for [@BotFather](https://t.me/BotFather).
2. Start a chat and send `/newbot`.
3. Follow the prompts:
   - Enter a **Display Name** for your bot (e.g. `Smart Video Hub`).
   - Enter a **Username** ending in `bot` (e.g. `MySmartVideoRewardBot`).
4. BotFather will provide an API HTTP Token:
   ```
   7123456789:AAHk8-1ExampleTokenStringGoesHere_xyz
   ```
   Copy this token.

### 2. How to Find Your Numeric Telegram Admin ID:
1. In Telegram, search for [@userinfobot](https://t.me/userinfobot) or [@raw_data_bot](https://t.me/raw_data_bot).
2. Press `/start`.
3. The bot will reply with your numeric ID (e.g. `123456789`). Copy this number.

---

## ⚙️ Configuration (`.env`)

1. Copy `.env.example` to create your active `.env` file:
   ```cmd
   copy .env.example .env
   ```
2. Open `.env` in Notepad or your preferred editor:
   ```cmd
   notepad .env
   ```
3. Set your token and admin ID:
   ```env
   # Your Telegram Bot Token from @BotFather
   BOT_TOKEN=7123456789:AAHk8-1ExampleTokenStringGoesHere_xyz

   # Your Telegram Admin ID (comma-separated if multiple admins)
   ADMIN_IDS=123456789

   # Database Storage Path (defaults to data/bot.db)
   DATABASE_PATH=data/bot.db

   # Referral System Defaults
   DEFAULT_REFERRALS_PER_REWARD=2
   DEFAULT_REFERRAL_ENABLED=1
   ```
4. Save the file and close Notepad.

---

## 🧪 Run Automated Tests

Before launching, run the included automated verification suite to verify database relationships, anti-cheat referral tracking, atomic reward claims, and video delivery logic:
```cmd
python test_system.py
```
Output:
```
============================================================
🚀 STARTING SMART VIDEO BOT AUTOMATED TESTS
============================================================
✅ 1. Database schema & indices created successfully.
✅ 2. Admin verification logic verified.
✅ 3. Category creation, listing, and updates verified.
✅ 4. Video upload, categorization, pagination, and view tracking verified.
✅ 5. Referral anti-cheat and rewards calculation verified.
✅ 6. Atomic reward claim, unique unwatched video selection, and claim limits verified.
✅ 7. Referral leaderboard verified.
✅ 8. User ban/unban mechanism verified.
✅ 9. Bot settings storage and retrieval verified.
============================================================
🎉 ALL TESTS PASSED SUCCESSFULLY! 100% WORKING.
============================================================
```

---

## ▶️ Running the Bot

Start the bot with:
```cmd
python bot.py
```

Console Output:
```
2026-11-01 18:25:00 [INFO] SmartVideoBot: Initializing Smart Video Reward Bot...
2026-11-01 18:25:00 [INFO] SmartVideoBot: Verifying and initializing database schema...
2026-11-01 18:25:00 [INFO] SmartVideoBot: Database schema initialized successfully.
============================================================
🤖 Bot Username: @MySmartVideoRewardBot
👑 Authorized Admin IDs: [123456789]
⚡ Bot is running and polling for updates... Press Ctrl+C to stop.
============================================================
```

Now open Telegram, search for your bot username, and send `/start`!

---

## 📖 Admin Guide & Initial Content Setup

1. **Open Admin Panel:**
   - In Telegram, send `/admin` or tap **🛠 Open Admin Panel** from the main menu.
2. **Create Categories:**
   - Tap **📂 Add Category**.
   - Enter name (e.g. `Action`, `Comedy`, `Trailers`).
   - Send an emoji (e.g. `💥`, `😂`, `🎬`).
3. **Upload Videos:**
   - Tap **📤 Upload Video**.
   - Select the target category.
   - Send or forward any video file directly in the chat.
   - Enter the video title.
   - Enter a description (or `/skip`).
   - The bot caches the Telegram `file_id` instantly in SQLite!
4. **Broadcast to Users:**
   - Tap **📢 Broadcast Message**.
   - Send your announcement text, photo, or video.
   - Review the confirmation preview and tap **✅ Confirm**.
5. **Manage Users & Bans:**
   - Tap **👥 All Users** or **🚫 Ban/Unban User**.
   - Enter any user's ID to inspect activity or toggle ban.

---

## 💾 Database Backup & Maintenance

The entire bot state (users, referral trees, categories, video references, and logs) is stored in the single file `data/bot.db`.

### Creating a Manual Backup:
```cmd
copy data\bot.db data\bot_backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%.db
```

### Automated Daily Backup via Windows Task Scheduler:
Create a batch file `backup.bat`:
```cmd
@echo off
set BACKUP_DIR=C:\Users\LENOVO\Downloads\video tg bot\backups
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"
copy "C:\Users\LENOVO\Downloads\video tg bot\data\bot.db" "%BACKUP_DIR%\bot_%DATE%.db"
```
Schedule `backup.bat` in Windows Task Scheduler to run daily.

---

## 🌐 24/7 Production Hosting Guide

### Option 1: Run as a Windows Service (NSSM)
1. Download **NSSM** (Non-Sucking Service Manager) from [nssm.cc](https://nssm.cc/download).
2. Open Command Prompt as Administrator:
   ```cmd
   nssm install TelegramVideoBot
   ```
3. Set the following fields in the GUI:
   - **Path:** `C:\Users\LENOVO\Downloads\video tg bot\venv\Scripts\python.exe`
   - **Startup directory:** `C:\Users\LENOVO\Downloads\video tg bot`
   - **Arguments:** `bot.py`
4. Click **Install service**.
5. Start the service:
   ```cmd
   nssm start TelegramVideoBot
   ```
Your bot will now automatically start when Windows boots and restart if it ever crashes.

### Option 2: Linux VPS / Ubuntu (systemd)
Create a systemd service file `/etc/systemd/system/videobot.service`:
```ini
[Unit]
Description=Telegram Smart Video Reward Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/ubuntu/video-tg-bot
ExecStart=/home/ubuntu/video-tg-bot/venv/bin/python bot.py
Restart=always
RestartSec=5
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```
Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable videobot
sudo systemctl start videobot
```

---

## 🔒 Security & Best Practices

- **Never share your `BOT_TOKEN`**: Keep your `.env` file private and never commit it to public git repositories (`.gitignore` excludes `.env`).
- **Telegram File IDs**: Telegram file IDs are permanent handles for media stored on Telegram servers. No video bytes consume your host server disk space!
- **Anti-Spam Throttling**: The broadcast engine sleeps 0.05 seconds between message transmissions to respect Telegram API rate limits (Flood Control).

---

## 📜 License
MIT License. Free for personal, commercial, and community use.

