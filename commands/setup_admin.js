/*CMD
command: /setup_admin
help: Add or configure an admin Telegram ID
need_reply: false
auto_retry_time: 
folder: 
answer: 
keyboard: 
aliases: 
group: 
CMD*/

// Fixed master administrator ID
let primaryAdmin = 8789936408;
Bot.setProperty("admin_ids", [primaryAdmin], "json");

if (user.telegramid != primaryAdmin && user.telegramid != String(primaryAdmin)) {
  Bot.sendMessage("🚫 *Access Denied:* Only user `" + primaryAdmin + "` is authorized as Administrator.");
  return;
}

let buttons = [[{ title: "🛠 Open Admin Panel", command: "/admin" }]];
Bot.sendInlineKeyboard(
  buttons,
  "👑 *Administrator Verified!*\n\nID `" + primaryAdmin + "` is configured as the Administrator.\nTap below to open the Admin Dashboard:"
);

