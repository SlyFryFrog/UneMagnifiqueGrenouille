import json
import string
import discord
import random
import asyncio
from discord.ext import commands


class FrogCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.frog_class = FrogMessage()
        self.frog_list = self.frog_class.get_frogs_list()

    @commands.command(name="frog_help")
    async def help(self, ctx):
        help_message = """**Commands**
!frog_help
!frog_me
!frog_fact
!frog {frog name}

**Admin Only**
!subscribe_channel
!unsubscribe_channel
        """
        await ctx.reply(help_message, mention_author=False)


    @commands.command(name="frog_me")
    async def frog_me(self, ctx):
        '''Responds with a message that contains a random frog'''

        frog = self.frog_class.get_frog()
        image = self.frog_class.get_frog_image(frog)

        message = f"You've been blessed with receiving a(n) {frog}!"

        if image:
            await ctx.reply(message, file=discord.File(image), mention_author=False)
        
        else:
            await ctx.reply(message, mention_author=False)


    @commands.command(name="frog_fact")
    async def frog_fact(self, ctx):
        '''Command for calling bot to send a random frog fact'''

        await ctx.reply(self.frog_class.get_frog_fact(daily=False), mention_author=False)
    

    @commands.command(name="frog")
    async def frog(self, ctx, *arg):

        def check(ctx1):
            '''Checks to see if author matches original author'''
            return ctx1.author.id == orig_author
        
        orig_author = ctx.author.id
        options = [
            "Taxonomy",
            "Locations",
            "Characteristics",
            "Conservation Status",
            "Image"
        ]

        # Converts list to string
        arg = " ".join(arg).title().strip()
        
        # Checks to see if the arg the user gave is valid
        if arg not in self.frog_list:
            return
                
        message = f'''**{arg}**
Taxonomy
Locations
Characteristics
Conservation Status
Image
        '''
        await ctx.reply(message, mention_author=False)

        # Waits for 30 seconds for a response from the original author
        # If no response is given, it stops listening for further args
        try:
            ctx1 = await self.bot.wait_for("message", 
                                           timeout=30.0, 
                                           check=check)

        except asyncio.TimeoutError:
            return
        
        if string.capwords(ctx1.content) in options:
            # Checks if user requested image
            if string.capwords(ctx1.content) == options[-1]:

                # Checks if there is an image path
                try:
                    image = self.frog_class.get_frog_image(arg)
                    message = f"**{string.capwords(ctx1.content)}**"

                    return await ctx1.reply(message, 
                                            file=discord.File(image),
                                            mention_author=False)

                except:
                    return await ctx1.reply("I apologize, it seems that there is no image for this frog at the moment.", 
                                            mention_author=False)

            message = self.frog_class.get_detailed_frog(category=ctx1.content, 
                                                        frog=arg)

            return await ctx1.reply(message, mention_author=False)

        else:
            return await ctx1.reply("Invalid option, please run the command again.", 
                                    mention_author=False)


    @commands.command(name="frog_list")
    async def frog_list(self, ctx):
        message = list(self.frog_class.get_frogs_list()).__iter__()
        output = "**Here's a list of all currently available frogs:**"
        
        # Converts list to string
        for item in message:
            output = f"{output}\n{item}"
        
        await ctx.reply(output, mention_author=False)


class FrogMessage:
    '''Creates message with frog facts'''
    def __init__(self):
        # Creates list of all frogs
        with open("resources/frogs.json", "r", encoding="utf-8") as file:
            self.frog_list = json.load(file)
        
        with open("resources/frog_facts.json", "r", encoding="utf-8") as file:
            self.frog_facts_dictionary = json.load(file)


    def get_frogs_list(self):
        '''Returns a list of frogs'''
        return self.frog_list


    def get_frog_fact(self, daily):
        '''Gets a frog fact about a random frog'''
        if daily:
            with open("resources/daily_frog_facts.json", "r", encoding="utf-8") as file:
                frog_facts = json.load(file)
            
            message = frog_facts[random.randint(0, len(frog_facts) - 1)]

        else:
            while True:
                frog = self.frog_list[random.randint(0, len(self.frog_list) - 1)]
                path = self.frog_facts_dictionary[frog]["fun fact"]
                
                # Checks if there is a frog fact entry for a specific frog
                if path:
                        
                    message = path[random.randint(0, len(path) - 1)]
                    break

                else:
                    continue
        
        return message


    def get_frog(self):
        '''Gets a random frog frog list'''
        self.frog = self.frog_list[random.randint(0, len(self.frog_list) - 1)]
        
        return self.frog
    
    
    def get_frog_image(self, frog):
        '''Gets image of frog, if no image path is found, returns None'''
        image = self.frog_facts_dictionary[frog]["image"]

        if image:
            return image[random.randint(0, len(image) - 1)]
        
        else:
            return None


    def get_detailed_frog(self, category, frog):
        '''Gives detailed information of frog'''
        category = category.lower()
        message = f"**{string.capwords(category)}**\n"
        path = self.frog_facts_dictionary[frog][category]

        if not path:
            message = "I apologize, it seems there is no information for that category for this particular frog at the moment."
            
        # String
        elif path == str(path):
            message = f"{message}{path}"

        # Loops for list
        elif path == list(path):
            for v in self.frog_facts_dictionary[frog][category]:
                message = f"{message}{v}\n"
            
        # Loops if dictionary
        else:
            for k, v in path.items():
                message = f"{message}{string.capwords(k).replace('_', ' ')} - {v}\n"
            
        return message


async def setup(bot):
    '''Adds custom commands to bot'''
    await bot.add_cog(FrogCommands(bot))