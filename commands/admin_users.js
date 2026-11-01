/*CMD
command: /admin_users
help: Registered users overview
need_reply: false
auto_retry_time: 
folder: 
answer: 
keyboard: 
aliases: 
group: 
CMD*/

let allUsers = Bot.getProperty("all_users_list") || [];
let totalCount = Bot.getProperty("total_users_count") || allUsers.length;

let rows = [];
let maxDisplay = Math.min(allUsers.length, 15);

for (let i = 0; i < maxDisplay; i++) {
  let u = allUsers[i];
  let refs = Bot.getProperty("ref_count_" + u.id) || 0;
  let uname = u.username ? " (@" + u.username + ")" : "";
  rows.push("• `" + u.id + "` — *" + u.name + "*" + uname + " | Refs: " + refs);
}

if (allUsers.length === 0) {
  rows.push("_No users registered yet._");
} else if (allUsers.length > 15) {
  rows.push("_...and " + (allUsers.length - 15) + " more users_");
}

let text =
  "👥 *Registered Users Overview*\n" +
  "Total Users: *" + totalCount + "*\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  rows.join("\n") +
  "\n━━━━━━━━━━━━━━━━━━━━━\n" +
  "Use *Ban/Unban User* to restrict or restore user access.";

let buttons = [
  [{ title: "🚫 Ban/Unban User by ID", command: "/admin_ban" }],
  [{ title: "🛠 Admin Dashboard", command: "/admin" }]
];

Bot.sendInlineKeyboard(buttons, text);

