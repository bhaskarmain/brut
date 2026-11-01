/*CMD
command: /daily_bonus
help: Daily free video reward claim
need_reply: false
auto_retry_time: 
folder: 
answer: 
keyboard: 
aliases: 
group: 
CMD*/

let lastClaim = User.getProperty("last_daily_claim");
let now = Date.now();
let cooldown = 24 * 60 * 60 * 1000; // 24 hours in ms

if (lastClaim && (now - lastClaim < cooldown)) {
  let diff = cooldown - (now - lastClaim);
  let hoursLeft = Math.ceil(diff / (60 * 60 * 1000));

  let buttons = [
    [{ title: "📂 Browse Categories", command: "/categories" }],
    [{ title: "🏠 Main Menu", command: "/start" }]
  ];
  Bot.sendInlineKeyboard(
    buttons,
    "⏰ *Daily Bonus Already Claimed!*\n\n" +
    "You have already claimed your daily bonus today.\n" +
    "Please come back in approximately *" + hoursLeft + " hour(s)* for your next free daily video!"
  );
  return;
}

let videos = Bot.getProperty("videos") || [];
if (videos.length === 0) {
  Bot.sendMessage("⚠️ No videos in the library yet. Please check back later!");
  return;
}

let watched = User.getProperty("watched_videos") || [];
let unwatched = [];
for (let i = 0; i < videos.length; i++) {
  if (watched.indexOf(videos[i].id) === -1) {
    unwatched.push(videos[i]);
  }
}

let pool = unwatched.length > 0 ? unwatched : videos;
let randomIndex = Math.floor(Math.random() * pool.length);
let bonusVid = pool[randomIndex];

// Update timestamp
User.setProperty("last_daily_claim", now, "integer");

// Record watch
if (watched.indexOf(bonusVid.id) === -1) {
  watched.push(bonusVid.id);
  User.setProperty("watched_videos", watched, "json");
}

let caption =
  "🎁 *DAILY BONUS VIDEO UNLOCKED!* 🌟\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  "🎬 *" + bonusVid.title + "*\n\n" +
  "_" + (bonusVid.description || "Here is your free daily bonus video!") + "_\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  "✨ _Come back in 24 hours for another daily surprise video!_";

let inlineKeyboard = [
  [
    { text: "🎲 Next Random Video", callback_data: "/random_video" },
    { text: "📂 Categories", callback_data: "/categories" }
  ],
  [{ text: "🏠 Main Menu", callback_data: "/start" }]
];

Api.sendVideo({
  chat_id: chat.chatid,
  video: bonusVid.file_id,
  caption: caption,
  parse_mode: "Markdown",
  supports_streaming: true,
  reply_markup: {
    inline_keyboard: inlineKeyboard
  }
});
