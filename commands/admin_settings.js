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

let adminIds = Bot.getProperty("admin_ids") || [];
let req = Bot.getProperty("referrals_per_reward") || 2;
let isRefEnabled = Bot.getProperty("referral_enabled");

let text =
  "⚙️ *Bot System Settings (Bots.Business)*\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  "👑 *Authorized Admin IDs:*\n`" + JSON.stringify(adminIds) + "`\n\n" +
  "🎁 *Referral Requirement:* " + req + " refs/reward\n" +
  "⚡ *Referral Program:* " + (isRefEnabled !== false ? "Active" : "Disabled") + "\n" +
  "🏆 *Reward Type:* Random Video Streaming\n" +
  "☁️ *Platform:* https://app.bots.business/\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  "_Tip: You can add or change Admin IDs by running /setup_admin <id>._";

let buttons = [
  [{ title: "👑 Add Admin ID", command: "/setup_admin" }],
  [{ title: "🔙 Admin Dashboard", command: "/admin" }]
];

Bot.sendInlineKeyboard(buttons, text);

