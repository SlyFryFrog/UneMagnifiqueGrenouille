# Brief Introduction

This discord bot, Une Magnifique Grenouille, serves the purpose of enabling guild members to learn more about frogs. This is still in its beta stage, so some features may not be fully developed or finalized.

# How To Use

To run the bot, you will first need to create a **.env** file and put it ino the **resources** folder. After you have done that, copy the following into it.

DISCORD_BOT_TOKEN={your discord token}

BETA_BOT_TOKEN={optional second token}

# Public Commands

"!help_frog" - Responds with a generic help message to assist the user.

"!frog {frog name}" - Responds with a detailed description of the requested frog. Currently, however, this command is still in development.

"!frog_me" - Responds to the user with a random frog. If an image is available, the bot will also send an image alongside the text.

"!frog_fact" - Responds to the user with a random frog fact about a random frog. This command ***does not*** use the facts specifically made for the daily command.

# Admin Only Commands

"!subscribe_channel" - Subscribes the channel from which the command was sent. The channel will then receive a daily frog fact that is different from the "!frog_fact" command. The bot will send the fact daily at 12pm EST.

"!unsubscribe_channel" - Unsubscribes the channel from receiving a daily frog fact. It ***does not*** need to be used in the same channel as the one originally subscribe.

# Additional Info

Have questions or suggestions? If so, feel free to join my discord server. https://discord.gg/vGTvxHGKvG