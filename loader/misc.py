from discord.ext import commands
import discord
import time
import maths
from decimal import Decimal, getcontext
class misc (commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def solve(self, ctx, *, arg):
        getcontext().prec = 20
        try :
            solver = maths.parser(arg)
            try :
                embed=discord.Embed(title = arg, description=("The equation equals " + str(Decimal(str(solver.term())))))
            except :
                embed=discord.Embed(title = "NULL", description=("You provided an invalid expression"))
        except :
            embed=discord.Embed(title = "NULL", description=("You provided an invalid expression"))
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def avatar(self, ctx, member : discord.Member = None):
        if member == None : member = ctx.message.author
        avatarUrl = member.avatar_url
        embed = discord.Embed(title = f"```{member}'s avatar```")
        embed.set_image(url = avatarUrl)
        await ctx.send(embed = embed)
        return

def setup(bot):
    bot.add_cog(misc(bot))
