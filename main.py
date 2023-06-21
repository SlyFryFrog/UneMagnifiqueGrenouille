import discord
import os
import asyncio
from dotenv import load_dotenv
from discord.ext import commands

from src.modules.subscribe import DailyCommands
from src.config import default_config, read_config, update_guild_settings

class GrenouilleBot:
    '''Initializes bot'''
    def __init__(self, beta):
        self.beta = beta
        asyncio.run(self.create_grenouille())
        self.run_bot()

        
    def run_bot(self):
        
        # BOT LOGIN
        @self.bot.event
        async def on_ready():
            # Performs actions when bot successfully connects
            await self.bot.change_presence(activity=discord.Game("Studying frogs | Étudier les grenouilles"))
            DailyCommands(self.bot)

            print(f"{self.bot.user} has successfully connected.")
        

        @self.bot.event
        async def on_guild_join(guild):
            guild_id = str(guild.id)
            

            guild_config = default_config()
            guild_id_list = read_config()
            
            guild_id_list[guild_id] = guild_config

            update_guild_settings(guild_id_list)

            print(f"I've successfully joined {guild_id} and configured their default settings.")


        @self.bot.event
        async def on_guild_remove(guild):
            guild_id = str(guild.id)    

            guild_id_list = read_config()

            del guild_id_list[guild_id]
            update_guild_settings(guild_id_list)

        
        # Checks for discord token
        try:
            load_dotenv("resources/.env")

            if self.beta:
                self.bot.run(os.getenv('BETA_BOT_TOKEN'))

            else:
                self.bot.run(os.getenv('DISCORD_BOT_TOKEN'))

        
        except TypeError:
            print("ERROR: COULD NOT LOCATE DISCORD TOKEN\nEXITING...")
            raise SystemExit


    async def create_grenouille(self):
        '''Sets default settings needed for bot'''
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True

        if self.beta:
            self.bot = commands.Bot(command_prefix='!b', intents=intents)
        
        else:
            self.bot = commands.Bot(command_prefix='!', intents=intents)

        
        # Adds all discord cogs
        directory = "src/modules/"
        cog_dir = directory.replace("/", ".")
        
        for file in os.listdir(directory):
            
            if file.endswith(".py"):
                # Tries to load cog, if it fails or doesn't have
                # setup function, then it safely ignore the file
                try:
                    await self.bot.load_extension(f"{cog_dir}{file.rstrip('.py')}")

                except:
                    print(f"{file}.py gave an error when loading and as such was skipped.")
                    continue

        return


if __name__ == '__main__':
    GrenouilleBot(beta=False)