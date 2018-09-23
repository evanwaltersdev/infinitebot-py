from discord.ext import commands
import discord
import libneko


# Notice that because we use a class, everything has an additional
# `self` parameter
class Misc:
    def __init__(self, bot):
        self.bot = bot

    # Notice we do commands.command now, not bot.command.
    @commands.command()
    async def say(self, ctx, *, something):
        """Say something!"""
        if something is None:
            await ctx.send("What do you want to say?")
            return

        await ctx.send(f"{ctx.message.author.mention} said: **{something}**")

    @commands.command()
    async def git(self, ctx, *, user: discord.Member = None):
        """Link to Berg's git repo"""
        if user is None:
            user = ctx.author
        await ctx.message.delete()
        await ctx.send(f"{user.mention}, https://github.com/evanwaltersdev/infinitebot-py")

    @commands.command()
    async def suggest(self, ctx, *, suggestion):
        """Suggest a feature to <@268085347462676480>"""
        creator = (await bot.application_info()).owner
        await creator.send(f"New suggestion from {ctx.message.author.mention}: {suggestion}")
        embed=libneko.Embed(title=f'Your suggestion has been sent: {suggestion}')
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=f"{ctx.author.avatar_url_as(size=1024)}")
        await ctx.send(embed=embed)


# Each extension needs this method
def setup(bot):
    bot.add_cog(Misc(bot))