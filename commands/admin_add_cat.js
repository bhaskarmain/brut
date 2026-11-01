/*CMD
command: /admin_add_cat
help: Add a new category
need_reply: true
auto_retry_time: 
folder: 
answer: 📂 *Add New Category — Step 1 of 2*\n\nEnter the *Name* of the new category (e.g. Action, Comedy, Tutorials):
keyboard: 
aliases: 
group: 
CMD*/

if (!message || message.trim().length < 2) {
  Bot.sendMessage("⚠️ Category name must be at least 2 characters. Try again or send /admin to cancel:");
  Bot.run({ command: "/admin_add_cat" });
  return;
}

User.setProperty("new_cat_name", message.trim(), "string");

Bot.sendMessage(
  "📂 *Add New Category — Step 2 of 2*\n\n" +
  "Send an *emoji* for this category (e.g. 🎬, 🔥, 🎭, 🍿) or send `/skip` for default 📁:"
);

Bot.run({ command: "/admin_add_cat_step2" });

