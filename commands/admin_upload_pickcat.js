/*CMD
command: /admin_upload_pickcat
help: Step 2 of Video Upload - Expect Video File
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
  Bot.runCommand("/admin_upload");
  return;
}

User.setProperty("upload_cat_id", catId, "integer");

let buttons = [[{ title: "❌ Cancel", command: "/admin" }]];
Bot.sendInlineKeyboard(
  buttons,
  "📤 *Upload Video — Step 2 of 4*\n\n" +
  "Now send or forward the *video file* directly into this chat:"
);

Bot.run({ command: "/admin_upload_got_video" });

