/*CMD
command: /admin_add_cat_step2
help: Save new category
need_reply: true
auto_retry_time: 
folder: 
answer: 
keyboard: 
aliases: 
group: 
CMD*/

let name = User.getProperty("new_cat_name");
let emoji = (message && message.trim() !== "/skip") ? message.trim().substring(0, 4) : "📁";

let categories = Bot.getProperty("categories") || [];
let newId = Date.now();

categories.push({
  id: newId,
  name: name,
  emoji: emoji
});

Bot.setProperty("categories", categories, "json");
User.setProperty("new_cat_name", null, "string");

let buttons = [
  [{ title: "📂 Add Another Category", command: "/admin_add_cat" }],
  [{ title: "🛠 Admin Dashboard", command: "/admin" }]
];

Bot.sendInlineKeyboard(
  buttons,
  "✅ *Category Created Successfully!*\n\n" +
  "🆔 ID: " + newId + "\n" +
  "📂 Name: " + emoji + " " + name
);

