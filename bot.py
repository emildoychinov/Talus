from discord.ext import commands
import chat
bot = commands.Bot(command_prefix='~')
bot.load_extension('ttt')
bot.load_extension('imagery')
bot.load_extension('utils')
bot.load_extension('misc')
chatbot = chat.chat()
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    print(message.content)
    if str(bot.user.id) in message.content:
        msg = message.content.replace(f'<@!{bot.user.id}> ' if f'<@!{bot.user.id}>' in message.content else '@{bot.user.id}> ','')
        print(msg)
        await message.channel.send(chatbot.respond(message.content))
bot.run('mytoken')
