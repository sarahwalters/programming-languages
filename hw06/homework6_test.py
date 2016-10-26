import unittest
from homework6 import *

class TestStringMethods (unittest.TestCase):
    def test_for(self):
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

        print "test_for case 1: should be 0, 1, 2"
        self.assertEqual(type(parse_imp(inp1)["stmt"].eval(env)), VNone)

        print "\ntest_for case 2: should be 1, 2, 4, 8"
        self.assertEqual(type(parse_imp(inp2)["stmt"].eval(env)), VNone)

        print "\ntest_for case 3: should be 10, 7, 4, 1"
        self.assertEqual(type(parse_imp(inp3)["stmt"].eval(env)), VNone)

        print "\ntest_for case 4: should be 0, 4, 1, 7, 2, 10"
        self.assertEqual(type(parse_imp(inp4)["stmt"].eval(env)), VNone)

        print ""


if __name__ == '__main__':
    unittest.main()
