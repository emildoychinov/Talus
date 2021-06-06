import discord
from discord.ext import commands
import chat
from chatbot import chatter
bot = commands.Bot(command_prefix='~')
bot.remove_command("help")
bot.load_extension('ttt')
bot.load_extension('imagery')
bot.load_extension('utils')
bot.load_extension('misc')
chatter = chatter.ChatBot()
chatter.prepare()
@bot.group(invoke_without_command = True)
async def help(ctx):
    embed = discord.Embed(title = "Help", description = "`Use ~help <command> for extended info`")
    embed.add_field(name = "Miscellaneous", value = "```solve, game```")
    embed.add_field(name = "Imagery :art:", value = "```modify, rotate```")
    embed.add_field(name = "Moderation :police_officer:", value = "```clear```")
    await ctx.send(embed = embed)
@help.command()
async def solve(ctx):
    embed = discord.Embed(title = "Solve :robot:", description = "`Solves a mathematical expression`")
    embed.add_field(name = "Use", value = "```~solve <expression>```")
    await ctx.send(embed = embed)
@help.command()
async def modify(ctx):
    embed = discord.Embed(title = "Modify :art:", description = "`Lightens or darkens a provided image depending on the given parameter`")
    embed.add_field(name = "Use", value = "```~modify <number> <image>```")
    await ctx.send(embed = embed)
@help.command()
async def rotate(ctx):
    embed = discord.Embed(title = "Modify :art:", description = "`Rotates a provided image depending on the given parameter`")
    embed.add_field(name = "Use", value = "```~rotate <number> <image>```")
    await ctx.send(embed = embed)
@help.command()
async def clear(ctx):
    embed = discord.Embed(title = "Clear :pencil2:", description = "`Clears a provided number of messages`")
    embed.add_field(name = "Use", value = "```~clear <number>```")
    await ctx.send(embed = embed)
@help.command()
async def game(ctx):
    embed = discord.Embed(title = "Game :robot:", description = "`Plays a game of Tic Tac Toe with Talus`")
    embed.add_field(name = "Use", value = "```~game```")
    embed.add_field(name = "Stop the game", value = "```Type stop to stop the game```")
    embed.add_field(name = "Playing the game", value = "```While playing the game, type in a number between 1 and 9 to take up a position on the field```")
    await ctx.send(embed = embed)
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    print(message.content)
    if str(bot.user.id) in message.content:
        msg = message.content.replace(f'<@!{bot.user.id}> ' if f'<@!{bot.user.id}>' in message.content else '@{bot.user.id}> ','')
        await message.channel.send(chatter.respond(msg))
bot.run('mytoken')
