import unittest
import maths
equations = [('(1^4*2^2+3^3)-2^5/4', 23), ('(18/6*5)-14/7', 13), ('(2+4)*6+2^2-10', 30), ('5-(4^2)', -11), 
        ('((69-(1432*3)/2)^2)^2+2822549328+2735343758592', 21419933570001), ('5*12-10.5*5+5^(2^((5-3)^2))+11^(2*(15^(5-5)))', 152587890753.5)]
class tester(unittest.TestCase):
    def test(self):
        for i in range (len(equations)):
            solver = maths.parser(equations[i][0])
            self.assertEqual(float(solver.term()), equations[i][1])

if __name__ == '__main__':
    unittest.main()
