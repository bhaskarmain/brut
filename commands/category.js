/*CMD
command: /category
help: Instantly streams a random video from the selected category if user has balance
need_reply: false
auto_retry_time: 
folder: 
answer: 
keyboard: 
aliases: 
group: 
CMD*/

let parts = params ? params.trim().split(" ") : [];
let catId = parseInt(parts[0]);

if (!catId) {
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
    "━━━━━━━━━━━━━━━━━━━━━\n" +
    "_Tip: Niche diye gaye button se doston ko share karein!_";

  Bot.sendInlineKeyboard(buttons, text);
  return;
}

// 2. Fetch Category
let categories = Bot.getProperty("categories") || [];
let cat = null;
for (let i = 0; i < categories.length; i++) {
  if (categories[i].id === catId) {
    cat = categories[i];
    break;
  }
}

if (!cat) {
  Bot.sendMessage("⚠️ Category not found.");
  Bot.runCommand("/categories");
  return;
}

let catEmoji = cat.emoji || "📁";

// 3. Fetch and filter videos in this category
let allVideos = Bot.getProperty("videos") || [];
let catVideos = [];
for (let i = 0; i < allVideos.length; i++) {
  if (allVideos[i].category_id === catId) {
    catVideos.push(allVideos[i]);
  }
}

// Filter out zip archives so we never send zip document cards
let playableVideos = [];
let hasZipOnly = false;
for (let i = 0; i < catVideos.length; i++) {
  if (!catVideos[i].is_zip) {
    playableVideos.push(catVideos[i]);
  }
}

if (playableVideos.length === 0) {
  let buttons = [
    [{ title: "🎬 Watch Videos", command: "/categories" }],
    [{ title: "🏠 Main Menu", command: "/start" }]
  ];

  if (catVideos.length > 0) {
    // Only ZIP archives were uploaded
    Bot.sendInlineKeyboard(
      buttons,
      catEmoji + " *" + cat.name + "*\n\n" +
      "⚠️ *Format Notice:* Content in this category was uploaded as a .ZIP archive. Telegram cannot stream ZIP files in its native video player.\n\n" +
      "🛠 *Admin:* Go to `/admin` -> Manage Videos, remove the ZIP entry, and upload/forward the extracted MP4 video file!"
    );
  } else {
    Bot.sendInlineKeyboard(
      buttons,
      catEmoji + " *" + cat.name + "*\n\nNo videos have been uploaded to this category yet. Check back soon!"
    );
  }
  return;
}

// 4. Deduct 1 referral balance if not admin
if (!isAdmin) {
  User.setProperty("rewards_claimed", rewardsClaimed + 1, "integer");
}

// 5. Pick unwatched or random playable video
let watched = User.getProperty("watched_videos") || [];
let unwatched = [];
for (let i = 0; i < playableVideos.length; i++) {
  if (watched.indexOf(playableVideos[i].id) === -1) {
    unwatched.push(playableVideos[i]);
  }
}

let pool = unwatched.length > 0 ? unwatched : playableVideos;
let randomIndex = Math.floor(Math.random() * pool.length);
let selectedVid = pool[randomIndex];

// Update views
for (let i = 0; i < allVideos.length; i++) {
  if (allVideos[i].id === selectedVid.id) {
    allVideos[i].views = (allVideos[i].views || 0) + 1;
    break;
  }
}
Bot.setProperty("videos", allVideos, "json");

let totalViews = Bot.getProperty("total_views_count") || 0;
Bot.setProperty("total_views_count", totalViews + 1, "integer");

// Record on user
if (watched.indexOf(selectedVid.id) === -1) {
  watched.push(selectedVid.id);
  User.setProperty("watched_videos", watched, "json");
}

let userWatchedCount = User.getProperty("user_watched_count") || 0;
User.setProperty("user_watched_count", userWatchedCount + 1, "integer");

// 6. Build Caption and Interactive Controls
let newBalance = isAdmin ? "Unlimited (Admin)" : Math.max(0, currentBalance - 1);
let descPart = selectedVid.description ? "\n\n📝 _" + selectedVid.description + "_" : "";

let caption =
  "🎬 *" + selectedVid.title + "*\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  "📂 *Category:* " + catEmoji + " " + cat.name + "\n" +
  "💳 *Video Balance:* " + newBalance + (isAdmin ? "" : " Video(s)") +
  descPart + "\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  "✨ _Enjoy watching!_";

let inlineKeyboard = [
  [
    { text: "▶️ Next Video", callback_data: "/category " + cat.id }
  ],
  [
    { text: "🎬 Watch Videos", callback_data: "/categories" },
    { text: "🏠 Main Menu", callback_data: "/start" }
  ]
];

// Always stream as native Telegram video (never as document / zip)
Api.sendVideo({
  chat_id: chat.chatid,
  video: selectedVid.file_id,
  caption: caption,
  parse_mode: "Markdown",
  supports_streaming: true,
  reply_markup: {
    inline_keyboard: inlineKeyboard
  }
});
