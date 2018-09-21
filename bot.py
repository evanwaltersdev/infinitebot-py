import discord
from discord.ext import commands
import time
import json
import libneko
import asyncio
import logging
from datetime import datetime


logging.basicConfig(level='INFO')
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



#The @bot.event defines a bot event. The on_ready event occurs when the bot is ready / is logged in to the Client. In this example, the "I'm here!" message will be printed to the console.

def format_seconds(total_seconds: float, *, precision: int=None) -> str:
    """
    Formats a number of seconds into meaningful units.

    If precision is specified as an int, then only this many of the largest non-zero
    units will be output in the string. Else, all will:

        >>> age = datetime.utcnow() - user.created_at
        >>> age_string = format_seconds(age.total_seconds(), precision=3)
        >>> print(age_string)
        33 days, 14 minutes, 12 seconds
    """

    mins, secs = divmod(total_seconds, 60)
    hrs, mins = divmod(mins, 60)
    days, hrs = divmod(hrs, 24)
    months, days = divmod(days, 30)
    years, months = divmod(months, 12)

    fmt = lambda n, word: n and f'{n:.0f} {word}{int(n) - 1 and "s" or ""}' or ''

    queue = [
        fmt(years, 'year'),
        fmt(months, 'month'),
        fmt(days, 'day'),
        fmt(hrs, 'hour'),
        fmt(mins, 'minute'),
        fmt(secs, 'second')
    ]
    queue = [*filter(None, queue)]

    if precision:
        queue = queue[:precision]

    return ', '.join(queue) or 'just now'


@bot.command()
async def say(ctx, *, something):
    """Say something!"""
    if something is None:
        await ctx.send("What do you want to say?")
        return

    await ctx.send(f"{ctx.message.author.mention} said: **{something}**")

@bot.command()
async def ping(ctx):
    # Time the time required to send a message first.
    # This is the time taken for the message to be sent, awaited, and then
    # for discord to send an ACK TCP header back to you to say it has been
    # received; this is dependant on your bot's load (the event loop latency)
    # and generally how shit your computer is, as well as how badly discord
    # is behaving.
    start = time.monotonic()
    msg = await ctx.send('Pinging...')
    millis = (time.monotonic() - start) * 1000

    # Since sharded bots will have more than one latency, this will average them if needed.
    heartbeat = ctx.bot.latency * 1000

    await msg.edit(content=f'Heartbeat: {heartbeat:,.2f}ms\tACK: {millis:,.2f}ms.')

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
    embed=libneko.Embed(title=f'Your suggestion has been sent: {suggestion}')
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=f"{ctx.author.avatar_url_as(size=1024)}")
    await ctx.send(embed=embed)


@bot.command()
async def avatar(ctx, *, user: discord.Member = None):
    """ Get the avatar of you or someone else """
    if user is None:
        user = ctx.author

    embed=libneko.Embed(title=f"{user.name}\'s avatar", url=f"{user.avatar_url_as(size=1024)}")
    embed.set_image(url=f"{user.avatar_url_as(size=1024)}")
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=f"{ctx.author.avatar_url_as(size=1024)}")
    await ctx.send(embed=embed)

@bot.command()
async def serverinfo(ctx):
    """Get info about the current server"""
    dt = ctx.guild.created_at
    embed = libneko.Embed(title=ctx.guild.name)
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
    embed = libneko.Embed(title=f"{user.name}#{user.discriminator}")
    embed.add_field(name="ID:", value=user.id, inline=True)
    embed.add_field(name="Nickname:", value=user.nick, inline=True)
    embed.add_field(name="Mention:", value=user.mention, inline=True)
    embed.add_field(name="Joined at:", value=user.joined_at.strftime('%d/%m/%y at %H:%M'), inline=True)
    embed.add_field(name="Created at:", value=user.created_at.strftime('%d/%m/%y at %H:%M'), inline=True)
    embed.set_thumbnail(url=user.avatar_url_as(size=1024))
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=f"{ctx.author.avatar_url_as(size=1024)}")
    await ctx.send(embed=embed)

@bot.command()
async def git(ctx, *, user: discord.Member = None):
    """Link to Berg's git repo"""
    if user is None:
        user = ctx.author
    await ctx.message.delete()
    await ctx.send(f"{user.mention}, https://github.com/evanwaltersdev/infinitebot-py")

@bot.command()
async def accountage(ctx, *, user: discord.Member = None):
    """Determines age of account"""

    if user is None:
        user = ctx.author
        name = "Your"
    else:
        name = f"{user.mention}\'s"
    created = datetime.utcnow() - user.created_at
    created_string = format_seconds(created.total_seconds(), precision=3)
    description = f"{name} account was created {created_string} ago!"
    embed = libneko.Embed(description=description)
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=f"{ctx.author.avatar_url_as(size=1024)}")
    await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, num=None):
        """Purges a specified number of messages from the current channel."""
        await ctx.message.delete()
        username = ctx.message.mentions
        try:
            purge = int(num)
        except (ValueError, TypeError):
            purge = 100
        if len(username) == 0:
            if num == None:
                deleted = await ctx.channel.purge(
                    limit=100, check=lambda m: m.author == ctx.bot.user
                )
            else:
                deleted = await ctx.channel.purge(limit=int(purge))
        else:
            deleted = await ctx.channel.purge(
                limit=int(purge), check=lambda m: m.author == username[0]
            )
        await ctx.send(
            embed=discord.Embed(
                title=f"Deleted {len(deleted)} message(s)", color=0x9013fe
            ),
            delete_after=10,
        )


bot.run(token)
