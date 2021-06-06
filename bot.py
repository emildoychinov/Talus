from discord.ext import commands
import chat
from chatbot import chatter
bot = commands.Bot(command_prefix='~')
bot.load_extension('ttt')
bot.load_extension('imagery')
bot.load_extension('utils')
bot.load_extension('misc')
chatter = chatter.ChatBot()
chatter.prepare()
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    print(message.content)
    if str(bot.user.id) in message.content:
        msg = message.content.replace(f'<@!{bot.user.id}> ' if f'<@!{bot.user.id}>' in message.content else '@{bot.user.id}> ','')
        await message.channel.send(chatter.respond(msg))
bot.run('mytoken')
