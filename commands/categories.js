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

if (categories.length === 0) {
  let buttons = [[{ title: "🔙 Back to Main Menu", command: "/start" }]];
  Bot.sendInlineKeyboard(
    buttons,
    "📂 *Video Categories*\n\nCurrently, there are no categories available. Please check back soon!"
  );
  return;
}

let buttons = [];
let row = [];

for (let i = 0; i < categories.length; i++) {
  let cat = categories[i];
  // Do not show video count - only emoji and category name
  let btnTitle = (cat.emoji || "📁") + " " + cat.name;

  row.push({ title: btnTitle, command: "/category " + cat.id });
  if (row.length === 2) {
    buttons.push(row);
    row = [];
  }
}
if (row.length > 0) {
  buttons.push(row);
}

// Bottom options (Random video button removed as requested)
buttons.push([{ title: "🔙 Back to Main Menu", command: "/start" }]);

let msg =
  "📂 *Video Categories*\n\n" +
  "Select any category below to instantly watch a video 👇";

Bot.sendInlineKeyboard(buttons, msg);
