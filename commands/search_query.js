/*CMD
command: /search_query
help: Execute search query across all videos
need_reply: true
auto_retry_time: 
folder: 
answer: 
keyboard: 
aliases: 
group: 
CMD*/

if (!message || message.trim().length < 2) {
  Bot.sendMessage("⚠️ Search term must be at least 2 characters. Try again or send /start:");
  Bot.run({ command: "/search_query" });
  return;
}

let query = message.trim().toLowerCase();
let videos = Bot.getProperty("videos") || [];
let results = [];

for (let i = 0; i < videos.length; i++) {
  let v = videos[i];
  let titleMatch = v.title && v.title.toLowerCase().indexOf(query) > -1;
  let descMatch = v.description && v.description.toLowerCase().indexOf(query) > -1;
  if (titleMatch || descMatch) {
    results.push(v);
  }
}

let buttons = [];

if (results.length === 0) {
  buttons.push([
    { title: "🔍 Search Again", command: "/search" },
    { title: "📂 Browse Categories", command: "/categories" }
  ]);
  buttons.push([{ title: "🏠 Main Menu", command: "/start" }]);
  Bot.sendInlineKeyboard(
    buttons,
    "🔍 *No matching videos found for:* `" + message.trim() + "`\n\nTry a different keyword or browse categories 👇"
  );
  return;
}

// Display top 8 results
let displayCount = Math.min(results.length, 8);
for (let i = 0; i < displayCount; i++) {
  let v = results[i];
  let shortTitle = v.title.length > 28 ? v.title.substring(0, 28) + "..." : v.title;
  buttons.push([{ title: "▶️ " + shortTitle, command: "/video_info " + v.id }]);
}

buttons.push([
  { title: "🔍 New Search", command: "/search" },
  { title: "📂 All Categories", command: "/categories" }
]);
buttons.push([{ title: "🏠 Main Menu", command: "/start" }]);

let text =
  "🔍 *Search Results for:* `" + message.trim() + "`\n" +
  "Found *" + results.length + "* matching video(s):\n\n" +
  "Select a video below to stream 👇";

Bot.sendInlineKeyboard(buttons, text);

