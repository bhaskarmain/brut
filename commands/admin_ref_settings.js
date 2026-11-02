/*CMD
command: /admin_ref_settings
help: Referral system management
need_reply: false
auto_retry_time: 
folder: 
answer: 
keyboard: 
aliases: 
group: 
CMD*/

let req = Bot.getProperty("referrals_per_reward") || 1;
let isEnabled = Bot.getProperty("referral_enabled");
let statusStr = (isEnabled !== false) ? "🟢 Enabled (Active)" : "🔴 Disabled (Paused)";

let text =
  "🎁 *Referral Rewards Configuration*\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  "⚙️ *Current Status:* " + statusStr + "\n" +
  "🎯 *Requirement:* *" + req + "* referral(s) per 1 video reward\n" +
  "🏆 *Reward Type:* Random Video Streaming\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  "Modify settings using the buttons below:";

let toggleBtnText = (isEnabled !== false) ? "🔴 Disable Referral Program" : "🟢 Enable Referral Program";

let buttons = [
  [{ title: toggleBtnText, command: "/admin_toggle_ref" }],
  [{ title: "✏️ Change Requirement (" + req + " ref/video)", command: "/admin_set_ref_req" }],
  [{ title: "🏆 View Leaderboard", command: "/leaderboard" }],
  [{ title: "🔙 Back to Admin", command: "/admin" }]
];

Bot.sendInlineKeyboard(buttons, text);
