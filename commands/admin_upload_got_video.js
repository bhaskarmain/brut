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
let autoTitle = "";

let doc = (request && request.document) ? request.document : (request && request.message && request.message.document);
let vid = (request && request.video) ? request.video : (request && request.message && request.message.video);

if (vid) {
  fileId = vid.file_id;
  autoTitle = (vid.file_name) ? vid.file_name.replace(/\.[^/.]+$/, "") : "Video Clip";
} else if (doc) {
  let fileName = doc.file_name ? doc.file_name.toLowerCase() : "";
  if (fileName.endsWith(".zip") || (doc.mime_type && doc.mime_type.indexOf("zip") > -1) || fileName.endsWith(".rar") || fileName.endsWith(".7z")) {
    Bot.sendMessage(
      "❌ *ZIP Archives Cannot Stream as Video!*\n\n" +
      "Telegram cannot extract or stream .ZIP files in its built-in video player. If a ZIP archive is uploaded, users only see a raw file download card (like CP3.zip) instead of a playable video.\n\n" +
      "✅ *How to upload:*\n" +
      "1. Extract the ZIP archive on your computer or mobile.\n" +
      "2. Send or forward the **MP4 or MOV video file(s)** directly here.\n\n" +
      "👉 *Please send an MP4 / MOV video now, or send /admin to cancel:*"
    );
    Bot.run({ command: "/admin_upload_got_video" });
    return;
  }
  fileId = doc.file_id;
  autoTitle = doc.file_name ? doc.file_name.replace(/\.[^/.]+$/, "").replace(/[_-]/g, " ") : "Video Clip";
}

if (!fileId) {
  Bot.sendMessage("⚠️ No video detected. Please send or forward an MP4/MOV video file, or send /admin to cancel:");
  Bot.run({ command: "/admin_upload_got_video" });
  return;
}

User.setProperty("upload_file_id", fileId, "string");
User.setProperty("upload_is_zip", false, "boolean");
User.setProperty("upload_auto_title", autoTitle, "string");

Bot.sendMessage(
  "✅ *Video received!*\n\n" +
  "📤 *Step 3 of 4:* Enter a *Title* for this video (or send `/auto` to use: *" + (autoTitle || "New Video") + "*):"
);

Bot.run({ command: "/admin_upload_got_title" });
