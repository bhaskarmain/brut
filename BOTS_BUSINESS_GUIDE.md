# 🚀 BOTS.BUSINESS (https://app.bots.business/) SETUP GUIDE

A complete guide on deploying and running your **Smart Video Reward Telegram Bot** on **[Bots.Business](https://app.bots.business/)** using **Bot JavaScript (BJS)**.

---

## 📌 OVERVIEW (خلاصہ)

Yeh bot ab **Bots.Business** platform ke official format mein mukammal tayyar hai. Is mein tamam features shamil hain:
1. **User Panel:** Categories browsing, direct video streaming, unwatched video prioritization, aur surprise random videos.
2. **Referral Reward System:** Har user ka unique link, 2 referrals = 1 free video reward (4 referrals = 2 videos, etc.), automated calculation, anti-cheat, dashboard, aur leaderboard.
3. **Admin Panel:** Videos upload karna (Telegram se direct), categories create/edit karna, videos delete karna, broadcast announcements bhejna, users ko ban/unban karna, aur global statistics.

---

## 🛠 TARIQA #1: GITHUB SE 1-CLICK IMPORT (RECOMMENDED)

Bots.Business mein Git integration shamil hoti hai. Aap is folder ko GitHub par push karke 1 minute mein import kar sakte hain:

1. **GitHub Repository Banayein:**
   - [GitHub.com](https://github.com) par jayein aur new repository banayein.
   - Apne is project folder ko repository mein upload/push karein.
   - Folder mein mojood `bot.json` aur `commands/` directory root level par honi chahiye.

2. **Bots.Business mein Bot Banayein:**
   - [https://app.bots.business/](https://app.bots.business/) par login karein.
   - **"Create Bot"** par click karein aur apna Telegram Bot Token dalein (jo @BotFather se mila ho).

3. **Git Import Karein:**
   - Apne bot ke dashboard par **"Git"** tab par click karein.
   - Apni GitHub repository ka link connect karein ya **"Import from Git"** par click karein.
   - Bots.Business automatically `bot.json` aur `commands/` ke tamam 38 commands ko aapke bot mein load kar dega!

---

## 📝 TARIQA #2: MANUAL WEB DASHBOARD COPY-PASTE

Agar aap Git use nahi karna chahte, toh aap direct https://app.bots.business/ ke web editor mein commands copy-paste kar sakte hain:

1. [https://app.bots.business/](https://app.bots.business/) par jayein aur apna bot open karein.
2. Left menu se **"Commands"** par click karein.
3. Har command ke liye **"+ New Command"** par click karein:
   - **Command Name:** File ke andar likha hua command name (jaise `/start`, `/categories`, `/admin`).
   - **BJS Code:** File ke andar ka JavaScript code paste karein (header ke neeche wala code).
   - **Need Reply:** Jin commands ke header mein `need_reply: true` likha ho, unka toggle switch **ON** karein.
   - **Save** par click karein.

### List of Key Commands to Add:

| Command Name | File Path | Need Reply? | Description |
| :--- | :--- | :--- | :--- |
| `/start` | `commands/_start.js` | No | Welcome message & Referral tracking |
| `/search` | `commands/search.js` | No | Video Search by Title / Keyword |
| `/search_query` | `commands/search_query.js` | **Yes** | Executes Search Query |
| `/daily_bonus` | `commands/daily_bonus.js` | No | Free Daily Bonus Video Claim (24h) |
| `/categories` | `commands/categories.js` | No | Browse categories with counts |
| `/category` | `commands/category.js` | No | Paginated videos inside category |
| `/video_info` | `commands/video_info.js` | No | Video details card |
| `/play_video` | `commands/play_video.js` | No | Stream video via Telegram |
| `/random_video` | `commands/random_video.js` | No | Surprise unwatched video |
| `/referral` | `commands/referral.js` | No | Referral dashboard & stats |
| `/claim_reward` | `commands/claim_reward.js` | No | Claim free reward video |
| `/leaderboard` | `commands/leaderboard.js` | No | Top referrers leaderboard |
| `/account` | `commands/account.js` | No | User profile & join date |
| `/stats` | `commands/stats.js` | No | Personal view & invite stats |
| `/help` | `commands/help.js` | No | Usage rules & guide |
| `/admin` | `commands/admin.js` | No | Admin management panel |
| `/admin_upload` | `commands/admin_upload.js` | No | Upload video - Step 1 |
| `/admin_upload_pickcat` | `commands/admin_upload_pickcat.js` | No | Upload video - Step 2 |
| `/admin_upload_got_video`| `commands/admin_upload_got_video.js` | **Yes** | Receives video file |
| `/admin_upload_got_title`| `commands/admin_upload_got_title.js` | **Yes** | Receives video title |
| `/admin_upload_got_desc` | `commands/admin_upload_got_desc.js`  | **Yes** | Receives description & saves |
| `/admin_add_cat` | `commands/admin_add_cat.js` | **Yes** | Add category name |
| `/admin_add_cat_step2` | `commands/admin_add_cat_step2.js` | **Yes** | Add category emoji & saves |
| `/admin_edit_cat` | `commands/admin_edit_cat.js` | No | Edit/Delete categories |
| `/admin_cat_detail` | `commands/admin_cat_detail.js` | No | Category delete card |
| `/admin_del_cat_do` | `commands/admin_del_cat_do.js` | No | Executes category deletion |
| `/admin_manage_vids` | `commands/admin_manage_vids.js` | No | Manage all videos |
| `/admin_vid_detail` | `commands/admin_vid_detail.js` | No | Single video actions |
| `/admin_del_vid_do` | `commands/admin_del_vid_do.js` | No | Deletes video |
| `/admin_users` | `commands/admin_users.js` | No | View registered users |
| `/admin_stats` | `commands/admin_stats.js` | No | Global statistics |
| `/admin_ref_settings`| `commands/admin_ref_settings.js` | No | Referral program settings |
| `/admin_toggle_ref` | `commands/admin_toggle_ref.js` | No | Enable/Disable referral rewards |
| `/admin_set_ref_req` | `commands/admin_set_ref_req.js` | **Yes** | Change requirement number |
| `/admin_broadcast` | `commands/admin_broadcast.js` | **Yes** | Send broadcast message |
| `/admin_ban` | `commands/admin_ban.js` | **Yes** | Ban/Unban user by ID |
| `/admin_settings` | `commands/admin_settings.js` | No | Settings overview |
| `/setup_admin` | `commands/setup_admin.js` | No | Set your Telegram ID as Admin |
| `@` | `commands/_before.js` | No | Security filter (blocks banned users) |
| `*` | `commands/_fallback.js` | No | Fallback menu for unhandled text |

---

## 👑 PEHLA STEP: APNE AAP KO ADMIN KAISE BANAYEIN?

Jab aap bot launch karein:
1. Telegram mein apne bot ko open karein aur `/start` bhejein.
2. Ab chat mein yeh command bhejein:
   ```
   /setup_admin
   ```
   *(Ya `/setup_admin APNA_NUMERIC_ID` jaise `/setup_admin 123456789`)*
3. Bot foran reply karega ke aapko Administrator bana diya gaya hai!
4. Ab aap `/admin` command bhej kar poora Admin Panel use kar sakte hain!

---

## 🎬 VIDEOS UPLOAD AUR CATEGORIES KAISE BANAYEIN?

1. **Category Banayein:**
   - `/admin` bhejein.
   - **📂 Add Category** par click karein.
   - Category ka naam bhejein (jaise `Action`, `Funny`, ya `Trailers`).
   - Uska emoji bhejein (jaise `🔥` ya `😂`). Category save ho jayegi!
2. **Video Upload Karein:**
   - `/admin` open karein aur **📤 Upload Video** par click karein.
   - Category select karein.
   - Telegram chat mein koi bhi video file send ya forward karein.
   - Video ka Title bhejein.
   - Description bhejein (ya `/skip` bhejein).
   - Video live ho jayegi aur sab users ke liye available ho jayegi!

---

## 🎁 REFERRAL REWARD SYSTEM KAISE CHALTA HAI?

- Har user `/referral` par click karke apna personal link le sakta hai.
- Format: `https://t.me/AapKaBot?start=ref_USERID`
- Jab naya dost join karta hai:
  - Pehle user ko Telegram notification milti hai: `"🎉 New Referral Joined!"`
  - Anti-cheat self-referrals aur duplicate users ko block karta hai.
  - Jab 2 referrals mukammal ho jate hain, dashboard par **"🎁 Claim Free Video Reward"** button active ho jata hai!
  - Button par click karne se bot ek unwatched random video stream karta hai!
  - Mazid 2 referrals (total 4) par doosri video milti hai, 6 par teesri, etc.

---

## 🟢 HOSTING & 24/7 AVAILABILITY

Bots.Business cloud-based platform hai. Iska faida yeh hai ke:
- **No Hosting Cost:** Bots.Business par bot 24/7 free cloud par chalta hai.
- **No PC/CMD needed:** Aapko apna computer ya CMD on rakhne ki zaroorat nahi hoti.
- **Automatic Database:** Tamam users, referrals, categories, aur videos ka data Bots.Business cloud storage mein permanently mehfooz rehta hai.

