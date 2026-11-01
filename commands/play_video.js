/*CMD
command: /play_video
help: Streams the requested video directly to user with attached controls
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
let vidIndex = -1;
for (let i = 0; i < videos.length; i++) {
  if (videos[i].id === vidId) {
    vidIndex = i;
    break;
  }
}

if (vidIndex === -1) {
  Bot.sendMessage("⚠️ Video not found or has been removed.");
  return;
}

let vid = videos[vidIndex];

// Get category info
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

// Increment views
let currentViews = (vid.views || 0) + 1;
videos[vidIndex].views = currentViews;
Bot.setProperty("videos", videos, "json");

let totalViews = Bot.getProperty("total_views_count") || 0;
Bot.setProperty("total_views_count", totalViews + 1, "integer");

// Record watched video on user profile
let watched = User.getProperty("watched_videos") || [];
if (watched.indexOf(vid.id) === -1) {
  watched.push(vid.id);
  User.setProperty("watched_videos", watched, "json");
}

let userWatchedCount = User.getProperty("user_watched_count") || 0;
User.setProperty("user_watched_count", userWatchedCount + 1, "integer");

// Stream video with interactive controls attached directly
let descPart = vid.description ? "\n\n📝 _" + vid.description + "_" : "";
let caption =
  "🎬 *" + vid.title + "*\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  "📂 *Category:* " + catEmoji + " " + catName + "\n" +
  "👁 *Views:* " + currentViews +
  descPart + "\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  "✨ _Enjoy watching!_";

let inlineKeyboard = [
  [
    { text: "🎲 Next Random Video", callback_data: "/random_video" },
    { text: catEmoji + " " + catName, callback_data: "/category " + vid.category_id }
  ],
  [
    { text: "📂 All Categories", callback_data: "/categories" },
    { text: "🏠 Main Menu", callback_data: "/start" }
  ]
];

Api.sendVideo({
  chat_id: chat.chatid,
  video: vid.file_id,
  caption: caption,
  parse_mode: "Markdown",
  supports_streaming: true,
  reply_markup: {
    inline_keyboard: inlineKeyboard
  }
});
