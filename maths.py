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
            '^' : TOKEN.POW,
            '/' : TOKEN.MULT_DIV,
            '*' : TOKEN.MULT_DIV,
            '-' : TOKEN.SUB_ADD,
            '+' : TOKEN.SUB_ADD,
            '(' : TOKEN.PAR,
            ')' : TOKEN.PAR
        }

        self.operators = []
        self.operands = []
        self.toDo = []

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

        for i in range(len(self.expr)) :

            if self.expr[i] == '-' and self.expr[i-1] not in self.tokens:
                self.operators.append('+')
            elif self.expr[i] in self.tokens and self.tokens[self.expr[i]]!=TOKEN.PAR and self.expr[i] != '-' :
                self.operators.append(self.expr[i])

        self.operands = re.findall(r'\-?\d+\.\d+|\-?\d+', self.expr)

    def analyze(self, expr, count = 0):

        par = str()
        expression = re.split(r'([\s\+\-\*\/\^\(\)])', expr)
        expression = list(filter(lambda x: x!='' and x!=' ', expression))
        flag = 0
        self.operands = re.findall(r'\-?\d+\.\d+|\-?\d+', expr)
        i = 0
        while i < len(expression):

            count = 0
            if not expression[i].isnumeric() and i == 0 and ('.' not in expression[i]) and expression[i]!='(' and expression[i]!=')':
                expression.insert(i, '0')
                flag = 1

            if expression[i] in self.tokens:
                ix = i
                if expression[ix] == '-' :

                    while expression[ix] == '-':
                        count +=1
                        expression.pop(ix)
                    expression.insert(ix, '+' if count % 2 == 0 and count!=0 else '-')

                elif self.tokens[expression[ix]]!=TOKEN.PAR and expression[ix] != '-':
                    opr = expression[ix]
                    while expression[ix] == opr :
                        count+=1
                        expression.pop(ix)
                    expression.insert(ix, opr)

                elif expression[ix] == '(' :
                    count = 0
                    expression.pop(ix)
                    while expression[ix]!=')':

                        par+=expression[ix]
                        if(expression[ix] == '('):
                            count+=1
                        expression.pop(ix)

                    expression.pop(ix)
                    for i in range(count):
                        par+=')'
                    expression.insert(ix,self.evaluate(par))
                    par = ''
                    i=0
            i+=1


        return ''.join(list(expression))


    def evaluate (self, expr) :

        self.lex(expr)
        self.lex(self.expr)
        for i in range(len(self.operators)):

            ix = self.get_precedent()
            self.operands[ix] = str(self.calc(self.operators[ix], float(self.operands[ix]), float(self.operands[ix+1])))
            self.operands.pop(ix+1)
            self.operators.pop(ix)

        return (self.operands[0]) if self.operands[0] != '69.0' else (self.operands[0]+', nice')

    def __repr__(self):

        self.evaluate()
        return str(self.expr)+'\n'+str(self.operands)
