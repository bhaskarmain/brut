/*CMD
command: /help
help: Bot Help & Guidelines
need_reply: false
auto_retry_time: 
folder: 
answer: 
keyboard: 
aliases: 
group: 
CMD*/

let req = Bot.getProperty("referrals_per_reward") || 2;

let helpText =
  "ℹ️ *Bot Help & Guidelines*\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  "*1. How to Watch Videos:*\n" +
  "Tap *📂 Browse Categories* or *🎬 Watch Videos* from the main menu, pick a category, and choose any video to stream it directly in Telegram.\n\n" +
  "*2. How to Earn Free Video Rewards:*\n" +
  "• Open *🎁 Referral Rewards* and copy your personal link.\n" +
  "• Share your link with friends or channels.\n" +
  "• For every *" + req + " genuine new users* who join via your link, you unlock *1 free exclusive video reward*!\n" +
  "• The rewards are *unlimited*: " + (req * 2) + " referrals = 2 videos, " + (req * 3) + " referrals = 3 videos, etc.\n\n" +
  "*3. Rules & Fair Play:*\n" +
  "• Self-referrals and duplicate accounts are strictly blocked.\n" +
  "• Fake accounts will result in account suspension.\n\n" +
  "*4. Need Assistance?*\n" +
  "If you encounter any issues or want to report a broken video, contact an administrator.";

let buttons = [
  [
    { title: "🎬 Start Watching", command: "/categories" },
    { title: "🎁 Referral Program", command: "/referral" }
  ],
  [{ title: "🔙 Back to Main Menu", command: "/start" }]
];

Bot.sendInlineKeyboard(buttons, helpText);

