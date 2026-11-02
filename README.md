# 🎬 Smart Video Reward Telegram Bot for Bots.Business

A production-ready Telegram Video Bot built specifically for **[Bots.Business](https://app.bots.business/)** using **Bot JavaScript (BJS)**.

---

## 🌟 Key Features

### 👤 1. User Panel
- **🎬 Watch Videos:** When a user taps a category, the bot immediately streams a random video from that category in the built-in Telegram video player (`supports_streaming: true`).
- **▶️ Next Video:** Users can tap *Next Video* under the player to watch the next random video.
- **Hidden Counts:** Video counts are hidden from the user interface for a clean, premium look.
- **🌟 Daily Bonus:** Free daily surprise reward video every 24 hours.
- **👤 My Account & 📊 Statistics:** Track watch history, referrals, and live available video balance.

### 🎁 2. Referral Reward System (1 Refer = 1 Video Balance)
- **Formula:** **1 Referral = 1 Video Access**!
- **Strict Balance Enforcement:**
  - If a user has `0 Balance`, clicking to watch a video displays `⚠️ Not Enough Balance!` along with their referral link and direct share buttons.
  - When user refers a friend, 1 video credit is added to their balance immediately.
  - Watching a video deducts 1 credit.
- **Interactive Dashboard:** Live balance counter, rank badges (🥉 Bronze, 🥈 Silver, 🥇 Gold), and instant share links.
- **Anti-Cheat:** Blocks self-referrals and duplicate accounts.

### 🛠 3. Admin Panel (Exclusive Admin: `8789936408`)
- **📤 Upload Video:**
  - Direct MP4/MOV video upload & forwarding.
  - All videos stream natively in Telegram video player with play/pause, scrub, and fullscreen.
  - ZIP guidance: Instructs admin to extract archives on PC/phone and upload MP4 videos directly so Telegram streams them smoothly.
- **📂 Add & Manage Categories:** Create, edit, and delete categories with custom emojis.
- **📋 Video Catalog:** Manage, preview, and delete uploaded videos.
- **📢 Broadcast:** Send announcements to all registered users.
- **🚫 User Management:** Ban/unban users by numeric Telegram ID.
- **📊 Advanced Analytics:** Real-time metrics, views counter, and user growth.
- **👑 Admin Bypass:** Admin `8789936408` has unlimited video streaming without any referral or balance requirement.

---

## 🚀 How to Import into Bots.Business (1-Click Setup)

1. Open your bot at **[https://app.bots.business/](https://app.bots.business/)**.
2. Click on the **"Git"** tab.
3. Link this repository:
   ```text
   https://github.com/bhaskarmain/brut.git
   ```
4. Click **"Import from Git"** or **"Sync"**.
5. All commands in `commands/` and `bot.json` are automatically loaded into your bot!

---

## 👑 Admin Verification
The bot is strictly configured for administrator ID **`8789936408`**.
When starting the bot from that Telegram account, the **🛠 Open Admin Panel** button appears automatically, or you can send `/admin`.
