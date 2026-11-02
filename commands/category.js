/*CMD
command: /category
help: Instantly streams a random video from the selected category
need_reply: false
auto_retry_time: 
folder: 
answer: 
keyboard: 
aliases: 
group: 
CMD*/

let parts = params ? params.trim().split(" ") : [];
let catId = parseInt(parts[0]);

if (!catId) {
  Bot.runCommand("/categories");
  return;
}

let categories = Bot.getProperty("categories") || [];
let cat = null;
for (let i = 0; i < categories.length; i++) {
  if (categories[i].id === catId) {
    cat = categories[i];
    break;
  }
}

if (!cat) {
  Bot.sendMessage("⚠️ Category not found.");
  Bot.runCommand("/categories");
  return;
}

let allVideos = Bot.getProperty("videos") || [];
let catVideos = [];
for (let i = 0; i < allVideos.length; i++) {
  if (allVideos[i].category_id === catId) {
    catVideos.push(allVideos[i]);
  }
}

let catEmoji = cat.emoji || "📁";

if (catVideos.length === 0) {
  let buttons = [
    [{ title: "🎬 Watch Videos", command: "/categories" }],
    [{ title: "🏠 Main Menu", command: "/start" }]
  ];
  Bot.sendInlineKeyboard(
    buttons,
    catEmoji + " *" + cat.name + "*\n\nNo videos have been uploaded to this category yet. Check back soon!"
  );
  return;
}

// Filter unwatched videos in this category
let watched = User.getProperty("watched_videos") || [];
let unwatched = [];
for (let i = 0; i < catVideos.length; i++) {
  if (watched.indexOf(catVideos[i].id) === -1) {
    unwatched.push(catVideos[i]);
  }
}

// Prioritize unwatched video, otherwise pick random from category
let pool = unwatched.length > 0 ? unwatched : catVideos;
let randomIndex = Math.floor(Math.random() * pool.length);
let selectedVid = pool[randomIndex];

// Update views
for (let i = 0; i < allVideos.length; i++) {
  if (allVideos[i].id === selectedVid.id) {
    allVideos[i].views = (allVideos[i].views || 0) + 1;
    break;
  }
}
Bot.setProperty("videos", allVideos, "json");

let totalViews = Bot.getProperty("total_views_count") || 0;
Bot.setProperty("total_views_count", totalViews + 1, "integer");

// Record on user
if (watched.indexOf(selectedVid.id) === -1) {
  watched.push(selectedVid.id);
  User.setProperty("watched_videos", watched, "json");
}

let userWatchedCount = User.getProperty("user_watched_count") || 0;
User.setProperty("user_watched_count", userWatchedCount + 1, "integer");

// Caption (Notice: No video count shown anywhere)
let descPart = selectedVid.description ? "\n\n📝 _" + selectedVid.description + "_" : "";
let caption =
  "🎬 *" + selectedVid.title + "*\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  "📂 *Category:* " + catEmoji + " " + cat.name +
  descPart + "\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  "✨ _Enjoy watching!_";

let inlineKeyboard = [
  [
    { text: "▶️ Next Video", callback_data: "/category " + cat.id }
  ],
  [
    { text: "🎬 Watch Videos", callback_data: "/categories" },
    { text: "🏠 Main Menu", callback_data: "/start" }
  ]
];

Api.sendVideo({
  chat_id: chat.chatid,
  video: selectedVid.file_id,
  caption: caption,
  parse_mode: "Markdown",
  supports_streaming: true,
  reply_markup: {
    inline_keyboard: inlineKeyboard
  }
});
