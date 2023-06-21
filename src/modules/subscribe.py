import datetime
from discord.ext import commands, tasks

from src.modules.frog import FrogMessage
from src.config import read_config, update_guild_settings, default_config

daily_message_time = datetime.time(hour=16, tzinfo=datetime.timezone.utc)

class DailyCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild_id_list = read_config()
        self.daily_frog_fact.start()


    @tasks.loop(time=daily_message_time)
    async def daily_frog_fact(self):
        '''Function to send a random frog fact daily'''
        frog_class = FrogMessage()
        
        # Gets a random fact
        message = frog_class.get_frog_fact(daily=True)

        # Updates variable
        self.guild_id_list = read_config()
        
        for guild_id in self.guild_id_list:
            # Gets channel_id and sends daily message
            try:
                if self.guild_id_list[guild_id]["subscribe.daily"]["enabled"]:
                    channel_id = self.guild_id_list[guild_id]["subscribe.daily"]["channel.id"]
                    channel = self.bot.get_channel(int(channel_id))

                    await channel.send(f"Daily Frog Fact:\n{message}")
                    continue
                    
            except:
                if channel_id:
                    print(f"{channel_id} was not found, skipping...")
                
                else:
                    print("No channel was found, skipping...")

                continue
    #

    @commands.command(name="subscribe_channel")
    @commands.has_any_role("Administrator", "Admin", "Moderator", "Mod")
    async def subscribe_to_daily(self, ctx):
        guild_id = str(ctx.guild.id)

        # Checks if guild already has a daily message channel
        # If it does, checks if channel.id matches ctx channel
        # If it doesn't, it writes over the old channel.id
        
        if guild_id not in str(self.guild_id_list.keys()):
            # Gets template
            guild_config = default_config()
            
            self.guild_id_list[guild_id] = guild_config
            self.guild_id_list[guild_id]["subscribe.daily"]["enabled"] = True

            
        for guild in self.guild_id_list:
            if guild == guild_id:
                # Updates subscribed channel
                self.guild_id_list[guild_id]["subscribe.daily"]["enabled"] = True
                self.guild_id_list[guild_id]["subscribe.daily"]["channel.id"] = ctx.channel.id
                
                update_guild_settings(self.guild_id_list)
                
                await ctx.send("This channel has successfully enabled daily frog facts; they will be sent daily at 12pm EST.")
                break
                
            else:
                continue
    

    @commands.command(name="unsubscribe_channel")
    @commands.has_any_role("Administrator", "Admin", "Moderator", "Mod")
    async def unsubscribe_to_daily(self, ctx):
        '''Marks server as having the daily fact disabled'''
        guild_id = str(ctx.guild.id)

        if guild_id not in self.guild_id_list.keys():
            await ctx.reply("Daily frog facts were never enabled.", mention_author=False)
        else:
            for guild in self.guild_id_list:
                if guild == guild_id:
                    self.guild_id_list[guild_id]["subscribe.daily"]["enabled"] = False
                    self.guild_id_list[guild_id]["subscribe.daily"]["channel.id"] = None
                    update_guild_settings(self.guild_id_list)
                    
                    await ctx.send("All daily frog facts have been disabled successfully.")
                    break


async def setup(bot):
    await bot.add_cog(DailyCommands(bot))