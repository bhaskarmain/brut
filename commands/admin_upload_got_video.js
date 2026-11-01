/*CMD
command: /admin_upload_got_video
help: Step 3 of Video Upload - Receive Video File and Prompt for Title
need_reply: true
auto_retry_time: 
folder: 
answer: 
keyboard: 
aliases: 
group: 
CMD*/

let fileId = null;

if (request && request.video) {
  fileId = request.video.file_id;
} else if (request && request.message && request.message.video) {
  fileId = request.message.video.file_id;
} else if (request && request.document && request.document.mime_type && request.document.mime_type.indexOf("video") > -1) {
  fileId = request.document.file_id;
}

if (!fileId) {
  Bot.sendMessage("⚠️ No valid video file detected. Please send an MP4/MOV video, or send /admin to cancel:");
  Bot.run({ command: "/admin_upload_got_video" });
  return;
}

User.setProperty("upload_file_id", fileId, "string");

Bot.sendMessage("✅ *Video received!*\n\n📤 *Step 3 of 4:* Now enter a *Title* for this video:");
Bot.run({ command: "/admin_upload_got_title" });

