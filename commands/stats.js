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
let isAdmin = (user.telegramid == 8789936408 || user.telegramid == "8789936408");
let balance = isAdmin ? "Unlimited (Admin)" : Math.max(0, refs - claimed);

let text =
  "📊 *My Personal Statistics*\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  "💰 *Available Video Balance:* *" + balance + (isAdmin ? "" : " Video(s)") + "*\n" +
  "🎬 *Videos Watched:* " + watchedCount + "\n" +
  "👥 *Invited Friends:* " + refs + "\n" +
  "📌 *Rule:* 1 Referral = 1 Video\n\n" +
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
