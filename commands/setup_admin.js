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

let newAdminId = null;

if (params) {
  newAdminId = parseInt(params.trim());
} else {
  newAdminId = user.telegramid;
}

if (!newAdminId) {
  Bot.sendMessage("⚠️ Please provide a valid Telegram ID. Example: `/setup_admin 123456789`");
  return;
}

let adminIds = Bot.getProperty("admin_ids") || [];
if (adminIds.indexOf(newAdminId) === -1 && adminIds.indexOf(String(newAdminId)) === -1) {
  adminIds.push(newAdminId);
  Bot.setProperty("admin_ids", adminIds, "json");
}

let buttons = [[{ title: "🛠 Open Admin Panel", command: "/admin" }]];
Bot.sendInlineKeyboard(
  buttons,
  "👑 *Admin Setup Completed!*\n\nID `" + newAdminId + "` has been granted full Administrator access.\nTap below to open the Admin Dashboard:"
);

