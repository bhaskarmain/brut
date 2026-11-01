/*CMD
command: /admin_stats
help: Global Bot Analytics and Statistics
need_reply: false
auto_retry_time: 
folder: 
answer: 
keyboard: 
aliases: 
group: 
CMD*/

let totalUsers = Bot.getProperty("total_users_count") || 0;
let categories = Bot.getProperty("categories") || [];
let videos = Bot.getProperty("videos") || [];
let totalViews = Bot.getProperty("total_views_count") || 0;
let totalRefs = Bot.getProperty("total_valid_referrals") || 0;

let text =
  "📊 *Bot Global Statistics & Analytics*\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  "👥 *Total Registered Users:* " + totalUsers + "\n" +
  "📂 *Total Categories:* " + categories.length + "\n" +
  "🎬 *Total Videos:* " + videos.length + "\n" +
  "👁 *Total Video Views:* " + totalViews + "\n" +
  "🤝 *Total Successful Referrals:* " + totalRefs + "\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  "🟢 *Platform Status:* Operational on Bots.Business";

let buttons = [[{ title: "🔙 Back to Admin Dashboard", command: "/admin" }]];
Bot.sendInlineKeyboard(buttons, text);

