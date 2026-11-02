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
    "🎬 *Watch Videos*\n\nCurrently, there are no categories available. Please check back soon!"
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

// Bottom options
buttons.push([{ title: "🔙 Back to Main Menu", command: "/start" }]);

let msg =
  "🎬 *Watch Videos*\n\n" +
  "Select a category below to instantly stream a random video 👇";

Bot.sendInlineKeyboard(buttons, msg);
