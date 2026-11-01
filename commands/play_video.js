/*CMD
command: /play_video
help: Streams the requested video directly to user
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
videos[vidIndex].views = (videos[vidIndex].views || 0) + 1;
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

// Stream video
let caption =
  "🎬 *" + vid.title + "*\n" +
  "📂 Category: " + catEmoji + " " + catName + "\n\n" +
  "_" + (vid.description || "") + "_";

Api.sendVideo({
  chat_id: chat.chatid,
  video: vid.file_id,
  caption: caption,
  parse_mode: "Markdown"
});

// Navigation buttons under video
let buttons = [
  [
    { title: "🎲 Next Random Video", command: "/random_video" },
    { title: "📂 Categories", command: "/categories" }
  ],
  [{ title: "🏠 Main Menu", command: "/start" }]
];

Bot.sendInlineKeyboard(buttons, "Enjoy watching! Select an option below 👇");

