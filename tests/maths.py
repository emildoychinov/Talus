import re
class grammarError(Exception) : pass
class Tokenizer:
    def __init__(self, expr):
        self.tokens = re.findall(r'[\d\.]+|[+-\/*\(\)\^]', expr)
        if re.match(r'[a-zA-z]', expr):
            raise grammarError ('Invalid expression')
        self.ix = 0

    def getNext(self) :
        if self.ix < len(self.tokens):
            op = self.tokens[self.ix]
            self.ix+=1
            return op
        return None

    def peekNext(self) :
        if self.ix < len(self.tokens):
            return self.tokens[self.ix]
        return None

class parser:
    def __init__(self, expr):
        self.expr = expr
        self.tokenizer = Tokenizer(self.expr)

    def isNumber(self, token):
        try :
            float(token)
            return True
        except ValueError:
            return False

    def term (self):
        op1 = float(self.factor())
        while self.tokenizer.peekNext() in ('+', '-'):
            opr = self.tokenizer.getNext()
            op2 = float(self.factor())
            if opr == '+' : op1+=op2
            else : op1-=op2
        return op1

    def factor (self):
        op1 = float(self.power())
        while self.tokenizer.peekNext() in ('*', '/'):
            opr = self.tokenizer.getNext()
            op2 = float(self.power())
            if opr == '*' : op1*=op2
            else :op1/=op2
        return op1

    def power (self):
        op1 = float(self.value())
        while self.tokenizer.peekNext() == '^' :
            opr = self.tokenizer.getNext()
            op2 = float(self.value())
            op1 = op1**op2
        return op1

    def value(self):
        token = self.tokenizer.getNext()
        if token == '(':
            token = self.term()
            if self.tokenizer.getNext() != ')':
                raise grammarError('The expression is invalid')

        if not self.isNumber(token):
            self.tokenizer.ix-=1
            token = 0

        return token
