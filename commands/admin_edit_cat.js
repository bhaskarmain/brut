/*CMD
command: /admin_edit_cat
help: List categories to edit or delete
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
  Bot.sendInlineKeyboard(buttons, "⚠️ No categories exist yet.");
  return;
}

let buttons = [];
for (let i = 0; i < categories.length; i++) {
  let cat = categories[i];
  buttons.push([{
    title: (cat.emoji || "📁") + " " + cat.name,
    command: "/admin_cat_detail " + cat.id
  }]);
}

buttons.push([{ title: "🔙 Back to Admin", command: "/admin" }]);

Bot.sendInlineKeyboard(buttons, "✏️ *Select a Category to Edit or Delete:*");

