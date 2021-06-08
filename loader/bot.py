import discord
from discord.ext import commands
from chatbot import chatter
import os
bot = commands.Bot(command_prefix='~')
bot.load_extension('misc')
for file in os.listdir('cogs'):
    if file.endswith('.py'):
            bot.load_extension(f'cogs.{file[:-3]}')
chatter = chatter.ChatBot()
chatter.prepare()
bot.remove_command('help')
@bot.group(invoke_without_command = True)
async def help(ctx):
    embed = discord.Embed(title = "Help", description = "`Use ~help <command> for extended info`")
    embed.add_field(name = "Miscellaneous", value = "```solve, game, avatar```")
    embed.add_field(name = "Imagery :art:", value = "```modify, rotate, invert```")
    embed.add_field(name = "Moderation :police_officer:", value = "```clear, ban```")
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
async def invert(ctx):
    embed = discord.Embed(title = "Invert :art:", description = "`Inverts a provided image`")
    embed.add_field(name = "Use", value = "```~invert <image>```")
    await ctx.send(embed = embed)

@help.command()
async def clear(ctx):
    embed = discord.Embed(title = "Clear :pencil2:", description = "`Clears a provided number of messages`")
    embed.add_field(name = "Use", value = "```~clear <number>```")
    embed.add_field(name = "Note :exclamation:", value = "```You cannot use that command unless you have the permisions to manage guilds```")
    await ctx.send(embed = embed)

@help.command()
async def game(ctx):
    embed = discord.Embed(title = "Game :robot:", description = "`Plays a game of Tic Tac Toe with Talus`")
    embed.add_field(name = "Use", value = "```~game```")
    embed.add_field(name = "Stop the game", value = "```Type stop to stop the game```")
    embed.add_field(name = "Playing the game", value = "```While playing the game, type in a number between 1 and 9 to take up a position on the field```")
    await ctx.send(embed = embed)

@help.command() 
async def avatar(ctx):
    embed = discord.Embed(title = "Avatar :person_doing_cartwheel:", description = "`Sends the avatar of a tagged user`")
    embed.add_field(name = "Use", value = "```~avatar <user>```")
    embed.add_field(name = "Note :exclamation:", value = "```If a user is not mentioned your avatar will be sent```")
    await ctx.send(embed = embed)

@help.command()
async def ban(ctx):
    embed = discord.Embed(title = "Ban :police_car:", description = "`Bans a tagged user`")
    embed.add_field(name = "Use", value = "```~ban <user> <reason>```")
    embed.add_field(name = "Note :exclamation:", value = "```You cannot use that command unless you have the permisions to kick people```")    
    await ctx.send(embed = embed)

@bot.event
async def on_message(message):
    message.content = message.content.lower()
    await bot.process_commands(message)
    if str(bot.user.id) in message.content and message.content[0]!='~':
        msg = message.content.replace(f'<@!{bot.user.id}> ' if f'<@!{bot.user.id}>' in message.content else '@{bot.user.id}> ','')
        await message.channel.send(chatter.respond(msg))

bot.run('ODE0NTkwMzQzMzY1Mzk0NDUy.YDgEYA.T7H5lBoa8D_T2keBZopQXONzfPI')
