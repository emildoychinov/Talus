from discord.ext import commands
bot = commands.Bot(command_prefix='~')
bot.load_extension('ttt')
bot.load_extension('imagery')
bot.load_extension('utils')
bot.load_extension('misc')
bot.run('mytoken')
