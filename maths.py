from enum import Enum
import re
class TOKEN(Enum):

    POW = 1
    MULT_DIV = 2
    SUB_ADD = 3

class parser :

    def __init__(self, expr):
        self.expr = expr
        self.tokens = {
            '^' : TOKEN.POW,
            '/' : TOKEN.MULT_DIV,
            '*' : TOKEN.MULT_DIV,
            '-' : TOKEN.SUB_ADD,
            '+' : TOKEN.SUB_ADD
        }

        self.operators = []
        self.operands = []
        self.toDo = []

    def calc(self, operator, operand1, operand2):

        print([operand1, operator, operand2])
        if operator == '+':
            return operand1 + operand2
        elif operator == '-':
            return operand1 - operand2
        elif operator == '*':
            return operand1 * operand2
        elif operator == '/':
            return operand1 / operand2
        elif operator == '^':
            return operand1 ** operand2

    def precedence(self, op1, op2): return self.tokens[op1].value < self.tokens[op2].value

    def get_precedent(self):

        ix = 4
        mx = 4
        for i in range(len(self.operators)):

            if mx>self.tokens[self.operators[i]].value :
                mx = self.tokens[self.operators[i]].value
                ix=i

        return ix

    def lex(self):

        self.analyze()
        self.operators.clear()
        self.operands.clear()

        for i in self.expr :

            if i in self.tokens :
                self.operators.append(i)

        self.operands = re.findall(r'\d+\.\d+|\d+', self.expr)

    def analyze(self):

        expression = re.split(r'([\s\+\-\*\/\^])', self.expr)
        expression = list(filter(lambda x: x!='' and x!=' ', expression))
        print(expression)
        cycles = 0
        flag = 0
        self.operands = re.findall(r'\d+\.\d+|\d+', self.expr)
        for i in range(len(expression)):
            count = 0
            print(expression[i])
            if not expression[i].isnumeric() and i == 0 and ('.' not in expression[i]):
                expression.insert(i, '0')
                flag = 1
            if expression[i] in self.tokens:
                ix = i
                if expression[ix] == '-' :
                    while expression[ix] == '-':
                        count +=1
                        expression.pop(ix)
                    expression.insert(ix, '+' if count % 2 == 0 and count!=0 else '-')
                else :
                    opr = expression[ix]
                    while expression[ix] == opr :
                        count+=1
                        expression.pop(ix)
                    expression.insert(ix, opr)
                cycles+=1
                if cycles == ((len(self.operands)-1) if flag == 0 else (len(self.operands))):
                    break

        self.expr = ''.join(list(expression))


    def evaluate (self) :

        self.lex()
        print('expression : ' + self.expr + '\n')
        print(self.expr)
        for i in range(len(self.operators)):

            print('operators : \n' + str(self.operators) + '\noperands : \n' + str(self.operands))
            ix = self.get_precedent()
            self.operands[ix] = str(self.calc(self.operators[ix], float(self.operands[ix]), float(self.operands[ix+1])))
            self.operands.pop(ix+1)
            self.operators.pop(ix)

    def __repr__(self):

        self.evaluate()
        return str(self.expr)+'\n'+str(self.operands)

a = parser('6.1^4+23*2.1--2^0-3.3')
print(a)
