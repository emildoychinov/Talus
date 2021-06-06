from discord.ext import commands
import discord
import requests
import os
import asyncio
from PIL import Image, ImageEnhance, ImageOps
class imgs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.msg = None

    def write(self, att):
        URL = att.url
        img = requests.get(URL)
        file = open("img.png", "wb")
        file.write(img.content)
        file.close()
        return Image.open("img.png")

    def check(self, ctx):
        try:
            att = ctx.message.attachments[0]
            return att
        except IndexError:
            try :
                att = self.msg.attachments[0]
                return att
            except :
                return None

    @commands.command()
    async def modify(self, ctx, fac=None):
        if fac is None :
            ctx.channel.send("no value was given")
            return None
        att = self.check(ctx)
        if att is None :
            await ctx.channel.send("no image was provided")
            return None
        img = self.write(att)
        enc = ImageEnhance.Brightness(img)
        img = enc.enhance(float(fac))
        img.save("changed.png")
        img.close()
        self.msg = await ctx.channel.send(file=discord.File("changed.png"))

    @commands.command()
    async def rotate(self, ctx, ang = None):
        if ang == None:
            await ctx.channel.send("no value was given")
            return
        att = self.check(ctx)
        if att is None :
            await ctx.channel.send("no image was provided")
            return None
        img = self.write(att)
        img = img.rotate(float(ang))
        img.save("changed.png")
        img.close()
        self.msg = await ctx.channel.send(file=discord.File("changed.png"))

    @commands.command()
    async def invert(self, ctx):
        att = self.check(ctx)
        if att is None :
            await ctx.channel.send("no image was provided")
            return None
        img = self.write(att).convert('RGB')
        im = ImageOps.invert(img)
        im.save('changed.png')
        self.msg = await ctx.channel.send(file=discord.File("changed.png"))


def setup(bot):
    bot.add_cog(imgs(bot))
