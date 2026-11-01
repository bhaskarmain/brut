/*CMD
command: /admin_cat_detail
help: Details and delete option for a selected category
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
  Bot.runCommand("/admin_edit_cat");
  return;
}

let buttons = [
  [{ title: "🗑 Delete Category (and its videos)", command: "/admin_del_cat_do " + cat.id }],
  [
    { title: "🔙 Categories List", command: "/admin_edit_cat" },
    { title: "🛠 Admin Menu", command: "/admin" }
  ]
];

let text =
  "📂 *Category Details:*\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  "🆔 ID: `" + cat.id + "`\n" +
  "🏷 Name: " + (cat.emoji || "📁") + " " + cat.name + "\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  "Select an action:";

Bot.sendInlineKeyboard(buttons, text);

