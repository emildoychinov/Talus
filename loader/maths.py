import re
class grammarError(Exception) : pass
#the tokenizer for the parser
class Tokenizer:
    def __init__(self, expr):
        #we split the expression into different tokens with a regular expression
        self.tokens = re.findall(r'[\d\.]+|[+-\/*\(\)\^]', expr)
        #if lettets (a-Z) are in the expression it is invalid, so we raise an exception
        if re.match(r'[a-zA-z]', expr):
            raise grammarError ('Invalid expression')
        self.ix = 0
    #getting the next token
    def getNext(self) :
        if self.ix < len(self.tokens):
            op = self.tokens[self.ix]
            self.ix+=1
            return op
        return None
    #peeking the next token
    def peekNext(self) : 
        if self.ix < len(self.tokens):
            return self.tokens[self.ix]
        return None

class parser:
    def __init__(self, expr):
        self.expr = expr
        #we tokenize the expression
        self.tokenizer = Tokenizer(self.expr)
    #a function that will be used to check if a certain token is a number
    def isNumber(self, token):
        try :
            float(token)
            return True
        except ValueError:
            return False
    
    def term (self):
        #we get the result from factoring
        op1 = float(self.factor())
        #while the next token is + or -
        while self.tokenizer.peekNext() in ('+', '-'):
            #we get the operation by going onto the next token
            opr = self.tokenizer.getNext()
            #we get the result from factoring
            op2 = float(self.factor())
            #we return the result between the two operands
            if opr == '+' : op1+=op2
            else : op1-=op2
        return op1

    def factor (self):
        #we get the result from powering
        op1 = float(self.power())
        while self.tokenizer.peekNext() in ('*', '/'):
            opr = self.tokenizer.getNext()
            #we get the result from powering
            op2 = float(self.power())
            #we return the result between the two operands
            if opr == '*' : op1*=op2
            else :op1/=op2
        return op1
            
    def power (self):
        #we get the result from the expression in brackets, if there is one
        op1 = float(self.value())
        while self.tokenizer.peekNext() == '^' :
            opr = self.tokenizer.getNext()
            op2 = float(self.value())
            #we return the result between the two operands
            op1 = op1**op2
        return op1

    def value(self):
        #we get the next token
        token = self.tokenizer.getNext()
        #if it is a bracket
        if token == '(':
            #we call for the highest layer of the recursion - the one where we are adding the numbers, until we eventually come back here
            token = self.term()
            #if the next token is not a closing bracket, the expression is not valid, so we raise an exception
            if self.tokenizer.getNext() != ')':
                raise grammarError('The expression is invalid')
        #if the token is not a number and it was not an opening bracket, then we return 0 as an operand to be used  
        if not self.isNumber(token):
            self.tokenizer.ix-=1
            token = 0 

        return token

