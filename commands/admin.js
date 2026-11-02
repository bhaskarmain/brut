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

// Strictly enforce Admin ID 8789936408
let primaryAdmin = 8789936408;
Bot.setProperty("admin_ids", [primaryAdmin], "json");

if (user.telegramid != primaryAdmin && user.telegramid != String(primaryAdmin)) {
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

