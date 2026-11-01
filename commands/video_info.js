/*CMD
command: /video_info
help: Video details card
need_reply: false
auto_retry_time: 
folder: 
answer: 
keyboard: 
aliases: 
group: 
CMD*/

let vidId = parseInt(params);
if (!vidId) {
  Bot.runCommand("/categories");
  return;
}

let videos = Bot.getProperty("videos") || [];
let vid = null;
for (let i = 0; i < videos.length; i++) {
  if (videos[i].id === vidId) {
    vid = videos[i];
    break;
  }
}

if (!vid) {
  Bot.sendMessage("⚠️ Video not found or has been removed.");
  Bot.runCommand("/categories");
  return;
}

let categories = Bot.getProperty("categories") || [];
let catName = "General";
let catEmoji = "📁";
for (let i = 0; i < categories.length; i++) {
  if (categories[i].id === vid.category_id) {
    catName = categories[i].name;
    catEmoji = categories[i].emoji || "📁";
    break;
  }
}

let views = vid.views || 0;
let desc = vid.description || "No description provided.";

let text =
  "🎬 *" + vid.title + "*\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  "📂 *Category:* " + catEmoji + " " + catName + "\n" +
  "👁 *Total Views:* " + views + "\n\n" +
  "📝 *Description:*\n_" + desc + "_\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  "Tap *▶️ Watch Now* to stream this video directly in Telegram!";

let buttons = [
  [{ title: "▶️ Watch Now", command: "/play_video " + vid.id }],
  [
    { title: "🔙 Back to Category", command: "/category " + vid.category_id },
    { title: "🏠 Main Menu", command: "/start" }
  ]
];

Bot.sendInlineKeyboard(buttons, text);

