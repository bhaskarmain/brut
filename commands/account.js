/*CMD
command: /account
help: User Profile & Account details
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
let joined = User.getProperty("joined_at");
let joinDate = joined ? joined.substring(0, 10) : "Today";

let botUsername = bot.name || "SmartVideoBot";
let refLink = "https://t.me/" + botUsername + "?start=ref_" + user.telegramid;

let text =
  "👤 *My Account Profile*\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  "🆔 *User ID:* `" + user.telegramid + "`\n" +
  "👤 *Name:* " + (user.first_name || "Valued User") + "\n" +
  "🏷 *Username:* " + (user.username ? "@" + user.username : "Not set") + "\n" +
  "📅 *Member Since:* " + joinDate + "\n\n" +
  "💰 *Available Video Balance:* *" + balance + (isAdmin ? "" : " Video(s)") + "*\n" +
  "🎬 *Videos Watched:* " + watchedCount + "\n" +
  "👥 *Successful Referrals:* " + refs + "\n\n" +
  "🔗 *Your Referral Link:*\n" +
  "`" + refLink + "`\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  "_Tip: 1 Referral = 1 Video access!_";

let buttons = [
  [
    { title: "🎁 Referral Dashboard", command: "/referral" },
    { title: "🎬 Watch Videos", command: "/categories" }
  ],
  [
    { title: "🔄 Refresh", command: "/account" },
    { title: "🏠 Main Menu", command: "/start" }
  ]
];

Bot.sendInlineKeyboard(buttons, text);
