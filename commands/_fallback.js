/*CMD
command: *
help: Fallback command for unrecognized input
need_reply: false
auto_retry_time: 
folder: 
answer: 
keyboard: 
aliases: 
group: 
CMD*/

let buttons = [
  [
    { title: "🎬 Watch Videos", command: "/categories" }
  ],
  [
    { title: "🎁 Referral Rewards", command: "/referral" },
    { title: "👤 My Account", command: "/account" }
  ],
  [
    { title: "📊 My Statistics", command: "/stats" },
    { title: "ℹ️ Help", command: "/help" }
  ]
];

Bot.sendInlineKeyboard(buttons, "👋 Tap an option below to browse videos or manage your account:");

