import unittest
from homework4 import *

class TestStringMethods (unittest.TestCase):
    def test_example(self):
        pass

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
