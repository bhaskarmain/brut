/*CMD
command: /category
help: Displays paginated videos inside a category
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
let page = parts.length > 1 ? parseInt(parts[1]) : 1;
if (!page || page < 1) { page = 1; }

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

let pageSize = 6;
let totalVideos = catVideos.length;
let totalPages = Math.ceil(totalVideos / pageSize) || 1;
if (page > totalPages) { page = totalPages; }

let startIndex = (page - 1) * pageSize;
let pageVideos = catVideos.slice(startIndex, startIndex + pageSize);

let buttons = [];
for (let i = 0; i < pageVideos.length; i++) {
  let v = pageVideos[i];
  let shortTitle = v.title.length > 28 ? v.title.substring(0, 28) + "..." : v.title;
  buttons.push([{ title: "▶️ " + shortTitle, command: "/video_info " + v.id }]);
}

// Pagination controls if more than 1 page
if (totalPages > 1) {
  let navRow = [];
  if (page > 1) {
    navRow.push({ title: "◀️ Prev", command: "/category " + catId + " " + (page - 1) });
  }
  navRow.push({ title: "📄 " + page + "/" + totalPages, command: "/category " + catId + " " + page });
  if (page < totalPages) {
    navRow.push({ title: "Next ▶️", command: "/category " + catId + " " + (page + 1) });
  }
  buttons.push(navRow);
}

buttons.push([
  { title: "📂 All Categories", command: "/categories" },
  { title: "🏠 Main Menu", command: "/start" }
]);

let msg =
  catEmoji + " *" + cat.name + "*\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  "Total Videos: *" + totalVideos + "* | Page *" + page + "/" + totalPages + "*\n\n" +
  "Select a video below to view details and stream 👇";

Bot.sendInlineKeyboard(buttons, msg);
