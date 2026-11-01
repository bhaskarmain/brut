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

if (!message || message.trim().length < 2) {
  Bot.sendMessage("⚠️ Title must be at least 2 characters. Please enter a valid title:");
  Bot.run({ command: "/admin_upload_got_title" });
  return;
}

User.setProperty("upload_title", message.trim(), "string");

Bot.sendMessage(
  "📤 *Step 4 of 4:* Enter a *Description* for this video, or send `/skip` if you prefer no description:"
);
Bot.run({ command: "/admin_upload_got_desc" });

