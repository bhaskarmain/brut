/*CMD
command: /admin_upload
help: Step 1 of Video Upload - Choose Category
need_reply: false
auto_retry_time: 
folder: 
answer: 
keyboard: 
aliases: 
group: 
CMD*/

let categories = Bot.getProperty("categories") || [];
if (categories.length === 0) {
  let buttons = [[{ title: "🔙 Admin Menu", command: "/admin" }]];
  Bot.sendInlineKeyboard(buttons, "⚠️ No categories exist yet! Please add a category first via *Add Category*.");
  return;
}

let buttons = [];
let row = [];

for (let i = 0; i < categories.length; i++) {
  let cat = categories[i];
  row.push({
    title: (cat.emoji || "📁") + " " + cat.name,
    command: "/admin_upload_pickcat " + cat.id
  });
  if (row.length === 2) {
    buttons.push(row);
    row = [];
  }
}
if (row.length > 0) {
  buttons.push(row);
}

buttons.push([{ title: "❌ Cancel & Return", command: "/admin" }]);

let text =
  "📤 *Upload Video — Step 1 of 4*\n\n" +
  "Select the category for this video:";

Bot.sendInlineKeyboard(buttons, text);

