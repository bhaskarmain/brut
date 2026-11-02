# 🚀 BOTS.BUSINESS (https://app.bots.business/) SETUP GUIDE

A complete guide on deploying and running your **Smart Video Reward Telegram Bot** on **[Bots.Business](https://app.bots.business/)** using **Bot JavaScript (BJS)**.

---

## 📌 OVERVIEW (خلاصہ)

Yeh bot **Bots.Business** platform ke official format mein mukammal tayyar hai. Is mein tamam features shamil hain:
1. **User Panel:** Categories browsing, direct video streaming, unwatched video prioritization, aur instant category random streaming.
2. **Referral Reward System (1 Refer = 1 Video):** 
   - Har 1 valid referral par user ko **1 Video Balance** milta hai.
   - Agar user ke paas balance nahi hai (`balance <= 0`), toh bot video stream nahi karega balke **"⚠️ Not Enough Balance!"** aur unka referral link dikhayega.
   - User jaise hi 1 dost ko invite karega, uska balance 1 ho jayega aur wo video watch kar sakega!
3. **Admin Panel (Exclusive ID: `8789936408`):**
   - Sirf admin ID `8789936408` ko full access hasil hai (unlimited video streaming bina kisi balance restriction ke).
   - Videos upload karna (Telegram se direct MP4/MOV), categories manage karna, videos delete karna, broadcast announcements bhejna, users ko ban/unban karna, aur global statistics.
4. **Native Video Streaming:**
   - Tamam videos direct Telegram video player mein stream hoti hain (`supports_streaming: true`).
   - Telegram ZIP archives ko video player mein extract nahi kar sakta. Isliye videos direct **MP4/MOV** format mein upload karni hoti hain.

---

## 🛠 TARIQA #1: GITHUB SE 1-CLICK IMPORT (RECOMMENDED)

Bots.Business mein Git integration shamil hoti hai:

1. **GitHub Repository:**
   - Repository: `https://github.com/bhaskarmain/brut.git`
   - Is repository mein mojood `bot.json` aur `commands/` directory root level par hain.

2. **Bots.Business mein Bot Banayein:**
   - [https://app.bots.business/](https://app.bots.business/) par login karein.
   - **"Create Bot"** par click karein aur apna Telegram Bot Token dalein (jo @BotFather se mila ho).

3. **Git Import Karein:**
   - Apne bot ke dashboard par **"Git"** tab par click karein.
   - Apni GitHub repository ka link connect karein ya **"Import from Git"** par click karein.
   - Bots.Business automatically `bot.json` aur `commands/` ke tamam commands ko aapke bot mein load kar dega!

---

## 👑 MASTER ADMINISTRATOR

- **Authorized Admin ID:** `8789936408`
- Sirf ID `8789936408` hi Admin Panel (`/admin`) ko access kar sakti hai.
- Admin ko videos dekhne ke liye balance ki zaroorat nahi hoti (Unlimited access).

---

## 🎬 VIDEOS UPLOAD AUR STREAMING GUIDE

### ⚠️ ZIP Archive Notice:
Telegram ka video player sirf **MP4 aur MOV** video files ko in-app stream kar sakta hai. Telegram servers par ZIP archives ko extract nahi karta. Agar aap `.zip` file bhejte hain, toh Telegram usko ek raw download document (jaise `CP3.zip 1034 MB`) dikhata hai jisme video play button nahi hota.

### ✅ Sahi Tareeqa:
1. Apne mobile ya computer par ZIP file ko extract karein.
2. `/admin` -> **📤 Upload Video** par click karein.
3. Category select karein.
4. Telegram chat mein extracted **MP4 ya MOV video** send ya forward karein.
5. Title enter karein aur Description set karein.
6. Video live ho jayegi aur sabhi users ke Telegram video player mein direct stream hogi!

---

## 🎁 1 REFER = 1 VIDEO BALANCE SYSTEM

- Har user `/referral` se apna referral link le sakta hai:
  `https://t.me/AapKaBot?start=ref_USERID`
- **Balance Calculation:**
  `Available Balance = (Total Referrals) - (Videos Watched)`
- **Video Watching:**
  - Jab user category choose karta hai ya "▶️ Next Video" dabata hai:
    - Agar `Balance >= 1`: 1 credit deduct hota hai aur video stream hoti hai.
    - Agar `Balance <= 0`: Bot video rokk deta hai aur message dikhata hai:
      `⚠️ Not Enough Balance! 1 Referral = 1 Video` sath mein unka referral link aur share button.
- Admin `8789936408` ke liye koi deduction nahi hoti aur balance unlimited hota hai.
