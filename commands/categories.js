/*CMD
command: /categories
help: Browse video categories and show balance
need_reply: false
auto_retry_time: 
folder: 
answer: 
keyboard: 
aliases: 
group: 
CMD*/

let isAdmin = (user.telegramid == 8789936408 || user.telegramid == "8789936408");
let validReferrals = Bot.getProperty("ref_count_" + user.telegramid) || 0;
let rewardsClaimed = User.getProperty("rewards_claimed") || 0;
let currentBalance = isAdmin ? "Unlimited (Admin)" : Math.max(0, validReferrals - rewardsClaimed);

let categories = Bot.getProperty("categories") || [];

if (categories.length === 0) {
  let buttons = [[{ title: "🔙 Back to Main Menu", command: "/start" }]];
  Bot.sendInlineKeyboard(
    buttons,
    "🎬 *Watch Videos*\n\nCurrently, there are no categories available. Please check back soon!"
  );
  return;
}

let buttons = [];
let row = [];

for (let i = 0; i < categories.length; i++) {
  let cat = categories[i];
  // Do not show video count - only emoji and category name
  let btnTitle = (cat.emoji || "📁") + " " + cat.name;

  row.push({ title: btnTitle, command: "/category " + cat.id });
  if (row.length === 2) {
    buttons.push(row);
    row = [];
  }
}
if (row.length > 0) {
  buttons.push(row);
}

// Balance notification button if low balance
if (!isAdmin && (validReferrals - rewardsClaimed) <= 0) {
  buttons.push([{ title: "🎁 Earn Balance (Invite Friends)", command: "/referral" }]);
}

// Bottom options
buttons.push([{ title: "🔙 Back to Main Menu", command: "/start" }]);

let notice = "";
if (!isAdmin && (validReferrals - rewardsClaimed) <= 0) {
  notice = "\n⚠️ _Notice: Your video balance is 0. Each video requires 1 referral credit!_\n";
}

let msg =
  "🎬 *Watch Videos*\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  "💳 *Available Video Balance:* *" + currentBalance + (isAdmin ? "" : " Video(s)") + "*\n" +
  "📌 *Rule:* 1 Referral = 1 Video" +
  notice +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  "Select a category below to stream a random video 👇";

Bot.sendInlineKeyboard(buttons, msg);
