from discord.ext import commands
makeStr = lambda list : ''.join(list)
class tictactoe(commands.Cog):
    def __init__(self, bot, comp_sign='x', p_sign='o'):
        self.bot = bot
        self.pos=0
        self.p_move = -1
        self.comp_move = 1
        self.comp_sign = comp_sign
        self.p_sign = p_sign
        self.field = ['-']*9
    def represent(self, flag=0):
        fld = list(self.field)
        for i in range (0,9):
            if flag==0:
                fld[i]+=' ' 
            if i%3 == 0 :
                fld[i-1]+='\n'
        return makeStr(fld)
    def win (self):
        fld = str(self.represent(1))
        winPos = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]
        for i in range(8):
            if fld[winPos[i][0]] == fld[winPos[i][1]] and fld[winPos[i][1]] == fld[winPos[i][2]] and fld[winPos[i][0]]!='-':
                    if fld[winPos[i][0]] == self.p_sign:
                        return -1
                    elif fld[winPos[i][0]] == self.comp_sign :
                        return 1
        return 0
    @commands.command()
    async def game(self, ctx):
        self.field = ['-']*9
        for i in range(9):
            if self.win()!=0:
                print(self.win())
                await ctx.channel.send('```\nTHE GAME HAS ENDED!\n'+self.represent()+'\n```')
                return
            await ctx.channel.send('```\n'+self.represent()+'\n```')
            a = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
            if a.content == 'stop' :
                await ctx.channel.send('```\nOkay, I get it, human. You are too weak\n```')
                return
            pos = int(a.content)
            while pos > 9 or pos<=0 or self.field[pos-1]!='-':
                a = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
                pos = int(a.content)
            self.field[pos-1]=self.p_sign if i%2 == 0 else self.comp_sign
        await ctx.channel.send('```\nTHE GAME HAS ENDED!\n'+self.represent()+'\n```')
        return
def setup(bot):
    bot.add_cog(tictactoe(bot))
#tic = ttt(1,'x','o')
#tic.game() 
