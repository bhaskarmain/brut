/*CMD
command: /referral
help: Advanced Referral Dashboard (1 Refer = 1 Video)
need_reply: false
auto_retry_time: 
folder: 
answer: 
keyboard: 
aliases: 
group: 
CMD*/

let validReferrals = Bot.getProperty("ref_count_" + user.telegramid) || 0;
let rewardsClaimed = User.getProperty("rewards_claimed") || 0;
let currentBalance = Math.max(0, validReferrals - rewardsClaimed);

// Tier badge
let tier = "🥉 Bronze Member";
if (validReferrals >= 10) {
  tier = "🥇 Gold Champion";
} else if (validReferrals >= 4) {
  tier = "🥈 Silver VIP";
}

let botUsername = bot.name || "SmartVideoBot";
let refLink = "https://t.me/" + botUsername + "?start=ref_" + user.telegramid;

let isEnabled = Bot.getProperty("referral_enabled");
let statusBadge = (isEnabled !== false) ? "🟢 Active" : "🔴 Paused by Admin";

let text =
  "🎁 *Referral Rewards Dashboard*\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  "🏅 *Your Rank:* " + tier + "\n" +
  "👥 *Total Successful Referrals:* *" + validReferrals + "*\n" +
  "🎬 *Videos Watched:* *" + rewardsClaimed + "*\n" +
  "💰 *Available Video Balance:* *" + currentBalance + " Video(s)*\n\n" +
  "📜 *Reward Rules:*\n" +
  "• *1 Referral* = *1 Video Access*\n" +
  "• No limits! Har friend ke judne par 1 video balance add hoga!\n" +
  "⚡ *Program Status:* " + statusBadge + "\n\n" +
  "🔗 *Your Exclusive Referral Link:*\n" +
  "`" + refLink + "`\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  "_Tip: Tap the link above to copy it automatically._";

let buttons = [];

if (currentBalance > 0) {
  buttons.push([
    {
      title: "🎬 Watch Videos Now (" + currentBalance + " Available)",
      command: "/categories"
    }
  ]);
}

let shareText = "🎬 Join this Telegram Video Bot to watch amazing videos! Tap the link below:";
let shareUrl =
  "https://t.me/share/url?url=" +
  encodeURIComponent(refLink) +
  "&text=" +
  encodeURIComponent(shareText);

buttons.push([
  { title: "📤 Share Referral Link", url: shareUrl },
  { title: "🏆 Leaderboard", command: "/leaderboard" }
]);

buttons.push([
  { title: "🔄 Refresh Stats", command: "/referral" },
  { title: "🔙 Back to Main Menu", command: "/start" }
]);

Bot.sendInlineKeyboard(buttons, text);
