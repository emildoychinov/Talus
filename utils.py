from discord.ext import commands
import discord
import time
class utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def clear(self, ctx, args=None):
        if args==None:
            await ctx.channel.send("no args were given")
            return
        if args.isdigit()==0:
            await ctx.channel.send("invalid args")
            return
        args=int(args)+1
        async for i in ctx.history():
            if args!=0 :
                args-=1
                time.sleep(0.2)
                await i.delete()
            else :
                return None
def setup(bot):
    bot.add_cog(utilities(bot))
