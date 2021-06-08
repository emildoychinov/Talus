from discord.ext import commands
import time 
#a util function that will be used to make a list into a string
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
    #a function to represent the board and to make it ready for printing
    def represent(self, flag=0):
        fld = list(self.field)
        for i in range (0,9):
            if flag==0:
                fld[i]+=' ' 
            if i%3 == 0 and flag==0:
                fld[i-1]+='\n'
        return makeStr(fld)
    #here we check if the game has been won
    def win (self, fld=None):
        if fld is None : fld = list(self.represent(1))
        #the positions for winning
        winPos = [[0,1,2], [0,3,6], [0,4,8], [1,4,7], [2,4,6], [2,5,8], [3,4,5], [6,7,8]]
        #check
        for i in range(8):
            # if the player wins we return -1 and if the bot wins we return 1, that will be used in the algorithm for the bot
            if fld[winPos[i][0]] == fld[winPos[i][1]] and fld[winPos[i][0]] == fld[winPos[i][2]] and fld[winPos[i][0]]!='-':
                return -1 if fld[winPos[i][0]] == self.p_sign else 1
        #if it is a draw or the game has not yet ended we return 0
        return 0
    #a utility function to edit a discord message
    async def edt (self, ctx, cnt, msg, auth_msg = None):
        if auth_msg is not None :
            await auth_msg.delete()
        await msg.edit(content = cnt)
        return msg 
    #the bot algorithm
    def minimax(self, pl, fld = None):
        if fld is None:
            fld = list(self.represent(1))
        #if the game has ended we return either -1 or 1, depending on who won
        end = self.win(fld)
        if end : return end*pl
        #we start from negative score : we prefer a move that could lead to a draw rather than a move that could lead to the opposing player winning
        score = -10
        move=-10
        for i in range(9):
            #we check if the position is available
            if fld[i] == '-':
                #test the position
                fld[i] = self.p_sign if pl==-1 else self.comp_sign
                #see how the position will look like for the opposing player
                moveScore = -self.minimax(-pl, fld)
                if moveScore > score :
                    score = moveScore
                    move = i
                #we return the field on the given position back to normal
                fld[i] = '-'
        #if no move has been made we return 0
        if move == -10 :
            return 0
        #if there has been a move made but no one has yet won we return the score
        return score
    #here we make a move based on the results from the minimax function (a full tree search of the tictactoe board)
    def makeMove(self):
        fld = list(self.represent(1))
        score = -10
        for i in range(9):
            #if available
            if fld[i] == '-':
                #test the move
                fld[i] = self.comp_sign
                #see how it will look like for the opposing player
                thisScore = -self.minimax(-self.comp_move, fld)
                fld[i] = '-'
                #if the score of the move is better than the current score we save it
                if thisScore>score :
                    score = thisScore
                    move = i
        #we return the move+1
        return move+1
    #a utility function for deleting a certain message
    async def delTrace (self, ctx, msg):
        await msg.delete()

    @commands.command()
    #here the game is played off
    async def game(self, ctx):
        self.field = ['-']*9
        msg = await ctx.channel.send('```WELCOME TO THE GAME OF TICTACTOE!\n Do you want to be (f)irst or (s)econd?\n```')
        #we wait to see if the player wants to be first or second
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
            #if the game has been won
            if self.win():
                #edit the board
                msg = await self.edt(ctx, '```THE GAME HAS ENDED! '+('I WIN!\n' if self.win()==1 else 'YOU WIN!\n')+self.represent()+'\n```', msg)
                time.sleep(1.5)
                #delete the board
                await self.delTrace(ctx, msg)
                return
            try : 
                #a is an argument that is None by default, it's the player's message : if it doesn't exist we catch the exception and proceed without it
                #if it does, we delete it
                msg = await self.edt(ctx, '```\n'+self.represent()+'\n```', msg, a)
            except :
                msg = await self.edt(ctx, '```\n'+self.represent()+'\n```', msg)
            #flg is the flag for the player : if he is first it's 0, otherwise it's 1
            if i%2 == flg:
                #we wait for the player's move
                a = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
                #a cheeky easter egg :)
                if a.content == 'stop' :
                    await ctx.channel.send('```\nOkay, I get it, human. You are too weak\n```')
                    return
            #we check if the move is valid
            #if it is not, it becomes 0
            pos = (int(a.content) if a.content.isdigit() else 0) if i%2==flg else self.makeMove()
            #while the move is invalid
            while pos > 9 or pos<=0 or self.field[pos-1]!='-':
                #we wait for a new one
                a = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
                pos = int(a.content)
            #we make the move
            self.field[pos-1] = self.p_sign if i%2 == flg else self.comp_sign
        try :
            msg = await self.edt(ctx, '```THE GAME HAS ENDED! IT IS A DRAW!\n'+self.represent()+'\n```', msg, a)
        except :
            msg = await self.edt(ctx, '```THE GAME HAS ENDED! IT IS A DRAW!\n'+self.represent()+'\n```', msg)
        time.sleep(1.5)
        await self.delTrace(ctx, msg)
        
#setting up the cog for the bot...
def setup(bot):
    bot.add_cog(tictactoe(bot))
