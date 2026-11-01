/*CMD
command: /leaderboard
help: Displays referral leaderboard
need_reply: false
auto_retry_time: 
folder: 
answer: 
keyboard: 
aliases: 
group: 
CMD*/

let allUsers = Bot.getProperty("all_users_list") || [];
let leaderData = [];

for (let i = 0; i < allUsers.length; i++) {
  let u = allUsers[i];
  let refs = Bot.getProperty("ref_count_" + u.id) || 0;
  if (refs > 0) {
    leaderData.push({
      id: u.id,
      name: u.name || "User",
      refs: refs
    });
  }
}

// Sort descending by referrals
leaderData.sort(function(a, b) {
  return b.refs - a.refs;
});

let medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"];
let rows = [];

let topList = leaderData.slice(0, 10);
if (topList.length === 0) {
  rows.push("_No referrals yet. Be the first to invite friends and top the leaderboard!_");
} else {
  for (let i = 0; i < topList.length; i++) {
    let medal = i < medals.length ? medals[i] : "#" + (i + 1);
    rows.push(medal + " *" + topList[i].name + "* — *" + topList[i].refs + "* successful invites");
  }
}

let text =
  "🏆 *Top Referral Leaderboard*\n" +
  "━━━━━━━━━━━━━━━━━━━━━\n" +
  rows.join("\n") +
  "\n━━━━━━━━━━━━━━━━━━━━━\n" +
  "_Invite more friends to climb the leaderboard!_";

let buttons = [
  [{ title: "🔙 Back to Referral Dashboard", command: "/referral" }],
  [{ title: "🏠 Main Menu", command: "/start" }]
];

Bot.sendInlineKeyboard(buttons, text);

