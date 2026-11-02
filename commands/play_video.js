/*CMD
command: /play_video
help: Streams the requested video directly to user with attached controls
need_reply: false
auto_retry_time: 
folder: 
answer: 
keyboard: 
aliases: 
group: 
CMD*/

let vidId = parseInt(params);
if (!vidId) {
  Bot.runCommand("/categories");
  return;
}

// 1. Balance and Access Verification (1 Refer = 1 Video)
let isAdmin = (user.telegramid == 8789936408 || user.telegramid == "8789936408");
let validReferrals = Bot.getProperty("ref_count_" + user.telegramid) || 0;
let rewardsClaimed = User.getProperty("rewards_claimed") || 0;
let currentBalance = validReferrals - rewardsClaimed;

if (!isAdmin && currentBalance <= 0) {
  let botUsername = bot.name || "SmartVideoBot";
  let refLink = "https://t.me/" + botUsername + "?start=ref_" + user.telegramid;
  let shareText = "🎬 Watch amazing videos on this bot! Tap the link below to join:";
  let shareUrl =
    "https://t.me/share/url?url=" +
    encodeURIComponent(refLink) +
    "&text=" +
    encodeURIComponent(shareText);

  let buttons = [
    [{ title: "📤 Share Referral Link", url: shareUrl }],
    [{ title: "🎁 Referral Dashboard", command: "/referral" }],
    [{ title: "🏠 Main Menu", command: "/start" }]
  ];

  let text =
    "⚠️ *Not Enough Balance!*\n" +
    "━━━━━━━━━━━━━━━━━━━━━\n" +
    "Aapke paas video dekhne ke liye balance nahi hai!\n\n" +
    "📌 *Balance Rule:*\n" +
    "• *1 Referral = 1 Video*\n" +
    "• Total Referrals: *" + validReferrals + "*\n" +
    "• Videos Watched: *" + rewardsClaimed + "*\n" +
    "• Available Balance: *0 Videos*\n\n" +
    "🎁 *Balance Kaise Paye?*\n" +
    "Apne doston ko invite karein! Har *1 refer* par aapko *1 video* dekhne ko milegi.\n\n" +
    "🔗 *Aapka Referral Link:*\n" +
    "`" + refLink + "`\n" +
    "━━━━━━━━━━━━━━━━━━━━━";

  Bot.sendInlineKeyboard(buttons, text);
  return;
}

// 2. Fetch video
let videos = Bot.getProperty("videos") || [];
let vidIndex = -1;
for (let i = 0; i < videos.length; i++) {
  if (videos[i].id === vidId) {
    vidIndex = i;
    break;
  }
}

if (vidIndex === -1) {
  Bot.sendMessage("⚠️ Video not found or has been removed.");
  return;
}

let vid = videos[vidIndex];

// If video was saved as a zip file, cannot stream
if (vid.is_zip) {
  Bot.sendMessage("⚠️ Telegram cannot stream ZIP archives in the video player. Please ask the admin to upload the extracted MP4 video!");
  return;
}

// 3. Deduct balance if not admin
if (!isAdmin) {
  User.setProperty("rewards_claimed", rewardsClaimed + 1, "integer");
}

// Get category info
let categories = Bot.getProperty("categories") || [];
let catName = "General";
let catEmoji = "📁";
for (let i = 0; i < categories.length; i++) {
  if (categories[i].id === vid.category_id) {
    catName = categories[i].name;
    catEmoji = categories[i].emoji || "📁";
    break;
  }
}

// Increment views
let currentViews = (vid.views || 0) + 1;
videos[vidIndex].views = currentViews;
Bot.setProperty("videos", videos, "json");

let totalViews = Bot.getProperty("total_views_count") || 0;
Bot.setProperty("total_views_count", totalViews + 1, "integer");

// Record watched video on user profile
let watched = User.getProperty("watched_videos") || [];
if (watched.indexOf(vid.id) === -1) {
  watched.push(vid.id);
  User.setProperty("watched_videos", watched, "json");
}

let userWatchedCount = User.getProperty("user_watched_count") || 0;
User.setProperty("user_watched_count", userWatchedCount + 1, "integer");

// Caption & Controls
let newBalance = isAdmin ? "Unlimited (Admin)" : Math.max(0, currentBalance - 1);
let descPart = vid.description ? "\n\n📝 _" + vid.description + "_" : "";
let caption =
  "🎬 *" + vid.title + "*\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  "📂 *Category:* " + catEmoji + " " + catName + "\n" +
  "💳 *Video Balance:* " + newBalance + (isAdmin ? "" : " Video(s)") +
  descPart + "\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  "✨ _Enjoy watching!_";

let inlineKeyboard = [
  [
    { text: "▶️ Next Video", callback_data: "/category " + vid.category_id }
  ],
  [
    { text: "🎬 Watch Videos", callback_data: "/categories" },
    { text: "🏠 Main Menu", callback_data: "/start" }
  ]
];

// Always send as native streaming video
Api.sendVideo({
  chat_id: chat.chatid,
  video: vid.file_id,
  caption: caption,
  parse_mode: "Markdown",
  supports_streaming: true,
  reply_markup: {
    inline_keyboard: inlineKeyboard
  }
});
