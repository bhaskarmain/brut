/*CMD
command: /admin_del_vid_do
help: Permanently delete a video
need_reply: false
auto_retry_time: 
folder: 
answer: 
keyboard: 
aliases: 
group: 
CMD*/

let vidId = parseInt(params);
if (!vidId) {
  Bot.runCommand("/admin_manage_vids");
  return;
}

let videos = Bot.getProperty("videos") || [];
let newVids = [];

for (let i = 0; i < videos.length; i++) {
  if (videos[i].id !== vidId) {
    newVids.push(videos[i]);
  }
}

Bot.setProperty("videos", newVids, "json");

let buttons = [
  [{ title: "📋 Back to Videos", command: "/admin_manage_vids" }],
  [{ title: "🛠 Admin Dashboard", command: "/admin" }]
];

Bot.sendInlineKeyboard(buttons, "✅ *Video was permanently deleted from the database.*");

