from discord.ext import commands
import time 
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
            if i%3 == 0 and flag==0:
                fld[i-1]+='\n'
        return makeStr(fld)

    def win (self, fld=None):
        if fld is None : fld = list(self.represent(1))
        winPos = [[0,1,2], [0,3,6], [0,4,8], [1,4,7], [2,4,6], [2,5,8], [3,4,5], [6,7,8]]
        for i in range(8):
            if fld[winPos[i][0]] == fld[winPos[i][1]] and fld[winPos[i][0]] == fld[winPos[i][2]] and fld[winPos[i][0]]!='-':
                return -1 if fld[winPos[i][0]] == self.p_sign else 1
        return 0

    async def edt (self, ctx, cnt, msg, auth_msg = None):
        if auth_msg is not None :
            await auth_msg.delete()
        await msg.edit(content = cnt)
        return msg 

    def minimax(self, pl, fld = None):
        if fld is None:
            fld = list(self.represent(1))
        end = self.win(fld)
        if end : return end*pl
        score = -10
        move=-10
        for i in range(9):
            if fld[i] == '-':
                fld[i] = self.p_sign if pl==-1 else self.comp_sign
                moveScore = -self.minimax(-pl, fld)
                if moveScore > score :
                    score = moveScore
                    move = i
                fld[i] = '-'
        if move == -10 :
            return 0
        return score

    def makeMove(self):
        fld = list(self.represent(1))
        score = -10
        for i in range(9):
            if fld[i] == '-':
                fld[i] = self.comp_sign
                thisScore = -self.minimax(-self.comp_move, fld)
                fld[i] = '-'
                if thisScore>score :
                    score = thisScore
                    move = i
        return move+1

    async def delTrace (self, ctx, msg):
        await msg.delete()

    @commands.command()
    async def game(self, ctx):
        self.field = ['-']*9
        msg = await ctx.channel.send('```WELCOME TO THE GAME OF TICTACTOE!\n Do you want to be (f)irst or (s)econd?\n```')
        a = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
        if (a.content == 'f'):
            flg = 0
            self.p_sign = 'x'
            self.comp_sign = 'o'
        else :
            flg = 1
            self.p_sign = 'o'
            self.comp_sign = 'x'
        for i in range(9):
            if self.win():
                msg = await self.edt(ctx, '```THE GAME HAS ENDED! '+('I WIN!\n' if self.win()==1 else 'YOU WIN!\n')+self.represent()+'\n```', msg)
                time.sleep(1.5)
                await self.delTrace(ctx, msg)
                return
            try : 
                msg = await self.edt(ctx, '```\n'+self.represent()+'\n```', msg, a)
            except :
                msg = await self.edt(ctx, '```\n'+self.represent()+'\n```', msg)
            if i%2 == flg:
                a = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
                if a.content == 'stop' :
                    await ctx.channel.send('```\nOkay, I get it, human. You are too weak\n```')
                    return
            
            pos = (int(a.content) if a.content.isdigit() else 0) if i%2==flg else self.makeMove()
            print(pos)
            while pos > 9 or pos<=0 or self.field[pos-1]!='-':
                a = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
                pos = int(a.content)
            self.field[pos-1] = self.p_sign if i%2 == flg else self.comp_sign
        try :
            msg = await self.edt(ctx, '```THE GAME HAS ENDED! IT IS A DRAW!\n'+self.represent()+'\n```', msg, a)
        except :
            msg = await self.edt(ctx, '```THE GAME HAS ENDED! IT IS A DRAW!\n'+self.represent()+'\n```', msg)
        time.sleep(1.5)
        await self.delTrace(ctx, msg)

def setup(bot):
    bot.add_cog(tictactoe(bot))
