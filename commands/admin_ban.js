/*CMD
command: /admin_ban
help: Ban or unban user by ID
need_reply: true
auto_retry_time: 
folder: 
answer: 🚫 *Ban/Unban User by Telegram ID*\n\nEnter the numeric Telegram User ID of the user you want to ban or unban, or send /admin to cancel:
keyboard: 
aliases: 
group: 
CMD*/

if (!message || message.trim() === "/admin") {
  Bot.runCommand("/admin");
  return;
}

let targetId = parseInt(message.trim());
if (!targetId) {
  Bot.sendMessage("⚠️ Invalid ID format. Please send a numeric Telegram ID:");
  Bot.run({ command: "/admin_ban" });
  return;
}

let isCurrentlyBanned = Bot.getProperty("banned_" + targetId);
let newBanState = !isCurrentlyBanned;

Bot.setProperty("banned_" + targetId, newBanState, "boolean");

let stateText = newBanState ? "🚫 BANNED" : "✅ UNBANNED";
let msg = "User `" + targetId + "` has been *" + stateText + "* successfully!";

let buttons = [
  [{ title: "🚫 Ban/Unban Another", command: "/admin_ban" }],
  [{ title: "🛠 Admin Dashboard", command: "/admin" }]
];

Bot.sendInlineKeyboard(buttons, msg);

