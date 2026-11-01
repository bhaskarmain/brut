/*CMD
command: /admin_set_ref_req
help: Change required referrals per reward
need_reply: true
auto_retry_time: 
folder: 
answer: ✏️ *Change Referral Requirement*\n\nEnter the number of referrals needed to unlock 1 free video (e.g. 1, 2, 3, 5):
keyboard: 
aliases: 
group: 
CMD*/

let newReq = parseInt(message);
if (!newReq || newReq < 1) {
  Bot.sendMessage("⚠️ Please enter a positive number (at least 1):");
  Bot.run({ command: "/admin_set_ref_req" });
  return;
}

Bot.setProperty("referrals_per_reward", newReq, "integer");

let buttons = [
  [{ title: "🎁 Referral Settings", command: "/admin_ref_settings" }],
  [{ title: "🛠 Admin Dashboard", command: "/admin" }]
];

Bot.sendInlineKeyboard(
  buttons,
  "✅ *Referral requirement updated! Users now need " + newReq + " referrals to claim 1 reward.*"
);

