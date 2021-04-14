from discord.ext import commands
import discord
import time
class utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def clear(self, ctx, args=None):
        msgs = list()
        if args==None:
            await ctx.channel.send("no args were given")
            return
        if args.isdigit()==0:
            await ctx.channel.send("invalid args")
            return
        async for msg in ctx.message.channel.history(limit=(int(args)+1)):
            await msg.delete()

def setup(bot):
    bot.add_cog(utilities(bot))
