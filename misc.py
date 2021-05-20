from discord.ext import commands
import discord
import time
import maths
class misc (commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def solve(self, ctx, *, arg):
        #print(arg)
        solver = maths.parser(arg)
        embed=discord.Embed(title = arg, description=("The equation equals "+str(solver.evaluate())))
        await ctx.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(misc(bot))
