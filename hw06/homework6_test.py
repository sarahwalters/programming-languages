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

    def test_strings(self):
        env = initial_env_imp()

        inp1 = 'print "hello";'
        inp2 = 'print "\\"hello\\"";'
        inp3 = 'print (length "hello");'
        inp4 = 'print (substring "hello" 1 2);'
        inp5 = 'print (concat "hel" "lo");'
        inp6 = 'print (startswith "hello" "h");'
        inp7 = 'print (endswith "hello" "o");'
        inp8 = 'print (lower "HELLO");'
        inp9 = 'print (upper "hello");'

        print "\n* test_for case 1: hello"
        self.assertEqual(type(parse_imp(inp1)["stmt"].eval(env)), VNone)
        print "\n* test_for case 2: \"hello\""
        self.assertEqual(type(parse_imp(inp2)["stmt"].eval(env)), VNone)
        print "\n* test_for case 3: 5"
        self.assertEqual(type(parse_imp(inp3)["stmt"].eval(env)), VNone)
        print "\n* test_for case 4: e"
        self.assertEqual(type(parse_imp(inp4)["stmt"].eval(env)), VNone)
        print "\n* test_for case 5: hello"
        self.assertEqual(type(parse_imp(inp5)["stmt"].eval(env)), VNone)
        print "\n* test_for case 6: true"
        self.assertEqual(type(parse_imp(inp6)["stmt"].eval(env)), VNone)
        print "\n* test_for case 7: true"
        self.assertEqual(type(parse_imp(inp7)["stmt"].eval(env)), VNone)
        print "\n* test_for case 8: hello"
        self.assertEqual(type(parse_imp(inp8)["stmt"].eval(env)), VNone)
        print "\n* test_for case 9: HELLO"
        self.assertEqual(type(parse_imp(inp9)["stmt"].eval(env)), VNone)


    def test_procedures(self):
        env = initial_env_imp()

        inp1 = "procedure foo(x,y,z) print (+ (+ x y) z);"
        inp2 = "foo(1, 2 ,3);"

        result = parse_imp(inp1)
        (name,expr) = result["decl"]
        v = expr.eval(env)
        env.insert(0,(name,VRefCell(v)))

        print "\n* test_for case 1: 6"
        self.assertEqual(type(parse_imp(inp2)["stmt"].eval(env)), VNone)



    def test_strings(self):
        print "\n"
        env = initial_env_imp()

        inp1 = 'print "hello";'
        inp2 = 'print "\\"hello\\"";'
        inp3 = 'print (length "hello");'
        inp4 = 'print (substring "hello" 1 2);'
        inp5 = 'print (concat "hel" "lo");'
        inp6 = 'print (startswith "hello" "h");'
        inp7 = 'print (endswith "hello" "o");'
        inp8 = 'print (lower "HELLO");'
        inp9 = 'print (upper "hello");'

        print "\n* test_strings case 1: hello"
        self.assertEqual(type(parse_imp(inp1)["stmt"].eval(env)), VNone)
        print "\n* test_strings case 2: \"hello\""
        self.assertEqual(type(parse_imp(inp2)["stmt"].eval(env)), VNone)
        print "\n* test_strings case 3: 5"
        self.assertEqual(type(parse_imp(inp3)["stmt"].eval(env)), VNone)
        print "\n* test_strings case 4: e"
        self.assertEqual(type(parse_imp(inp4)["stmt"].eval(env)), VNone)
        print "\n* test_strings case 5: hello"
        self.assertEqual(type(parse_imp(inp5)["stmt"].eval(env)), VNone)
        print "\n* test_strings case 6: true"
        self.assertEqual(type(parse_imp(inp6)["stmt"].eval(env)), VNone)
        print "\n* test_strings case 7: true"
        self.assertEqual(type(parse_imp(inp7)["stmt"].eval(env)), VNone)
        print "\n* test_strings case 8: hello"
        self.assertEqual(type(parse_imp(inp8)["stmt"].eval(env)), VNone)
        print "\n* test_strings case 9: HELLO"
        self.assertEqual(type(parse_imp(inp9)["stmt"].eval(env)), VNone)


    def test_procedures(self):
        print "\n"
        env = initial_env_imp()

        inp1 = "procedure foo(x,y,z) print (+ (+ x y) z);"
        inp2 = "foo(1, 2 ,3);"

        result = parse_imp(inp1)
        (name,expr) = result["decl"]
        v = expr.eval(env)
        env.insert(0,(name,VRefCell(v)))

        print "\n* test_procedures case 1: 6"
        self.assertEqual(type(parse_imp(inp2)["stmt"].eval(env)), VNone)


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
        switch_imp(parse_imp(inp1), env)

        print "\n* test_array case 2: should be <arr [0,4,8,12,16]>"
        switch_imp(parse_imp(inp2), env)

        print "\n* test_array case 3: should be 6"
        switch_imp(parse_imp(inp3), env)

        print "\n* test_array case 4: should be 5"
        switch_imp(parse_imp(inp4), env)


    def test_quicksort(self):
        print "\n"
        env = initial_env_imp()

        setups = [
            """ procedure quicksort(arr, start, stop) {
                if (gt? (- stop start) 1) {
                    var pivot = (with arr (index (- stop 1)));
                    var q = start;

                    for (var i = start; (lt? i (- stop 1)); i <- (+ i 1)) {
                        if (lte? (with arr (index i)) pivot) {
                            do (with arr (swap i q));
                            q <- (+ q 1);
                        }
                    }

                    do (with arr (swap q (- stop 1)));

                    quicksort(arr, start, q);
                    quicksort(arr, (+ q 1), stop);
                }
            }""",
            """ procedure test_quicksort(len) {
                var test = (new-array len);
                var max = (* len 10);

                for (var i = 0; (lt? i len); i <- (+ i 1)) {
                    test[i] <- (random max);
                }

                quicksort(test, 0, len);

                print test;
            }"""
        ]

        print "* test_quicksort: setting up"
        for setup in setups:
            env = switch_imp(parse_imp(setup), env)

        inp1 = "test_quicksort(3);"
        inp2 = "test_quicksort(6);"
        inp3 = "test_quicksort(10);"

        print "\n* test_quicksort case 1: should be sorted array of length 3 (random integer values)"
        switch_imp(parse_imp(inp1), env)

        print "\n* test_quicksort case 2: should be sorted array of length 6 (random integer values)"
        switch_imp(parse_imp(inp2), env)

        print "\n* test_quicksort case 3: should be sorted array of length 10 (random integer values)"
        switch_imp(parse_imp(inp3), env)


if __name__ == '__main__':
    unittest.main()

