import unittest
from homework2 import *

class TestStringMethods (unittest.TestCase):
    def test_ELet(self):
        self.assertEqual(ELet([("a",EInteger(99))],EId("a")).eval(INITIAL_PRIM_DICT).value, 99)
        self.assertEqual(ELet([("a",EInteger(99)),
                               ("b",EInteger(66))],EId("a")).eval(INITIAL_PRIM_DICT).value, 99)
        self.assertEqual(ELet([("a",EInteger(99)),
                               ("b",EInteger(66))],EId("b")).eval(INITIAL_PRIM_DICT).value, 66)
        self.assertEqual(ELet([("a",EInteger(99))],
                         ELet([("a",EInteger(66)),
                               ("b",EId("a"))], EId("a"))).eval(INITIAL_PRIM_DICT).value, 66)
        self.assertEqual(ELet([("a",EInteger(5)),
                               ("b",EInteger(20))],
                               ELet([("a",EId("b")),
                                     ("b",EId("a"))],
                                     EPrimCall("-",[EId("a"),EId("b")]))).eval(INITIAL_PRIM_DICT).value, 15)

    def test_ELetS(self):
        # Without expand
        self.assertEqual(ELetS([("a",EInteger(99))],EId("a")).eval(INITIAL_PRIM_DICT).value, 99)
        self.assertEqual(ELetS([("a",EInteger(99)),
                                ("b",EInteger(66))],EId("a")).eval(INITIAL_PRIM_DICT).value, 99)
        self.assertEqual(ELetS([("a",EInteger(99)),
                                ("b",EInteger(66))],EId("b")).eval(INITIAL_PRIM_DICT).value, 66)
        self.assertEqual(ELet([("a",EInteger(99))],
                               ELetS([("a",EInteger(66)),
                                      ("b",EId("a"))],
                                      EId("a"))).eval(INITIAL_PRIM_DICT).value, 66)
        self.assertEqual(ELet([("a",EInteger(99))],
                               ELetS([("a",EInteger(66)),
                                      ("b",EId("a"))],
                                      EId("b"))).eval(INITIAL_PRIM_DICT).value, 66)
        self.assertEqual(ELetS([("a",EInteger(5)),
                                ("b",EInteger(20))],
                                ELetS([("a",EId("b")),
                                       ("b",EId("a"))],
                                       EPrimCall("-",[EId("a"),EId("b")]))).eval(INITIAL_PRIM_DICT).value, 0)

        # With expand
        self.assertEqual(ELetS([("a",EInteger(99)),
                                ("b",EInteger(66))],EId("a")).expand().eval(INITIAL_PRIM_DICT).value, 99)
        self.assertEqual(ELetS([("a",EInteger(99)),
                                ("b",EInteger(66))],EId("b")).expand().eval(INITIAL_PRIM_DICT).value, 66)
        self.assertEqual(ELet([("a",EInteger(99))],
                               ELetS([("a",EInteger(66)),
                                      ("b",EId("a"))],
                                      EId("a")).expand()).eval(INITIAL_PRIM_DICT).value, 66)
        self.assertEqual(ELet([("a",EInteger(99))],
                         ELetS([("a",EInteger(66)),
                                ("b",EId("a"))],
                                EId("b")).expand()).eval(INITIAL_PRIM_DICT).value, 66)
        self.assertEqual(ELetS([("a",EInteger(5)),
                                ("b",EInteger(20))],
                                ELetS([("a",EId("b")),
                                       ("b",EId("a"))],
                                       EPrimCall("-",[EId("a"),EId("b")]))).expand().eval(INITIAL_PRIM_DICT).value, 0)

    def test_ELetN(self):
        self.assertEqual(ELetN("a",EInteger(10),EId("a")).eval(INITIAL_PRIM_DICT).value, 10)
        self.assertEqual(ELetN("a",EInteger(10),
                         ELetN("b",EInteger(20),EId("a"))).eval(INITIAL_PRIM_DICT).value, 10)
        self.assertEqual(ELetN("a",EInteger(10),
                         ELetN("a",EInteger(20),EId("a"))).eval(INITIAL_PRIM_DICT).value, 20)
        self.assertEqual(ELetN("a",EPrimCall("+",[EInteger(10),EInteger(20)]),
                         ELetN("b",EInteger(20),EId("a"))).eval(INITIAL_PRIM_DICT).value, 30)
        self.assertEqual(ELetN("a",EPrimCall("+",[EInteger(10),EInteger(20)]),
                         ELetN("b",EInteger(20),
                               EPrimCall("*",[EId("a"),EId("a")]))).eval(INITIAL_PRIM_DICT).value, 900)

    def test_EDef(self):
        EDef("add1", ["x"], EPrimCall("+", [EInteger(1), EId("x")])).eval(INITIAL_PRIM_DICT)
        EDef("add2", "x", EPrimCall("+", [EInteger(2), EId("x")])).eval(INITIAL_PRIM_DICT)
        self.assertIn("add1", FUNC_DICT)
        self.assertIn("add2", FUNC_DICT)


    def test_ECall(self):
        EDef("add1", ["x"], EPrimCall("+", [EInteger(1), EId("x")])).eval(INITIAL_PRIM_DICT)
        self.assertEqual(ECall("add1", [EInteger(1)]).eval(INITIAL_PRIM_DICT).value, 2)
        self.assertEqual(ECall("add1", EInteger(1)).eval(INITIAL_PRIM_DICT).value, 2)

        FUN_DICT = {
            "+1": {"params":["x"],
                   "body":EPrimCall("+",[EId("x"),EInteger(1)])},
        }

        self.assertEqual(ECall("+1", [EInteger(100)]).eval(INITIAL_PRIM_DICT,FUN_DICT).value, 101)
if __name__ == '__main__':
    unittest.main()
