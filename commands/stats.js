/*CMD
command: /stats
help: User Personal Statistics
need_reply: false
auto_retry_time: 
folder: 
answer: 
keyboard: 
aliases: 
group: 
CMD*/

let watchedCount = User.getProperty("user_watched_count") || 0;
let refs = Bot.getProperty("ref_count_" + user.telegramid) || 0;
let claimed = User.getProperty("rewards_claimed") || 0;
let req = Bot.getProperty("referrals_per_reward") || 2;
if (req < 1) { req = 1; }

let totalEarned = Math.floor(refs / req);
let unclaimed = Math.max(0, totalEarned - claimed);
let nextIn = req - (refs % req);

let text =
  "📊 *My Personal Statistics*\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  "🎬 *Videos Watched:* " + watchedCount + "\n" +
  "👥 *Invited Friends:* " + refs + "\n" +
  "🏆 *Total Video Rewards Earned:* " + totalEarned + "\n" +
  "🎁 *Claimed Rewards:* " + claimed + "\n" +
  "✨ *Available to Claim:* " + unclaimed + "\n" +
  "🎯 *Next Reward In:* " + nextIn + " more invite(s)\n\n" +
  "⚡ *Account Status:* 🟢 Active & In Good Standing\n" +
  "━━━━━━━━━━━━━━━━━━━━━";

let buttons = [
  [
    { title: "🎁 Referral Program", command: "/referral" },
    { title: "🎬 Watch Videos", command: "/categories" }
  ],
  [{ title: "🏠 Main Menu", command: "/start" }]
];

Bot.sendInlineKeyboard(buttons, text);

