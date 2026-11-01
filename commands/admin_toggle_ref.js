/*CMD
command: /admin_toggle_ref
help: Toggle referral system enabled or disabled
need_reply: false
auto_retry_time: 
folder: 
answer: 
keyboard: 
aliases: 
group: 
CMD*/

let isEnabled = Bot.getProperty("referral_enabled");
let newState = (isEnabled === false) ? true : false;

Bot.setProperty("referral_enabled", newState, "boolean");

let stateText = newState ? "enabled" : "disabled";
Bot.sendMessage("✅ Referral system has been *" + stateText + "*!");

Bot.runCommand("/admin_ref_settings");

