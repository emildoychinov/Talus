from discord.ext import commands
import discord
import requests
import os
from PIL import Image, ImageEnhance
class imgs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def modify(self, ctx, fac=None):
        if fac==None :
            await ctx.channel.send("no value was given") 
            return
        att=0
        try :
        	att = ctx.message.attachments[0]
        except IndexError:
            await ctx.channel.send("no image was provided")
            return None
        URL=att.url
        img = requests.get(URL)
        file = open("img.png", "wb")
        file.write(img.content)
        file.close
        img = Image.open("img.png")
        enc = ImageEnhance.Brightness(img)
        ENCimg=enc.enhance(float(fac))
        ENCimg.save("changed.png")
        img.close()
        #os.remove("img.png")
        await ctx.channel.send(file=discord.File("changed.png"))

    @commands.command()
    async def rotate(self, ctx, ang):
        att=ctx.message.attachments[0]
        URL=att.url
        img=requests.get(URL)
        file = open("img.png", "wb")
        file.write(img.content)
        file.close
        img=Image.open("img.png")
        img=img.rotate(float(ang))
        img.save("changed.png")
        img.close()
        await ctx.channel.send(file=discord.File("changed.png"))

def setup(bot):
    bot.add_cog(imgs(bot))
