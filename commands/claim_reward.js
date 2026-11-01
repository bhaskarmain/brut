/*CMD
command: /claim_reward
help: Atomically claims one referral video reward
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

let validReferrals = Bot.getProperty("ref_count_" + user.telegramid) || 0;
let rewardsClaimed = User.getProperty("rewards_claimed") || 0;
let req = Bot.getProperty("referrals_per_reward") || 2;
if (req < 1) { req = 1; }

let totalRewardsEarned = Math.floor(validReferrals / req);
let unclaimedRewards = totalRewardsEarned - rewardsClaimed;

if (unclaimedRewards <= 0) {
  Bot.sendMessage("⚠️ You have no unclaimed rewards at this time. Invite more friends to earn rewards!");
  Bot.runCommand("/referral");
  return;
}

let videos = Bot.getProperty("videos") || [];
if (videos.length === 0) {
  Bot.sendMessage("⚠️ No videos are uploaded in the bot library yet. Please contact the administrator!");
  return;
}

let watched = User.getProperty("watched_videos") || [];

// Prioritize unwatched videos
let unwatched = [];
for (let i = 0; i < videos.length; i++) {
  if (watched.indexOf(videos[i].id) === -1) {
    unwatched.push(videos[i]);
  }
}

let pool = unwatched.length > 0 ? unwatched : videos;
let randomIndex = Math.floor(Math.random() * pool.length);
let rewardVid = pool[randomIndex];

// Update claimed counter
User.setProperty("rewards_claimed", rewardsClaimed + 1, "integer");

// Record as watched
if (watched.indexOf(rewardVid.id) === -1) {
  watched.push(rewardVid.id);
  User.setProperty("watched_videos", watched, "json");
}

// Find category name
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

// Send reward video
let caption =
  "🎁 *FREE REFERRAL REWARD UNLOCKED!* 🏆\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  "🎬 *" + rewardVid.title + "*\n" +
  "📂 Category: " + catEmoji + " " + catName + "\n\n" +
  "_" + (rewardVid.description || "Enjoy your exclusive referral reward video!") + "_\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  "🎉 _Thank you for supporting our community by inviting friends!_";

Api.sendVideo({
  chat_id: chat.chatid,
  video: rewardVid.file_id,
  caption: caption,
  parse_mode: "Markdown"
});

// Calculate remaining
let remaining = unclaimedRewards - 1;
let buttons = [];
if (remaining > 0) {
  buttons.push([{ title: "🎁 Claim Another Reward (" + remaining + " Left)", command: "/claim_reward" }]);
}
buttons.push([
  { title: "🎁 Referral Dashboard", command: "/referral" },
  { title: "🏠 Main Menu", command: "/start" }
]);

Bot.sendInlineKeyboard(buttons, "✨ You have successfully claimed 1 free video reward!");

