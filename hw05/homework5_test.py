import unittest
from homework5 import *

class TestStringMethods (unittest.TestCase):
    def test_multi_arg_func(self):
        env = initial_env()
        inp1 = "((function (x y) (+ x y)) 10 20)"
        inp2 = "(defun sum3 (x y z) (+ x (+ y z)))"
        inp3 = "(sum3 10 20 30)"

        self.assertEqual(parse(inp1)['expr'].eval(env).value, 30)
        result = parse(inp2)
        env.insert(0,(result["name"],VClosure(result["params"],result["body"],env)))
        self.assertEqual(parse(inp3)['expr'].eval(env).value, 60)
if __name__ == '__main__':
    unittest.main()
