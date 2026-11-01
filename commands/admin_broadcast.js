/*CMD
command: /admin_broadcast
help: Broadcast announcement to all users
need_reply: true
auto_retry_time: 
folder: 
answer: 📢 *Broadcast Message to All Users*\n\nSend the text announcement you wish to broadcast to all registered users, or send /admin to cancel:
keyboard: 
aliases: 
group: 
CMD*/

if (!message || message.trim() === "/admin") {
  Bot.runCommand("/admin");
  return;
}

let textToBroadcast = message.trim();
let allUsers = Bot.getProperty("all_users_list") || [];

let successCount = 0;
let failCount = 0;

for (let i = 0; i < allUsers.length; i++) {
  let targetId = allUsers[i].id;
  try {
    Bot.sendMessageToChatWithId(targetId, textToBroadcast);
    successCount++;
  } catch (e) {
    failCount++;
  }
}

let summary =
  "📢 *Broadcast Completed!*\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  "👥 *Total Attempted:* " + allUsers.length + "\n" +
  "✅ *Delivered Successfully:* " + successCount + "\n" +
  "❌ *Failed / Blocked:* " + failCount + "\n" +
  "━━━━━━━━━━━━━━━━━━━━━";

let buttons = [[{ title: "🛠 Admin Dashboard", command: "/admin" }]];
Bot.sendInlineKeyboard(buttons, summary);

