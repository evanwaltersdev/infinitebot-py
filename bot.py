import discord
from discord.ext import commands
import time
import json
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
    game = discord.Game(f"with {len(bot.guilds)} servers")
    await bot.change_presence(activity=game)
    print("I\'m here!")


@bot.listen()
async def on_command_error(ctx, error):
    cause = error.__cause__ if error.__cause__ else error

    if isinstance(cause, commands.CheckFailure):
        await ctx.send(embed=discord.Embed(title='That command is for <@268085347462676480> only!'))


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
    await ctx.send(embed=discord.Embed(title=f'Set presence to `{newpresence}`'))

@bot.command()
async def suggest(ctx, *, suggestion):
    """Suggest a feature to <@268085347462676480>"""
    creator = (await bot.application_info()).owner
    await creator.send(f"New suggestion from {ctx.message.author.mention}: {suggestion}")
    embed=discord.Embed(title=f'Your suggestion has been sent: {suggestion}')
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=f"{ctx.author.avatar_url_as(size=1024)}")
    await ctx.send(embed=embed)


@bot.command()
async def avatar(ctx, *, user: discord.Member = None):
    """ Get the avatar of you or someone else """
    if user is None:
        user = ctx.author

    embed=discord.Embed(title=f"{user.name}\'s avatar", url=f"{user.avatar_url_as(size=1024)}")
    embed.set_image(url=f"{user.avatar_url_as(size=1024)}")
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=f"{ctx.author.avatar_url_as(size=1024)}")
    await ctx.send(embed=embed)

@bot.command()
async def serverinfo(ctx):
    """Get info about the current server"""
    dt = ctx.guild.created_at
    embed = discord.Embed(title=ctx.guild.name)
    embed.add_field(name="Server Name:", value=ctx.guild.name, inline=True)
    embed.add_field(name="Server Owner:", value=f"{ctx.guild.owner}", inline=True)
    embed.add_field(name="Members:", value=f"{ctx.guild.member_count}", inline=True)
    embed.add_field(name="Server Region:", value=f"{ctx.guild.region}", inline=True)
    embed.add_field(name="Created at:", value=dt.strftime('%d/%m/%y at %H:%M'), inline=True)
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=f"{ctx.author.avatar_url_as(size=1024)}")
    await ctx.send(embed=embed)

@bot.command()
async def userinfo(ctx, *, user: discord.Member = None):
    """Get info about a user"""
    if user is None:
        user = ctx.author
    embed = discord.Embed(title=f"{user.name}#{user.discriminator}")
    embed.add_field(name="ID:", value=user.id, inline=True)
    embed.add_field(name="Nickname:", value=user.nick, inline=True)
    embed.add_field(name="Mention:", value=user.mention, inline=True)
    embed.add_field(name="Joined at:", value=user.joined_at.strftime('%d/%m/%y at %H:%M'), inline=True)
    embed.add_field(name="Created at:", value=user.created_at.strftime('%d/%m/%y at %H:%M'), inline=True)
    embed.set_thumbnail(url=user.avatar_url_as(size=1024))
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=f"{ctx.author.avatar_url_as(size=1024)}")
    await ctx.send(embed=embed)


bot.run(token)
