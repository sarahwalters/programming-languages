import unittest
from homework1 import *

zero = EInteger(0)
tt = EBoolean(True)
ff = EBoolean(False)

class TestStringMethods (unittest.TestCase):
        def test_EIsZero (self):
            self.assertEqual(EIsZero(zero).eval().value, True)
            self.assertEqual(EIsZero(EInteger(1)).eval().value, False)

            with self.assertRaises(Exception):
                EIsZero(EBoolean(False)).eval();

	def test_EOr (self):
            self.assertEqual(EOr(tt,tt).eval().value, True)
            self.assertEqual(EOr(tt,ff).eval().value, True)
            self.assertEqual(EOr(ff,tt).eval().value, True)
            self.assertEqual(EOr(ff,ff).eval().value, False)

            with self.assertRaises(Exception):
                EOr(EInteger(3), ff).eval()

        def test_EAnd (self):
            self.assertEqual(EAnd(tt,tt).eval().value, True)
            self.assertEqual(EAnd(tt,ff).eval().value, False)
            self.assertEqual(EAnd(ff,tt).eval().value, False)
            self.assertEqual(EAnd(ff,ff).eval().value, False)

            with self.assertRaises(Exception):
                EAnd(EInteger(3), ff).eval()

	def test_ENot (self):
            self.assertEqual(ENot(tt).eval().value, False)
            self.assertEqual(ENot(ff).eval().value, True)

            with self.assertRaises(Exception):
                ENot(EInteger(3)).eval()

        def test_VRational (self):
            self.assertEqual(VRational(1, 3).numer, 1)
            self.assertEqual(VRational(1, 3).denom, 3)

        def test_EDiv (self):
            self.assertEqual(EDiv(EInteger(1), EInteger(2)).eval().numer, 1)
            self.assertEqual(EDiv(EInteger(1), EInteger(2)).eval().denom, 2)
            self.assertEqual(EDiv(EInteger(2),EDiv(EInteger(3),EInteger(4))).eval().numer, 8)
            self.assertEqual(EDiv(EInteger(2),EDiv(EInteger(3),EInteger(4))).eval().denom, 3)

            with self.assertRaises(Exception):
                EDiv(EInteger(3), EBoolean(True)).eval()

        def test_EPlus (self):
            self.assertEqual(EPlus(EInteger(1), EInteger(1)).eval().value, 2)
            self.assertEqual(EPlus(ERational(1, 2), EInteger(1)).eval().numer, 3)
            self.assertEqual(EPlus(ERational(1, 2), EInteger(1)).eval().denom, 2)
            self.assertEqual(EPlus(EInteger(1), ERational(1, 2)).eval().numer, 3)
            self.assertEqual(EPlus(EInteger(1), ERational(1, 2)).eval().denom, 2)

        def test_EMinus (self):
            self.assertEqual(EMinus(EInteger(1), EInteger(1)).eval().value, 0)
            self.assertEqual(EMinus(ERational(3, 2), EInteger(1)).eval().numer, 1)
            self.assertEqual(EMinus(ERational(3, 2), EInteger(1)).eval().denom, 2)
            self.assertEqual(EMinus(EInteger(1), ERational(1, 2)).eval().numer, 1)
            self.assertEqual(EMinus(EInteger(1), ERational(1, 2)).eval().denom, 2)

        def test_ETimes (self):
            self.assertEqual(ETimes(EInteger(1), EInteger(3)).eval().value, 3)
            self.assertEqual(ETimes(ERational(1, 2), EInteger(3)).eval().numer, 3)
            self.assertEqual(ETimes(ERational(1, 2), EInteger(3)).eval().denom, 2)
            self.assertEqual(ETimes(EInteger(3), ERational(1, 2)).eval().numer, 3)
            self.assertEqual(ETimes(EInteger(3), ERational(1, 2)).eval().denom, 2)

if __name__ == '__main__':
    unittest.main()
