/*CMD
command: /category
help: Displays videos inside a category
need_reply: false
auto_retry_time: 
folder: 
answer: 
keyboard: 
aliases: 
group: 
CMD*/

let catId = parseInt(params);
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
    [{ title: "📂 All Categories", command: "/categories" }],
    [{ title: "🏠 Main Menu", command: "/start" }]
  ];
  Bot.sendInlineKeyboard(
    buttons,
    catEmoji + " *" + cat.name + "*\n\nNo videos have been uploaded to this category yet. Check back soon!"
  );
  return;
}

let buttons = [];
for (let i = 0; i < catVideos.length; i++) {
  let v = catVideos[i];
  let shortTitle = v.title.length > 28 ? v.title.substring(0, 28) + "..." : v.title;
  buttons.push([{ title: "▶️ " + shortTitle, command: "/video_info " + v.id }]);
}

buttons.push([
  { title: "📂 All Categories", command: "/categories" },
  { title: "🏠 Main Menu", command: "/start" }
]);

let msg =
  catEmoji + " *" + cat.name + "*\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  "Total Videos: *" + catVideos.length + "*\n\n" +
  "Select a video below to view details and stream 👇";

Bot.sendInlineKeyboard(buttons, msg);

