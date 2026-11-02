/*CMD
command: /start
help: Starts the bot and displays the main dashboard
need_reply: false
auto_retry_time: 
folder: 
answer: 
keyboard: 
aliases: 
group: 
CMD*/

// 1. Check if user is banned
let isBanned = User.getProperty("is_banned");
if (isBanned) {
  Bot.sendMessage("🚫 *Access Denied*\n\nYour account has been suspended by administrators.");
  return;
}

// 2. Register user & handle referral if new
let isRegistered = User.getProperty("is_registered");
if (!isRegistered) {
  User.setProperty("is_registered", true, "boolean");
  User.setProperty("rewards_claimed", 0, "integer");
  User.setProperty("watched_videos", [], "json");
  User.setProperty("joined_at", new Date().toISOString(), "string");

  // Track global user list
  let allUsers = Bot.getProperty("all_users_list") || [];
  allUsers.push({
    id: user.telegramid,
    name: user.first_name || "User",
    username: user.username || "",
    joined: new Date().toISOString()
  });
  Bot.setProperty("all_users_list", allUsers, "json");

  // Increment total users counter
  let totalUsers = Bot.getProperty("total_users_count") || 0;
  Bot.setProperty("total_users_count", totalUsers + 1, "integer");

  // Initialize seed categories if brand new bot
  let categories = Bot.getProperty("categories");
  if (!categories || categories.length === 0) {
    Bot.setProperty("categories", [
      { id: 1, name: "Action & Thriller", emoji: "💥" },
      { id: 2, name: "Comedy & Fails", emoji: "😂" },
      { id: 3, name: "Trailers & Clips", emoji: "🎬" }
    ], "json");
  }

  // Handle Referral
  if (params) {
    let cleanParam = params.toString().replace("ref_", "").replace("ref", "").trim();
    let refId = parseInt(cleanParam);

    // Anti-Cheat: cannot refer self, must be valid number
    if (refId && refId != user.telegramid) {
      let refEnabled = Bot.getProperty("referral_enabled");
      if (refEnabled !== false) {
        // Increment referrer count
        let refCount = Bot.getProperty("ref_count_" + refId) || 0;
        let newCount = refCount + 1;
        Bot.setProperty("ref_count_" + refId, newCount, "integer");

        // Save referral history
        let refList = Bot.getProperty("ref_list_" + refId) || [];
        refList.push({
          id: user.telegramid,
          name: user.first_name || "Friend",
          username: user.username || "",
          date: new Date().toISOString()
        });
        Bot.setProperty("ref_list_" + refId, refList, "json");

        // Save referrer on user
        User.setProperty("referrer_id", refId, "string");

        // Global referral count
        let totalValid = Bot.getProperty("total_valid_referrals") || 0;
        Bot.setProperty("total_valid_referrals", totalValid + 1, "integer");

        // Notify referrer (1 referral = 1 video balance)
        let req = Bot.getProperty("referrals_per_reward") || 1;

        try {
          Bot.sendMessageToChatWithId(
            refId,
            "🎉 *New Referral Joined!*\n\n" +
            "User *" + (user.first_name || "Friend") + "* joined using your link!\n" +
            "• Total Referrals: *" + newCount + "*\n\n" +
            "🎁 *+1 Video Balance Credited!* Tap /categories to watch a video!"
          );
        } catch (e) {
          // If referrer chat unreachable
        }
      }
    }
  }
}

// 3. Render Main Menu with Buttons
let buttons = [
  [
    { title: "🎬 Watch Videos", command: "/categories" }
  ],
  [
    { title: "🌟 Daily Bonus", command: "/daily_bonus" }
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

// Show Admin button only for authorized admin 8789936408
if (user.telegramid == 8789936408 || user.telegramid == "8789936408") {
  buttons.push([{ title: "🛠 Open Admin Panel", command: "/admin" }]);
}

let welcomeText =
  "👋 *Welcome, " + (user.first_name || "Friend") + "!*\n\n" +
  "🎬 *Smart Video Reward Bot*\n\n" +
  "📌 *What you can do:*\n" +
  "• 🎬 *Watch Videos:* Choose a category to stream videos (1 referral = 1 video).\n" +
  "• 🌟 *Daily Bonus:* Claim a free surprise video every 24 hours!\n" +
  "• 🎁 *Referral Rewards:* Invite friends & earn *1 video per 1 referral*!\n" +
  "• 📊 *Track Stats:* Monitor your views, referrals, and rewards.\n\n" +
  "Select an option below to get started 👇";

Bot.sendInlineKeyboard(buttons, welcomeText);
