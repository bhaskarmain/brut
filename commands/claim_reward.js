/*CMD
command: /claim_reward
help: Claims a video using referral balance
need_reply: false
auto_retry_time: 
folder: 
answer: 
keyboard: 
aliases: 
group: 
CMD*/

let isEnabled = Bot.getProperty("referral_enabled");
if (isEnabled === false) {
  Bot.sendMessage("⚠️ Referral rewards are temporarily disabled by the administrator.");
  return;
}

let isAdmin = (user.telegramid == 8789936408 || user.telegramid == "8789936408");
let validReferrals = Bot.getProperty("ref_count_" + user.telegramid) || 0;
let rewardsClaimed = User.getProperty("rewards_claimed") || 0;
let balance = validReferrals - rewardsClaimed;

if (!isAdmin && balance <= 0) {
  Bot.sendMessage("⚠️ *Not Enough Balance!* You have no available video credits.\n\nInvite friends via /referral to earn balance!");
  Bot.runCommand("/referral");
  return;
}

let videos = Bot.getProperty("videos") || [];
let playableVideos = [];
for (let i = 0; i < videos.length; i++) {
  if (!videos[i].is_zip) {
    playableVideos.push(videos[i]);
  }
}

if (playableVideos.length === 0) {
  Bot.sendMessage("⚠️ No playable videos are in the library yet. Please contact the administrator!");
  return;
}

let watched = User.getProperty("watched_videos") || [];
let unwatched = [];
for (let i = 0; i < playableVideos.length; i++) {
  if (watched.indexOf(playableVideos[i].id) === -1) {
    unwatched.push(playableVideos[i]);
  }
}

let pool = unwatched.length > 0 ? unwatched : playableVideos;
let randomIndex = Math.floor(Math.random() * pool.length);
let rewardVid = pool[randomIndex];

// Update claimed counter
if (!isAdmin) {
  User.setProperty("rewards_claimed", rewardsClaimed + 1, "integer");
}

// Record as watched
if (watched.indexOf(rewardVid.id) === -1) {
  watched.push(rewardVid.id);
  User.setProperty("watched_videos", watched, "json");
}

let categories = Bot.getProperty("categories") || [];
let catName = "General";
let catEmoji = "📁";
for (let i = 0; i < categories.length; i++) {
  if (categories[i].id === rewardVid.category_id) {
    catName = categories[i].name;
    catEmoji = categories[i].emoji || "📁";
    break;
  }
}

let remaining = isAdmin ? "Unlimited" : Math.max(0, balance - 1);

let descPart = rewardVid.description ? "\n\n📝 _" + rewardVid.description + "_" : "";
let caption =
  "🎁 *REFERRAL VIDEO UNLOCKED!* 🏆\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  "🎬 *" + rewardVid.title + "*\n" +
  "📂 *Category:* " + catEmoji + " " + catName + "\n" +
  "💳 *Remaining Balance:* " + remaining + "\n" +
  descPart + "\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  "🎉 _Keep inviting friends to earn more!_";

let inlineKeyboard = [
  [
    { text: "🎬 Watch Videos", callback_data: "/categories" },
    { text: "📊 Referral Dashboard", callback_data: "/referral" }
  ],
  [
    { text: "🏠 Main Menu", callback_data: "/start" }
  ]
];

Api.sendVideo({
  chat_id: chat.chatid,
  video: rewardVid.file_id,
  caption: caption,
  parse_mode: "Markdown",
  supports_streaming: true,
  reply_markup: {
    inline_keyboard: inlineKeyboard
  }
});
