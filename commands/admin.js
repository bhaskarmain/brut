/*CMD
command: /admin
help: Administrative Control Dashboard
need_reply: false
auto_retry_time: 
folder: 
answer: 
keyboard: 
aliases: 
group: 
CMD*/

// Initialize admin IDs if not configured yet
let adminIds = Bot.getProperty("admin_ids");
if (!adminIds || adminIds.length === 0) {
  adminIds = [user.telegramid];
  Bot.setProperty("admin_ids", adminIds, "json");
}

// Check admin authorization
if (adminIds.indexOf(user.telegramid) === -1 && adminIds.indexOf(String(user.telegramid)) === -1) {
  Bot.sendMessage("🚫 *Access Denied:* You are not authorized to access the Admin Panel.");
  return;
}

let buttons = [
  [
    { title: "📤 Upload Video", command: "/admin_upload" },
    { title: "📂 Add Category", command: "/admin_add_cat" }
  ],
  [
    { title: "📋 Manage Videos", command: "/admin_manage_vids" },
    { title: "✏️ Edit Category", command: "/admin_edit_cat" }
  ],
  [
    { title: "🗑 Delete Video", command: "/admin_del_vid_menu" },
    { title: "👥 All Users", command: "/admin_users" }
  ],
  [
    { title: "📊 Bot Statistics", command: "/admin_stats" },
    { title: "🎁 Referral Settings", command: "/admin_ref_settings" }
  ],
  [
    { title: "📢 Broadcast Message", command: "/admin_broadcast" },
    { title: "🚫 Ban/Unban User", command: "/admin_ban" }
  ],
  [
    { title: "⚙️ Bot Settings", command: "/admin_settings" },
    { title: "🔙 User Panel", command: "/start" }
  ]
];

let text =
  "🛠 *Smart Video Bot — Admin Dashboard*\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  "Welcome Administrator! Select a management module below 👇";

Bot.sendInlineKeyboard(buttons, text);

