/*CMD
command: /admin_upload_got_video
help: Step 3 of Video Upload - Receive Video or ZIP File and Prompt for Title
need_reply: true
auto_retry_time: 
folder: 
answer: 
keyboard: 
aliases: 
group: 
CMD*/

let fileId = null;
let isZip = false;
let autoTitle = "";

let doc = (request && request.document) ? request.document : (request && request.message && request.message.document);
let vid = (request && request.video) ? request.video : (request && request.message && request.message.video);

if (vid) {
  fileId = vid.file_id;
} else if (doc) {
  fileId = doc.file_id;
  let fileName = doc.file_name ? doc.file_name.toLowerCase() : "";
  if (fileName.endsWith(".zip") || (doc.mime_type && doc.mime_type.indexOf("zip") > -1)) {
    isZip = true;
    autoTitle = doc.file_name ? doc.file_name.replace(/\.zip$/i, "").replace(/[_-]/g, " ") : "Video Archive";
  }
}

if (!fileId) {
  Bot.sendMessage("⚠️ No video or ZIP file detected. Please send an MP4 video or a .ZIP archive, or send /admin to cancel:");
  Bot.run({ command: "/admin_upload_got_video" });
  return;
}

User.setProperty("upload_file_id", fileId, "string");
User.setProperty("upload_is_zip", isZip, "boolean");
User.setProperty("upload_auto_title", autoTitle, "string");

if (isZip) {
  Bot.sendMessage(
    "📦 *ZIP Archive Received!*\n\n" +
    "⚡ *Automatic Extraction Mode Enabled:*\n" +
    "Enter a *Title* for this video pack, or send `/auto` to use: *" + autoTitle + "*:"
  );
} else {
  Bot.sendMessage("✅ *Video received!*\n\n📤 *Step 3 of 4:* Now enter a *Title* for this video:");
}

Bot.run({ command: "/admin_upload_got_title" });
