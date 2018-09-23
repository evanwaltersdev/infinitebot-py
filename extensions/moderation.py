#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
from discord.ext import commands


# Notice that because we use a class, everything has an additional
# `self` parameter
class Moderation:
    def __init__(self, bot):
        self.bot = bot

   
    # Notice we do commands.command now, not bot.command.
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, num=None):
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


# Each extension needs this method
def setup(bot):
    bot.add_cog(Moderation(bot))