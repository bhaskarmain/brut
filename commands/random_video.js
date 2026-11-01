/*CMD
command: /random_video
help: Streams a random video
need_reply: false
auto_retry_time: 
folder: 
answer: 
keyboard: 
aliases: 
group: 
CMD*/

let videos = Bot.getProperty("videos") || [];
if (videos.length === 0) {
  let buttons = [[{ title: "🔙 Back to Main Menu", command: "/start" }]];
  Bot.sendInlineKeyboard(buttons, "⚠️ No videos available in the library yet. Please check back later!");
  return;
}

let watched = User.getProperty("watched_videos") || [];

// Filter unwatched videos
let unwatched = [];
for (let i = 0; i < videos.length; i++) {
  if (watched.indexOf(videos[i].id) === -1) {
    unwatched.push(videos[i]);
  }
}

// If user watched all, pick from all
let pool = unwatched.length > 0 ? unwatched : videos;
let randomIndex = Math.floor(Math.random() * pool.length);
let selectedVid = pool[randomIndex];

// Run play_video command with selected video ID
Bot.runCommand("/play_video " + selectedVid.id);

