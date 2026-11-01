/*CMD
command: /categories
help: Browse video categories
need_reply: false
auto_retry_time: 
folder: 
answer: 
keyboard: 
aliases: 
group: 
CMD*/

let categories = Bot.getProperty("categories") || [];
let videos = Bot.getProperty("videos") || [];

if (categories.length === 0) {
  let buttons = [[{ title: "🔙 Back to Main Menu", command: "/start" }]];
  Bot.sendInlineKeyboard(
    buttons,
    "📂 *Video Categories*\n\nCurrently, there are no categories available. Please check back soon!"
  );
  return;
}

// Calculate video count per category
let countMap = {};
for (let i = 0; i < videos.length; i++) {
  let cid = videos[i].category_id;
  countMap[cid] = (countMap[cid] || 0) + 1;
}

let buttons = [];
let row = [];

for (let i = 0; i < categories.length; i++) {
  let cat = categories[i];
  let cnt = countMap[cat.id] || 0;
  let btnTitle = (cat.emoji || "📁") + " " + cat.name + " (" + cnt + ")";

  row.push({ title: btnTitle, command: "/category " + cat.id });
  if (row.length === 2) {
    buttons.push(row);
    row = [];
  }
}
if (row.length > 0) {
  buttons.push(row);
}

// Bottom options
buttons.push([{ title: "🎲 Surprise Me (Random Video)", command: "/random_video" }]);
buttons.push([{ title: "🔙 Back to Main Menu", command: "/start" }]);

let msg =
  "📂 *Browse Video Categories*\n\n" +
  "Select a category below to explore videos, or hit *Surprise Me* for an instant random video 👇";

Bot.sendInlineKeyboard(buttons, msg);

