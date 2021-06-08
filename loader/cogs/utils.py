from discord.ext import commands
import discord
import time
class utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def clear(self, ctx, args=None):
        if ctx.message.author.permissions_in(ctx.message.channel).manage_guild :
            await ctx.channel.send("no args were given" if args==None else "invalid args") if args==None or args.isdigit()==0 else await ctx.message.channel.purge(limit=int(args)+1)
            return
        else :
            await ctx.channel.send("you do not have the permissions to do that :P")
            return
    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def ban(self,ctx, member:discord.Member = None, *, reason = "unspecified reason"):
        if ctx.message.author.permissions_in(ctx.message.channel).ban_members:
            if member == None or member.id == ctx.author.id :
                await ctx.send("You cannot ban yourself, sorry! :)")
                return
            else: 
                await member.ban(reason = reason)
                reasonEmbed = discord.Embed(
                    description = f'Succesfully banned {member.mention} for {reason}\n \n ',
                    colour = 0xFF0000)
                reasonEmbed.set_author(name=f"{member.name}" + "#"+ f"{member.discriminator}", icon_url='{}'.format(member.avatar_url))
                reasonEmbed.set_footer(text=f"Banned by {ctx.author.name}", icon_url = '{}'.format(ctx.author.avatar_url))
                await ctx.send(embed=reasonEmbed)
        else :
            await ctx.send("You do not have these permissions, sorry :P")

def setup(bot):
    bot.add_cog(utilities(bot))
