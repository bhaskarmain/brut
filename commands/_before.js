/*CMD
command: @
help: Security filter executed before all commands
need_reply: false
auto_retry_time: 
folder: 
answer: 
keyboard: 
aliases: 
group: 
CMD*/

if (user) {
  let isBanned = Bot.getProperty("banned_" + user.telegramid);
  if (isBanned) {
    Bot.sendMessage("🚫 *Access Denied*\n\nYour account has been suspended by administrators.");
    return false;
  }
}

