from discord.ext import commands
from discord.ext.commands import CommandNotFound, MissingAnyRole, CommandInvokeError


class CommandErrors(commands.Cog):
    '''Checks for what command error was raised'''
    def __init__(self, bot):
        pass
    
    # Prevents command-related errors from appearing and crashing bot
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        
        if isinstance(error, CommandNotFound):
            # Prevents harmless errors caused by
            # user typo from appearing in console
            return
            
        elif isinstance(error, MissingAnyRole):
            await ctx.reply(f"""Failed to perform command: Missing neccessary role.
                            Please try again with one of the following roles: 'Administrator,' 'Admin,' 'Moderator,' or 'Mod.'""", 
                            mention_author=False)
            return
        
        elif isinstance(error, CommandInvokeError):
            return
        
        else:
            raise error


async def setup(bot):
    await bot.add_cog(CommandErrors(bot))