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

    def test_letS(self):
    	inp1 = "(let* ((x 10)) x)"
    	inp2 = "(let* ((x 10) (y (+ x 1))) y)"
    	inp3 = "(let* ((x 10) (y (+ x 1)) (z (+ y 1))) x)"
    	inp4 = "(let* ((x 10) (y (+ x 1)) (z (+ y 1))) y)"
    	inp5 = "(let* ((x 10) (y (+ x 1)) (z (+ y 1))) z)"

        self.assertEqual(parse(inp1)["expr"].evalEnv(INITIAL_FUN_DICT, INITIAL_ENV_DICT).value, 10)
        self.assertEqual(parse(inp2)["expr"].evalEnv(INITIAL_FUN_DICT, INITIAL_ENV_DICT).value, 11)
        self.assertEqual(parse(inp3)["expr"].evalEnv(INITIAL_FUN_DICT, INITIAL_ENV_DICT).value, 10)
        self.assertEqual(parse(inp4)["expr"].evalEnv(INITIAL_FUN_DICT, INITIAL_ENV_DICT).value, 11)
        self.assertEqual(parse(inp5)["expr"].evalEnv(INITIAL_FUN_DICT, INITIAL_ENV_DICT).value, 12)


if __name__ == '__main__':
    unittest.main()
