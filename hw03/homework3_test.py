import unittest
from homework3 import *

class TestStringMethods (unittest.TestCase):
    def test_parseLet(self):
        inp1 = "(let ((x 10) (y 20)) (+ x y))"
        inp2 = "(let ((a (let ((x 1) (y 2)) x)) (b (let ((x 1) (y 2)) y))) (let ((b a) (a b)) a))"
        inp3 = "(let ((a 1) (b 2) (c 3) (d 4) (e 5) (f 6)) f)"
        inp4 = "(let ((a 10)) (let ((sq (* a a)) (db (+ a a))) (+ sq db)))"
        inp5 = "(let ((x 10) (y 20) (z 30)) (+ x (* y z)))"

        self.assertEqual(parse(inp1).eval(INITIAL_FUN_DICT).value, 30)
        self.assertEqual(parse(inp2).eval(INITIAL_FUN_DICT).value, 2)
        self.assertEqual(parse(inp3).eval(INITIAL_FUN_DICT).value, 6)
        self.assertEqual(parse(inp4).eval(INITIAL_FUN_DICT).value, 120)
        self.assertEqual(parse(inp5).eval(INITIAL_FUN_DICT).value, 610)

    def test_parseUserFunc(self):
        inp1 = "(zero? 0)"
        inp2 = "(zero? 1)"
        inp3 = "(zero? (- 10 20))"
        inp4 = "(zero? (let ((a 1) (b 1)) (- a b)))"
        inp5 = "(+1 10)"
        inp6 = "(if (= 3 3) 1 2)"
        inp7 = "(if (= 3 4) 1 2)"
        inp8 = "(- 30 (- 20 15))"
        inp9 = "(+1 (if (zero? 0) 10 20))"

        self.assertEqual(parse(inp1).eval(INITIAL_FUN_DICT).value, True)
        self.assertEqual(parse(inp2).eval(INITIAL_FUN_DICT).value, False)
        self.assertEqual(parse(inp3).eval(INITIAL_FUN_DICT).value, False)
        self.assertEqual(parse(inp4).eval(INITIAL_FUN_DICT).value, True)
        self.assertEqual(parse(inp5).eval(INITIAL_FUN_DICT).value, 11)
        self.assertEqual(parse(inp6).eval(INITIAL_FUN_DICT).value, 1)
        self.assertEqual(parse(inp7).eval(INITIAL_FUN_DICT).value, 2)
        self.assertEqual(parse(inp8).eval(INITIAL_FUN_DICT).value, 25)
        self.assertEqual(parse(inp9).eval(INITIAL_FUN_DICT).value, 11)

if __name__ == '__main__':
    unittest.main()