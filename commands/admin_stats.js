/*CMD
command: /admin_stats
help: Advanced Global Bot Analytics and Statistics
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

// Calculate most popular video
let topVideo = null;
let maxViews = -1;
for (let i = 0; i < videos.length; i++) {
  let v = videos[i];
  if ((v.views || 0) > maxViews) {
    maxViews = v.views || 0;
    topVideo = v;
  }
}

let avgViews = videos.length > 0 ? (totalViews / videos.length).toFixed(1) : "0";
let topVidStr = topVideo ? topVideo.title + " (" + (topVideo.views || 0) + " views)" : "None yet";

let text =
  "📊 *Bot Global Analytics & Insights*\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  "👥 *Total Registered Users:* " + totalUsers + "\n" +
  "🤝 *Total Successful Referrals:* " + totalRefs + "\n\n" +
  "🎬 *Total Videos:* " + videos.length + "\n" +
  "📂 *Total Categories:* " + categories.length + "\n" +
  "👁 *Total Video Views:* " + totalViews + "\n" +
  "📈 *Average Views / Video:* " + avgViews + "\n" +
  "🔥 *Top Performing Video:*\n`" + topVidStr + "`\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  "🟢 *Platform Status:* Operational on Bots.Business";

let buttons = [
  [{ title: "🔄 Refresh Analytics", command: "/admin_stats" }],
  [{ title: "🔙 Back to Admin Dashboard", command: "/admin" }]
];

Bot.sendInlineKeyboard(buttons, text);
