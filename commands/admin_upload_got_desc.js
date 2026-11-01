/*CMD
command: /admin_upload_got_desc
help: Step 5 of Video Upload - Save Video into System
need_reply: true
auto_retry_time: 
folder: 
answer: 
keyboard: 
aliases: 
group: 
CMD*/

let desc = (message && message.trim() === "/skip") ? "" : (message || "").trim();

let catId = User.getProperty("upload_cat_id");
let fileId = User.getProperty("upload_file_id");
let title = User.getProperty("upload_title");

let videos = Bot.getProperty("videos") || [];
let newId = Date.now();

videos.push({
  id: newId,
  category_id: catId,
  file_id: fileId,
  title: title,
  description: desc,
  views: 0,
  created_at: new Date().toISOString()
});

Bot.setProperty("videos", videos, "json");

// Clean temporary properties
User.setProperty("upload_cat_id", null, "integer");
User.setProperty("upload_file_id", null, "string");
User.setProperty("upload_title", null, "string");

let buttons = [
  [{ title: "📤 Upload Another Video", command: "/admin_upload" }],
  [{ title: "🛠 Admin Dashboard", command: "/admin" }]
];

let summary =
  "🎉 *Video Uploaded Successfully!*\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  "🆔 *Video ID:* " + newId + "\n" +
  "🎬 *Title:* " + title + "\n" +
  "📝 *Description:* " + (desc || "None") + "\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  "The video is now live in the library!";

Bot.sendInlineKeyboard(buttons, summary);

