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
  "Send or forward the *video file (MP4 / MOV)* directly into this chat:\n\n" +
  "⚠️ *Important Notice regarding ZIP files:*\n" +
  "Telegram video player requires direct MP4/MOV video files. Telegram cannot extract or stream .ZIP archives in its video player (it sends as a raw file download). Please extract any ZIP archive on your device and send the MP4 videos directly!"
);

Bot.run({ command: "/admin_upload_got_video" });
