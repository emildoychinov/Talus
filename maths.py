from enum import Enum
import re
import math
class TOKEN(Enum):

    POW = 1
    MULT_DIV = 2
    SUB_ADD = 3
    PAR = 4

class parser :
    def __init__(self):
        self.expr = str()
        self.tokens = {
            '^' : TOKEN.POW, '/' : TOKEN.MULT_DIV, '*' : TOKEN.MULT_DIV,
            '-' : TOKEN.SUB_ADD, '+' : TOKEN.SUB_ADD, '(' : TOKEN.PAR, ')' : TOKEN.PAR
        }
        self.operators = []
        self.operands = []

    def split(self, expr) :
        expr = re.split(r'([\s\+\-\*\/\^\(\)])', expr)
        return list(filter(lambda x: x!='' and x!=' ', expr))

    def calc(self, operator, operand1, operand2):
        if operator == '+' : return operand1 + operand2
        elif operator == '-' : return operand1 - operand2
        elif operator == '*' : return operand1 * operand2
        elif operator == '/' : return operand1 / operand2
        elif operator == '^' : return operand1 ** operand2

    def get_precedent(self):
        ix = 0
        mx = 4
        for i in range(len(self.operators)):
            if mx>self.tokens[self.operators[i]].value :
                mx = self.tokens[self.operators[i]].value
                ix=i
        return ix

    def lex(self, expr):
        self.expr = self.analyze(expr)
        self.operators.clear()
        self.operands.clear()
        self.expr = self.split(self.expr)
        for i in range(len(self.expr)) :
            if self.expr[i] == '-' and self.expr[i-1] not in self.tokens : self.operators.append('-' if self.expr[i+2 if i+2 in range(len(self.expr)) else i+1] == '^' else '+')
            elif self.expr[i] in self.tokens and self.tokens[self.expr[i]]!=TOKEN.PAR and self.expr[i] != '-' : self.operators.append(self.expr[i])
        self.expr = ''.join(list(self.expr))
        self.operands = re.findall(r'\-?\d+\.\d+|\-?\d+', self.expr)

    def analyze(self, expr):
        expression = self.split(expr)
        i = 0
        while i < len(expression):
            count = 0
            if not expression[i].isnumeric() and i == 0 and ('.' not in expression[i]) and self.tokens[expression[i]]!=TOKEN.PAR : expression.insert(i, '0')
            if expression[i] in self.tokens:
                if expression[i] == '-' :
                    while expression[i] == '-':
                        count += 1
                        expression.pop(i)
                    expression.insert(i, '+' if count % 2 == 0 and count!=0 else '-')

                elif self.tokens[expression[i]]!=TOKEN.PAR and expression[i]!='-':
                    while expression[i] == expression[i+1] : expression.pop(i)

                elif expression[i] == '(' :
                    par = ''
                    ix = i
                    while expression[i]!=')':
                        i+=1
                        if(expression[i] == '('):
                            ix = i
                    expression.pop(ix)
                    while expression[ix]!=')':
                        par+=expression.pop(ix)
                    expression.pop(ix)
                    expression.insert(ix, self.evaluate(par))
                    i = 0
            i+=1
        return ''.join(list(expression))

    def evaluate (self, expr) :
        self.lex(expr)
        self.lex(self.expr)
        for i in range(len(self.operators)):
            ix = self.get_precedent()
            self.operands[ix] = str(self.calc(self.operators.pop(ix), float(self.operands[ix]), float(self.operands.pop(ix+1))))
        return self.operands[0]
