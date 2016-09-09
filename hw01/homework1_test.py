import unittest
from homework1 import *

zero = EInteger(0)
tt = EBoolean(True)
ff = EBoolean(False)
v1 = EVector([EInteger(2), EInteger(3)])
v2 = EVector([EInteger(33), EInteger(66)])
b1 = EVector([EBoolean(True), EBoolean(False)])
b2 = EVector([EBoolean(False), EBoolean(False)])
half = EDiv(EInteger(1),EInteger(2))
third = EDiv(EInteger(1),EInteger(3))
v3 = EVector([half,third])
v4 = EVector([third,third])

def pair (v): return (v.get(0).value, v.get(1).value)

class TestStringMethods (unittest.TestCase):
    def test_EIsZero (self):
        self.assertEqual(EIsZero(zero).eval().value, True)
        self.assertEqual(EIsZero(EInteger(1)).eval().value, False)

        with self.assertRaises(Exception):
            EIsZero(EBoolean(False)).eval();


    def test_EOr (self):
        # booleans
        self.assertEqual(EOr(tt,tt).eval().value, True)
        self.assertEqual(EOr(tt,ff).eval().value, True)
        self.assertEqual(EOr(ff,tt).eval().value, True)
        self.assertEqual(EOr(ff,ff).eval().value, False)

        # vectors
        self.assertEqual(pair(EOr(b1, b2).eval()), (True, False))

        with self.assertRaises(Exception):
            EOr(EInteger(3), ff).eval()


    def test_EAnd (self):
        # booleans
        self.assertEqual(EAnd(tt,tt).eval().value, True)
        self.assertEqual(EAnd(tt,ff).eval().value, False)
        self.assertEqual(EAnd(ff,tt).eval().value, False)
        self.assertEqual(EAnd(ff,ff).eval().value, False)

        # vectors
        self.assertEqual(pair(EAnd(b1, b2).eval()), (False, False))

        with self.assertRaises(Exception):
            EAnd(EInteger(3), ff).eval()


    def test_ENot (self):
        # booleans
        self.assertEqual(ENot(tt).eval().value, False)
        self.assertEqual(ENot(ff).eval().value, True)

        # vectors
        self.assertEqual(pair(ENot(b1).eval()), (False, True))  

        with self.assertRaises(Exception):
            ENot(EInteger(3)).eval()


    def test_EPlus (self):
        # integers
        self.assertEqual(EPlus(EInteger(1), EInteger(1)).eval().value, 2)
        self.assertEqual(EPlus(EInteger(2), EInteger(3)).eval().value, 5)

        # rationals
        self.assertEqual(EPlus(ERational(1, 2), EInteger(1)).eval().numer, 3)
        self.assertEqual(EPlus(ERational(1, 2), EInteger(1)).eval().denom, 2)
        self.assertEqual(EPlus(EInteger(1), ERational(1, 2)).eval().numer, 3)
        self.assertEqual(EPlus(EInteger(1), ERational(1, 2)).eval().denom, 2)

        # vectors of integers
        self.assertEqual(pair(EPlus(v1, v2).eval()), (35, 69))

        # vectors of rationals
        self.assertEqual(EPlus(v3, v4).eval().get(0).numer, 5)
        self.assertEqual(EPlus(v3, v4).eval().get(0).denom, 6)
        self.assertEqual(EPlus(v3, v4).eval().get(1).numer, 6) # todo: update post-simplification
        self.assertEqual(EPlus(v3, v4).eval().get(1).denom, 9) # todo: update post-simplification

        with self.assertRaises(Exception):
            EPlus(EInteger(1), EBoolean(True)).eval()


    def test_EMinus (self):
        # integers
        self.assertEqual(EMinus(EInteger(1), EInteger(1)).eval().value, 0)
        self.assertEqual(EMinus(EInteger(3), EInteger(1)).eval().value, 2)

        # rationals
        self.assertEqual(EMinus(ERational(3, 2), EInteger(1)).eval().numer, 1)
        self.assertEqual(EMinus(ERational(3, 2), EInteger(1)).eval().denom, 2)
        self.assertEqual(EMinus(EInteger(1), ERational(1, 2)).eval().numer, 1)
        self.assertEqual(EMinus(EInteger(1), ERational(1, 2)).eval().denom, 2)

        # vectors of integers
        self.assertEqual(pair(EMinus(v1, v2).eval()), (-31, -63))

        # vectors of rationals
        self.assertEqual(EMinus(v3, v4).eval().get(0).numer, 1)
        self.assertEqual(EMinus(v3, v4).eval().get(0).denom, 6)

        with self.assertRaises(Exception):
            EMinus(EInteger(1), EBoolean(True)).eval()


    def test_ETimes (self):
        # integers
        self.assertEqual(ETimes(EInteger(1), EInteger(3)).eval().value, 3)

        # rationals
        self.assertEqual(ETimes(ERational(1, 2), EInteger(3)).eval().numer, 3)
        self.assertEqual(ETimes(ERational(1, 2), EInteger(3)).eval().denom, 2)
        self.assertEqual(ETimes(EInteger(3), ERational(1, 2)).eval().numer, 3)
        self.assertEqual(ETimes(EInteger(3), ERational(1, 2)).eval().denom, 2)

        # vectors of integers
        self.assertEqual(ETimes(v1, v2).eval().value, 264)
        self.assertEqual(ETimes(v1, EPlus(v2, v2)).eval().value, 528)
        self.assertEqual(ETimes(v1, EMinus(v2, v2)).eval().value, 0)

        # vectors of rationals
        self.assertEqual(ETimes(v3, v4).eval().numer, 15) # todo: update post-simplification
        self.assertEqual(ETimes(v3, v4).eval().denom, 54) # todo: update post-simplification

        with self.assertRaises(Exception):
            ETimes(EInteger(1), EBoolean(True)).eval()


    def test_EDiv (self):
        # integers
        self.assertEqual(EDiv(EInteger(1), EInteger(2)).eval().numer, 1)
        self.assertEqual(EDiv(EInteger(1), EInteger(2)).eval().denom, 2)
        self.assertEqual(EDiv(EInteger(2),EDiv(EInteger(3),EInteger(4))).eval().numer, 8)
        self.assertEqual(EDiv(EInteger(2),EDiv(EInteger(3),EInteger(4))).eval().denom, 3)

        # vectors of rationals
        self.assertEqual(EDiv(v3, v3).eval().get(0).numer, 2) # todo: update post-simplification
        self.assertEqual(EDiv(v3, v3).eval().get(0).denom, 2) # todo: update post-simplification
        self.assertEqual(EDiv(v3, v3).eval().get(1).numer, 3) # todo: update post-simplification
        self.assertEqual(EDiv(v3, v3).eval().get(1).denom, 3) # todo: update post-simplification

        with self.assertRaises(Exception):
            EDiv(EInteger(3), EBoolean(True)).eval()


    def test_EVector (self):
        # empty vector
        self.assertEqual(EVector([]).eval().length, 0)

        # vectors of integers
        evec = EVector([EInteger(10), EInteger(20), EInteger(30)])
        self.assertEqual(evec.eval().length, 3)
        self.assertEqual(evec.eval().get(0).value, 10)
        self.assertEqual(evec.eval().get(1).value, 20)
        self.assertEqual(evec.eval().get(2).value, 30)

        # vectors containing integer operations
        evec_plus = EVector([EPlus(EInteger(1), EInteger(2)), EInteger(0)])
        self.assertEqual(evec_plus.eval().length, 2)
        self.assertEqual(evec_plus.eval().get(0).value, 3)
        self.assertEqual(evec_plus.eval().get(1).value, 0)

        # vectors of booleans
        evec_bool = EVector([EBoolean(True), EAnd(EBoolean(True), EBoolean(False))])
        self.assertEqual(evec_bool.eval().length, 2)
        self.assertEqual(evec_bool.eval().get(0).value, True)
        self.assertEqual(evec_bool.eval().get(1).value, False)


    def test_VVector (self):
        self.assertEqual(VVector([]).length, 0)

        vvec = VVector([VInteger(10), VInteger(20), VInteger(30)])
        self.assertEqual(vvec.length, 3)
        self.assertEqual(vvec.get(0).value, 10)
        self.assertEqual(vvec.get(1).value, 20)
        self.assertEqual(vvec.get(2).value, 30)


    def test_VRational (self):
        self.assertEqual(VRational(1, 3).numer, 1)
        self.assertEqual(VRational(1, 3).denom, 3)

if __name__ == '__main__':
    unittest.main()
