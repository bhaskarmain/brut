/*CMD
command: /referral
help: Referral Dashboard with live stats and claim buttons
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
let req = Bot.getProperty("referrals_per_reward") || 2;
if (req < 1) { req = 1; }

let totalRewardsEarned = Math.floor(validReferrals / req);
let unclaimedRewards = Math.max(0, totalRewardsEarned - rewardsClaimed);
let referralsUntilNext = req - (validReferrals % req);

let botUsername = bot.name || "SmartVideoBot";
let refLink = "https://t.me/" + botUsername + "?start=ref_" + user.telegramid;

let isEnabled = Bot.getProperty("referral_enabled");
let statusBadge = (isEnabled !== false) ? "🟢 Active" : "🔴 Paused by Admin";

let claimBanner = "";
if (unclaimedRewards > 0) {
  claimBanner =
    "🎁 *YOU HAVE " + unclaimedRewards + " UNCLAIMED REWARD(S)!*\n" +
    "_Tap the 'Claim Free Video Reward' button below!_\n" +
    "━━━━━━━━━━━━━━━━━━━━━\n";
}

let text =
  "🎁 *Referral Rewards Dashboard*\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  claimBanner +
  "👥 *Total Successful Referrals:* " + validReferrals + "\n" +
  "🏆 *Total Videos Earned:* " + totalRewardsEarned + "\n" +
  "🎁 *Rewards Claimed:* " + rewardsClaimed + "\n" +
  "⏳ *Unclaimed Rewards:* *" + unclaimedRewards + "*\n" +
  "🎯 *Next Reward In:* " + referralsUntilNext + " more referral(s)\n" +
  "⚡ *Program Status:* " + statusBadge + "\n\n" +
  "📜 *Reward Rules:*\n" +
  "• *" + req + " Referrals* = *1 Free Random Video*\n" +
  "• *" + (req * 2) + " Referrals* = *2 Free Videos*\n" +
  "• *" + (req * 3) + " Referrals* = *3 Free Videos*\n" +
  "• _No limits! Keep inviting friends to earn unlimited videos!_\n\n" +
  "🔗 *Your Exclusive Referral Link:*\n" +
  "`" + refLink + "`\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  "_Tip: Tap the link above to copy it to your clipboard._";

let buttons = [];

if (unclaimedRewards > 0) {
  buttons.push([
    {
      title: "🎁 Claim Free Video Reward (" + unclaimedRewards + " Ready!)",
      command: "/claim_reward"
    }
  ]);
}

let shareUrl =
  "https://t.me/share/url?url=" +
  encodeURIComponent(refLink) +
  "&text=" +
  encodeURIComponent("🎬 Join this Telegram Video Bot to watch amazing videos and unlock free video rewards!");

buttons.push([
  { title: "📤 Share Referral Link", url: shareUrl },
  { title: "🏆 Leaderboard", command: "/leaderboard" }
]);

buttons.push([
  { title: "🔄 Refresh Stats", command: "/referral" },
  { title: "🔙 Back to Main Menu", command: "/start" }
]);

Bot.sendInlineKeyboard(buttons, text);

