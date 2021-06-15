from discord.ext import commands
import discord
import requests
import os
import asyncio
from PIL import Image, ImageEnhance, ImageOps
path = "E:/Programming/Python/Talus/loader/cogs/images/"
fullFile = lambda path,f : path+f
class imgs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def write(self, att):
        URL = att.url
        img = requests.get(URL)
        file = open(fullFile(path,"img.png"), "wb")
        file.write(img.content)
        file.close()
        return Image.open(fullFile(path,"img.png"))

    async def check(self, ctx):
        try:
            return ctx.message.attachments[0]
        except IndexError:
            try :
                async for msg in ctx.message.channel.history(limit = int(5) + 1):
                     try :
                            att = msg.attachments[0]
                            return att
                     except :
                         pass
                return None
            except :
                return None

    @commands.command()
    async def modify(self, ctx, fac=None):
        if fac is None :
            await ctx.channel.send("no value was given")
            return None
        att = await self.check(ctx)
        if att is None :
            await ctx.channel.send("no image was provided")
            return None
        img = self.write(att)
        enc = ImageEnhance.Brightness(img)
        img = enc.enhance(float(fac))
        img.save(fullFile(path,"img.png"))
        img.close()
        await ctx.channel.send(file=discord.File(fullFile(path, "img.png")))

    @commands.command()
    async def rotate(self, ctx, ang = None):
        if ang == None:
            await ctx.channel.send("no value was given")
            return
        att = await self.check(ctx)
        if att is None :
            await ctx.channel.send("no image was provided")
            return None
        img = self.write(att)
        img = img.rotate(float(ang), expand = True)
        img.save(fullFile(path,"img.png"))
        img.close()
        await ctx.channel.send(file=discord.File(fullFile(path,"img.png")))

    @commands.command()
    async def invert(self, ctx):
        att = await self.check(ctx)
        if att is None :
            await ctx.channel.send("no image was provided")
            return None
        img = self.write(att).convert('RGB')
        im = ImageOps.invert(img)
        im.save(fullFile(path,"img.png"))
        await ctx.channel.send(file=discord.File(fullFile(path,"img.png")))

def setup(bot):
    bot.add_cog(imgs(bot))
