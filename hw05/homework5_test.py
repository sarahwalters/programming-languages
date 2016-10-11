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

    def test_recursive_func(self):
        e = EFunction(["n"],
                      EIf(ECall(EId("zero?"),[EId("n")]),
                          EValue(VInteger(0)),
                          ECall(EId("+"),[EId("n"),
                                          ECall(EId("me"),[ECall(EId("-"),[EId("n"),EValue(VInteger(1))])])])),
                      name="me")
        f = e.eval(initial_env())
        self.assertEqual(ECall(EValue(f),[EValue(VInteger(10))]).eval([]).value, 55)
if __name__ == '__main__':
    unittest.main()
