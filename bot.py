import discord
from discord.ext import commands
import time
import json
import libneko
import asyncio


bot = commands.Bot(command_prefix=';', description='bruh.')

def is_owner():
    async def predicate(ctx):
        return ctx.author.id == 268085347462676480
    return commands.check(predicate)




with open('words.json') as fp:
    words = json.load(fp)

with open('token.txt') as fp:
    token = fp.read().strip()


#Defines a bot's prefix and description. There is one predefined command in the bot, the help command. This command shows you the full list of commands you have created.

@bot.event
async def on_ready():
    game = discord.Game("with the API")
    await bot.change_presence(activity=game)
    print("I\'m here!")


@bot.listen()
async def on_command_error(ctx, error):
    cause = error.__cause__ if error.__cause__ else error

    if isinstance(cause, commands.CheckFailure):
        await ctx.send(embed=libneko.Embed(title='That command is for <@268085347462676480> only!'))


@bot.listen()
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content.lower()
    for word, response in words.items():
        if content.startswith(word.lower()):
            return await message.channel.send(f'{message.author.mention}, {response}')



#The @bot.event defines a bot event. The on_ready event occurs when the bot is ready / is logged in to the Client. In this example, the "I'm here!" message will be printed to the console.

@bot.command()
async def say(ctx, *, something):
    """Say something!"""
    if something is None:
        await ctx.send("What do you want to say?")
        return

    await ctx.send(f"{ctx.message.author.mention} said: **{something}**")

@bot.command()
async def ping(ctx):
    """Pong!"""
    await ctx.send("Pong!")

@bot.command()
@is_owner()
async def presence(ctx, *, newpresence):
    """Change presence (Bot Owner Only)"""
    game = discord.Game(f"{newpresence}")
    await bot.change_presence(activity=game)
    await ctx.send(embed=libneko.Embed(title=f'Set presence to `{newpresence}`'))

@bot.command()
async def suggest(ctx, *, suggestion):
    """Suggest a feature to <@268085347462676480>"""
    creator = (await bot.application_info()).owner
    await creator.send(f"New suggestion from {ctx.message.author.mention}: {suggestion}")
    await ctx.send(embed=libneko.Embed(title=f'Your suggestion has been sent: {suggestion}'))

@bot.command()
@is_owner()
async def update(ctx):
    with ctx.typing():
        await ctx.bot.update()



bot.run(token)
