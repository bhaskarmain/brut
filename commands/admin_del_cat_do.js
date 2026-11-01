/*CMD
command: /admin_del_cat_do
help: Execute category deletion
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
  Bot.runCommand("/admin_edit_cat");
  return;
}

// Remove category
let categories = Bot.getProperty("categories") || [];
let newCats = [];
for (let i = 0; i < categories.length; i++) {
  if (categories[i].id !== catId) {
    newCats.push(categories[i]);
  }
}
Bot.setProperty("categories", newCats, "json");

// Cascade delete videos in that category
let videos = Bot.getProperty("videos") || [];
let newVids = [];
for (let i = 0; i < videos.length; i++) {
  if (videos[i].category_id !== catId) {
    newVids.push(videos[i]);
  }
}
Bot.setProperty("videos", newVids, "json");

let buttons = [[{ title: "🛠 Admin Dashboard", command: "/admin" }]];
Bot.sendInlineKeyboard(buttons, "✅ *Category and its associated videos have been deleted.*");

