import time
from discord.ext import commands
import libneko
from datetime import datetime
import time
import discord

# Notice that because we use a class, everything has an additional
# `self` parameter
class Utilities:
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
    
    def __init__(self, bot):
        self.bot = bot

    # Notice events now don't have a decorator!
    async def on_message(self, message):
        if message.author != self.bot.user and ' infinite ' in message.content.lower():
            await message.add_reaction('\N{OK HAND SIGN}')

    # Notice we do commands.command now, not bot.command.
    @commands.command()
    async def ping(self, ctx):
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


    @commands.command()
    @commands.is_owner()
    async def presence(self, ctx, *, newpresence):
        """Change presence (Bot Owner Only)"""
        game = discord.Game(f"{newpresence}")
        await bot.change_presence(activity=game)
        await ctx.send(embed=libneko.Embed(title=f'Set presence to `{newpresence}`'))


    @commands.command()
    async def avatar(self, ctx, *, user: discord.Member = None):
        """ Get the avatar of you or someone else """
        if user is None:
            user = ctx.author

        embed=libneko.Embed(title=f"{user.name}\'s avatar", url=f"{user.avatar_url_as(size=1024)}")
        embed.set_image(url=f"{user.avatar_url_as(size=1024)}")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=f"{ctx.author.avatar_url_as(size=1024)}")
        await ctx.send(embed=embed)


    @commands.command()
    async def serverinfo(self, ctx):
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

    @commands.command()
    async def userinfo(self, ctx, *, user: discord.Member = None):
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

    @commands.command()
    async def accountage(self, ctx, *, user: discord.Member = None):
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

# Each extension needs this method
def setup(bot):
    bot.add_cog(Utilities(bot))