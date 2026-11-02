/*CMD
command: /admin_upload_got_title
help: Step 4 of Video Upload - Receive Title and Prompt for Description
need_reply: true
auto_retry_time: 
folder: 
answer: 
keyboard: 
aliases: 
group: 
CMD*/

let titleText = message ? message.trim() : "";
let autoTitle = User.getProperty("upload_auto_title");

if (titleText === "/auto" && autoTitle) {
  titleText = autoTitle;
}

if (!titleText || titleText.length < 2) {
  Bot.sendMessage("⚠️ Title must be at least 2 characters. Please enter a valid title:");
  Bot.run({ command: "/admin_upload_got_title" });
  return;
}

User.setProperty("upload_title", titleText, "string");

Bot.sendMessage(
  "📤 *Step 4 of 4:* Enter a *Description* for this content, or send `/skip` for no description:"
);
Bot.run({ command: "/admin_upload_got_desc" });
