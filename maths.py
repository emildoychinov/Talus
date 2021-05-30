from enum import Enum
import re
import math
import decimal
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
    #Here we split the expression that was given to us into different parts
    def split(self, expr) :
        expr = re.split(r'([\s\+\-\*\/\^\(\)])', expr)
        return list(filter(lambda x: x!='' and x!=' ', expr))
    
    def calc(self, operator, operand1, operand2):
        ctx = decimal.Context()
        ctx.prec = 20
        if operator == '+' : dec = ctx.create_decimal(repr(operand1+operand2))
        if operator == '-' : dec = ctx.create_decimal(repr(operand1-operand2))
        if operator == '*' : dec = ctx.create_decimal(repr(operand1*operand2))
        if operator == '/' : dec = ctx.create_decimal(repr(operand1/operand2))
        if operator == '^' : dec = ctx.create_decimal(repr(operand1**operand2))
        return format(dec, 'f')
        
    #This function is vital for us : we get the operator that has the biggest precedence
    def get_precedent(self):
        ix = 0
        mx = 4
        for i in range(len(self.operators)):
            if mx>self.tokens[self.operators[i]].value :
                mx = self.tokens[self.operators[i]].value
                ix=i
        return ix
    #here we lex the given expression
    def lex(self, expr):
        self.expr = self.analyze(expr)
        self.operators.clear()
        self.operands.clear()
        #we split the expression
        self.expr = self.split(self.expr)
        for i in range(len(self.expr)) :
            #since we are reading the operands with minuses (for ex in an expression like 1-1 the operands will be 1 and -1) if the given operator is a - then we append it as a +
            #but only if the next operator in the expression is not an operator used for raising a number to a given power(^)
            if self.expr[i] == '-' and self.expr[i-1] not in self.tokens : self.operators.append('-' if self.expr[i+2 if i+2 in range(len(self.expr)) else i+1] == '^' else '+')
            elif self.expr[i] in self.tokens and self.tokens[self.expr[i]]!=TOKEN.PAR and self.expr[i] != '-' : self.operators.append(self.expr[i])
        #we turn the expression back into a string, so we can use regex on it and also because it will take part in the other functions
        self.expr = ''.join(list(self.expr))
        #finding the operands in the expression with a regular expression, divided into two possibilities : a decimal number or a normal number
        self.operands = re.findall(r'\-?\d+\.\d+|\-?\d+', self.expr)

    def analyze(self, expr):
        expression = self.split(expr)
        i = 0
        #here we use a while loop instead of a for loop, since in this case it's more managable like that
        while i < len(expression):
            count = 0
            #we check if the element at the given index is a token
            if expression[i] in self.tokens:
                #if the element is a - we enter a separated case
                if expression[i] == '-' :
                    #we count the consecutive minuses and remove them
                    while expression[i] == '-':
                        count += 1
                        expression.pop(i)
                    #in the end if the instances are an even count then we insert a plus and if they are an odd count - a minus
                    expression.insert(i, '+' if count % 2 == 0 and count!=0 else '-')
                #we remove the consecutive operators if they are not brackets or minuses
                elif self.tokens[expression[i]]!=TOKEN.PAR and expression[i]!='-':
                    while expression[i] == expression[i+1] : expression.pop(i)
                #if we have an open bracket
                elif expression[i] == '(' :
                    #we make a string for the expression between the brackets
                    par = ''
                    #we save the index of the bracket
                    ix = i
                    while expression[i]!=')':
                        i+=1
                        if(expression[i] == '('):
                            #we save the index of the new open bracket in case there are more than one open brackets in the expression
                            ix = i
                    expression.pop(ix)
                    #here we append the elements of the expression between the brackets
                    while expression[ix]!=')':
                        par+=expression.pop(ix)
                    expression.pop(ix)
                    #we insert the result
                    expression.insert(ix, self.evaluate(par))
                    #the iterator becomes 0, since we want to analyze the expression once again
                    i = 0
            i+=1
        return ''.join(list(expression))
    #here we evaluate the expression
    def evaluate (self, expr) :
        #first off we analyze the expression that was passed
        self.lex(expr)
        #after that we analyze the analyzed expression to ensure that everything is fine
        self.lex(self.expr)
        #we go through the operators and operands and evaluate the expression
        for i in range(len(self.operators)):
            #getting the precedent operation
            ix = self.get_precedent()
            #doing the necessary calculation
            self.operands[ix] = str(self.calc(self.operators.pop(ix), float(self.operands[ix]), float(self.operands.pop(ix+1))))
        return self.operands[0]
