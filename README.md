# 🎬 Smart Video Reward Telegram Bot for Bots.Business

A production-ready Telegram Video Bot built specifically for **[Bots.Business](https://app.bots.business/)** using **Bot JavaScript (BJS)**.

---

## 🌟 Key Features

### 👤 1. User Panel
- **🎬 Watch Videos:** Instant video playback! When a user taps a category, the bot immediately streams a random video from that category.
- **▶️ Next Video:** Users can keep tapping *Next Video* under the player to watch endless random videos from that category.
- **Hidden Counts:** Video counts are hidden from the user interface for a clean, clean look.
- **🌟 Daily Bonus:** Free daily surprise reward video every 24 hours.
- **👤 My Account & 📊 Statistics:** Track watch history, referrals, and status.

### 🎁 2. Referral Reward System
- **Formula:** 2 Referrals = 1 Free Video (4 Referrals = 2 Videos, etc. — unlimited & repeatable).
- **Interactive Dashboard:** Dynamic graphical progress bar (`[█████░░░░░] 50%`) and tier badges (🥉 Bronze, 🥈 Silver, 🥇 Gold).
- **Anti-Cheat:** Blocks self-referrals and duplicate accounts.
- **One-Tap Claim:** Instant video reward delivery when unlocked.

### 🛠 3. Admin Panel (Exclusive Admin: `8789936408`)
- **📤 Upload Video & ZIP Support:**
  - Send direct MP4/MOV videos.
  - Send `.ZIP` archives — automatic video processing & extraction!
- **📂 Add & Manage Categories:** Create, edit, and delete categories with custom emojis.
- **📋 Video Catalog:** Manage, preview, and delete uploaded videos.
- **📢 Broadcast:** Send announcements to all registered users.
- **🚫 User Management:** Ban/unban users by numeric Telegram ID.
- **📊 Advanced Analytics:** Real-time metrics, views counter, and top performing video tracker.

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
When you start the bot from that Telegram account, the **🛠 Open Admin Panel** button appears automatically, or you can send `/admin`.

---

## 📁 Repository Structure

```
├── bot.json                 # Bots.Business sync descriptor
├── commands/                # 37 BJS command files
│   ├── _before.js           # Security middleware (ban filter)
│   ├── _fallback.js         # Wildcard message handler
│   ├── _start.js            # Main welcome & referral tracking
│   ├── account.js           # User account profile
│   ├── admin.js             # Master admin dashboard
│   ├── admin_upload.js      # Video & ZIP upload wizard
│   ├── categories.js        # Category selection
│   ├── category.js          # Direct category random video player
│   ├── claim_reward.js      # Referral reward delivery
│   ├── daily_bonus.js       # 24h bonus claim
│   └── ...
├── BOTS_BUSINESS_GUIDE.md   # Complete step-by-step Urdu/English guide
└── README.md                # Project documentation
```
