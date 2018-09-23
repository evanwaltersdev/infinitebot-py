import discord
from discord.ext import commands
import time
import json
import libneko
import asyncio
import logging
from datetime import datetime
import traceback

bot = commands.Bot(command_prefix=';')

with open('words.json') as fp:
    words = json.load(fp)

with open('token.txt') as fp:
    token = fp.read().strip()


#Defines a bot's prefix and description. There is one predefined command in the bot, the help command. This command shows you the full list of commands you have created.

bot.load_extension('libneko.extras.superuser')

@bot.event
async def on_ready():
    game = discord.Game(f"with {len(bot.guilds)} servers")
    await bot.change_presence(activity=game)
    print("I\'m here!")


@bot.listen()
async def on_command_error(ctx, error):
    cause = error.__cause__ if error.__cause__ else error

    if isinstance(cause, commands.CheckFailure):
        await ctx.send(embed=libneko.Embed(title='You don\'t have permission to run that command!'))



#@bot.listen()
#async def on_message(message):
    #if message.author == bot.user:
        #return

    #content = message.content.lower()
    #for word, response in words.items():
        #if content.startswith(word.lower()):
            #return await message.channel.send(f'{message.author.mention}, {response}')

# Set up logging
logging.basicConfig(level='INFO')
logger = logging.getLogger('bot.py')

extensions = ['extensions.misc', 'extensions.moderation', 'extensions.utility']   # add more here later



# If we fail to load an extension, we just leave it out.
for extension in extensions:
    try:
        bot.load_extension(extension)
    except Exception:
        logger.error(f'Failed to load {extension} with error:\n{traceback.format_exc()}')














bot.run(token)
