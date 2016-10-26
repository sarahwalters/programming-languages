import unittest
from homework6 import *

class TestStringMethods (unittest.TestCase):
    def test_for(self):
        print "\n"

        env = initial_env_imp()

        inp1 = "for (var i = 0; (lt? i 3); i <- (+ i 1)) { print i; }"
        inp2 = "for (var i = 1; (lt? i 10); i <- (* i 2)) { print i; }"
        inp3 = "for (var i = 10; (gt? i 0); i <- (- i 3)) { print i; }"
        inp4 = """ for (var i = 0; (lt? i 3); i <- (+ i 1)) {
                       var j = (+ 4 (* 3 i));
                       print i;
                       print j;
                   }
                """

        print "\n* test_for case 1: should be 0, 1, 2"
        self.assertEqual(type(parse_imp(inp1)["stmt"].eval(env)), VNone)

        print "\n* test_for case 2: should be 1, 2, 4, 8"
        self.assertEqual(type(parse_imp(inp2)["stmt"].eval(env)), VNone)

        print "\n* test_for case 3: should be 10, 7, 4, 1"
        self.assertEqual(type(parse_imp(inp3)["stmt"].eval(env)), VNone)

        print "\n* test_for case 4: should be 0, 4, 1, 7, 2, 10"
        self.assertEqual(type(parse_imp(inp4)["stmt"].eval(env)), VNone)


    def test_array(self):
        print "\n"

        env = initial_env_imp()

        setups = [
            "var size = 5;",
            "var test = (new-array size);",
            "for (var i = 0; (lt? i size); i <- (+ i 1)) { test[i] <- (* i 2); }",
            "var square = (function (x) (* x x));",
            "var testSquared = (with test (map square));"
        ]

        print "* test_array: setting up"
        [switch_imp(parse_imp(setup), env) for setup in setups]

        inp1 = "print testSquared;"
        inp2 = "print (with test (map (function (x) (* x 2))));"
        inp3 = "print (with test (index 3));"
        inp4 = "print (with test (length));"

        print "\n* test_array case 1: should be <arr [0,4,16,36,64]>"
        self.assertEqual(switch_imp(parse_imp(inp1), env), None)

        print "\n* test_array case 2: should be <arr [0,4,8,12,16]>"
        self.assertEqual(switch_imp(parse_imp(inp2), env), None)

        print "\n* test_array case 3: should be 6"
        self.assertEqual(switch_imp(parse_imp(inp3), env), None)

        print "\n* test_array case 4: should be 5"
        self.assertEqual(switch_imp(parse_imp(inp4), env), None)


if __name__ == '__main__':
    unittest.main()
