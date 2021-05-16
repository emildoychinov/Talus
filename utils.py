from discord.ext import commands
import discord
import time
class utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def clear(self, ctx, args=None):
        if args==None or args.isdigit()==0:
            await ctx.channel.send("no args were given" if args==None else "invalid args")
            return
        await ctx.message.channel.purge(limit=int(args)+1)


def setup(bot):
    bot.add_cog(utilities(bot))
