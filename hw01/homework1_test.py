import unittest
from homework1 import *

tt = EBoolean(True)
ff = EBoolean(False)

class TestStringMethods (unittest.TestCase):
	def test_EOr (self):
		self.assertEqual(EOr(tt,tt).eval().value, True)
		self.assertEqual(EOr(tt,ff).eval().value, True)
		self.assertEqual(EOr(ff,tt).eval().value, True)
		self.assertEqual(EOr(ff,ff).eval().value, False)

		with self.assertRaises(Exception):
			EOr(EInt(3), ff)

	def test_ENot (self):
		self.assertEqual(ENot(tt).eval().value, False)
		self.assertEqual(ENot(ff).eval().value, True)

		with self.assertRaises(Exception):
			ENot(EInt(3))

if __name__ == '__main__':
	unittest.main()