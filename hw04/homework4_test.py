import unittest
from homework4 import *

class TestStringMethods (unittest.TestCase):
    def test_evalEnv(self):
        inp1 = "(let ((x 10)) (+ (let ((y 20)) (* y y)) x))"
        inp2 = "(let ((x 10)) (+ (let ((x 20)) (* x x)) x))"
        inp3 = "(let ((x 10)) (let ((y (+ x 1))) (let ((x (* y 2))) (* x x))))"
        inp4 = "(let ((x true) (y x)) (if y 1 0))"

        self.assertEqual(parse(inp1)["expr"].evalEnv(INITIAL_FUN_DICT, INITIAL_ENV_DICT).value, 410)
        self.assertEqual(parse(inp2)["expr"].evalEnv(INITIAL_FUN_DICT, INITIAL_ENV_DICT).value, 410)
        self.assertEqual(parse(inp3)["expr"].evalEnv(INITIAL_FUN_DICT, INITIAL_ENV_DICT).value, 484)
        self.assertEqual(parse(inp4)["expr"].evalEnv(INITIAL_FUN_DICT, INITIAL_ENV_DICT).value, 1)

    def test_and(self):
        inp1 = "(and)"
        inp2 = "(and true)"
        inp3 = "(and true false)"
        inp4 = "(and (= 1 1))"
        inp5 = "(let ((x true)) (and x x false true))"

        self.assertEqual(parse(inp1)['expr'].eval(INITIAL_FUN_DICT).value, True)
        self.assertEqual(parse(inp2)['expr'].eval(INITIAL_FUN_DICT).value, True)
        self.assertEqual(parse(inp3)['expr'].eval(INITIAL_FUN_DICT).value, False)
        self.assertEqual(parse(inp4)['expr'].eval(INITIAL_FUN_DICT).value, True)
        self.assertEqual(parse(inp5)['expr'].eval(INITIAL_FUN_DICT).value, False)

    def test_or(self):
        inp1 = "(or)"
        inp2 = "(or true)"
        inp3 = "(or true false)"
        inp4 = "(or true false false)"
        inp5 = "(or (= 1 1) (= 1 2))"

        self.assertEqual(parse(inp1)['expr'].eval(INITIAL_FUN_DICT).value, False)
        self.assertEqual(parse(inp2)['expr'].eval(INITIAL_FUN_DICT).value, True)
        self.assertEqual(parse(inp3)['expr'].eval(INITIAL_FUN_DICT).value, True)
        self.assertEqual(parse(inp4)['expr'].eval(INITIAL_FUN_DICT).value, True)
        self.assertEqual(parse(inp5)['expr'].eval(INITIAL_FUN_DICT).value, True)

    def test_cond(self):
        inp1 = "(cond)"
        inp2 = "(cond (true 10))"
        inp3 = "(cond (false 20) (true 30))"
        inp4 = "(cond ((= 1 2) 20) ((= 1 1) 30))"
        inp5 = "(cond ((= 1 2) 20) ((= 1 3) 30))"

        self.assertEqual(parse(inp1)['expr'].eval(INITIAL_FUN_DICT).value, False)
        self.assertEqual(parse(inp2)['expr'].eval(INITIAL_FUN_DICT).value, 10)
        self.assertEqual(parse(inp3)['expr'].eval(INITIAL_FUN_DICT).value, 30)
        self.assertEqual(parse(inp4)['expr'].eval(INITIAL_FUN_DICT).value, 30)
        self.assertEqual(parse(inp5)['expr'].eval(INITIAL_FUN_DICT).value, False)

if __name__ == '__main__':
    unittest.main()
