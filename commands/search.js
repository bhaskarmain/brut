/*CMD
command: /search
help: Search video library by keyword
need_reply: false
auto_retry_time: 
folder: 
answer: 
keyboard: 
aliases: 
group: 
CMD*/

let buttons = [[{ title: "🔙 Cancel & Return", command: "/start" }]];

Bot.sendInlineKeyboard(
  buttons,
  "🔍 *Search Video Library*\n\n" +
  "Type and send the *title or keyword* of the video you are looking for:"
);

Bot.run({ command: "/search_query" });
