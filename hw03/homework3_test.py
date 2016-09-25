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

if __name__ == '__main__':
    unittest.main()