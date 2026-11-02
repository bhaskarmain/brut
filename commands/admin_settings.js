/*CMD
command: /admin_settings
help: Bot System Settings Overview
need_reply: false
auto_retry_time: 
folder: 
answer: 
keyboard: 
aliases: 
group: 
CMD*/

let primaryAdmin = 8789936408;
let req = Bot.getProperty("referrals_per_reward") || 2;
let isRefEnabled = Bot.getProperty("referral_enabled");

let text =
  "⚙️ *Bot System Settings (Bots.Business)*\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  "👑 *Authorized Admin:* `" + primaryAdmin + "`\n\n" +
  "🎁 *Referral Requirement:* " + req + " refs/reward\n" +
  "⚡ *Referral Program:* " + (isRefEnabled !== false ? "Active" : "Disabled") + "\n" +
  "🏆 *Reward Type:* Random Video Streaming\n" +
  "☁️ *Platform:* https://app.bots.business/\n" +
  "━━━━━━━━━━━━━━━━━━━━━";

let buttons = [
  [{ title: "🔙 Admin Dashboard", command: "/admin" }]
];

Bot.sendInlineKeyboard(buttons, text);

