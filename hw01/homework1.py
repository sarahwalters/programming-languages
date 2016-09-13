############################################################
# HOMEWORK 1
#
# Team members: Sarah Walters, Austin Greene
#
# Emails: Sarah.Walters@students.olin.edu, Austin.Greene@students.olin.edu
#
# Remarks:
# We don't have a way to short-circuit boolean operations *and* allow scalar/vector
# boolean operations -- need to check the type of the second expression to decide what
# to return, which we can't do without evaluating the second expression. How would you
# work around this?


#
# Expressions
#

from math import sqrt, ceil
from functools import reduce

class Exp (object):
    pass


class EInteger (Exp):
    # Integer literal

    def __init__ (self,i):
        self._integer = i

    def __str__ (self):
        return "EInteger({})".format(self._integer)

    def eval (self):
        return VInteger(self._integer)


class ERational (Exp):
    # Boolean literal

    def __init__ (self, numer, denom):
        self._numer= numer
        self._denom = denom

    def __str__ (self):
        return "ERational({}, {})".format(self._numer, self._denom)

    def eval (self):
        rational = VRational(self._numer, self._denom)
        if rational.denom == 1:
            return VInteger(rational.numer)
        else:
            return rational


class EBoolean (Exp):
    # Boolean literal

    def __init__ (self,b):
        self._boolean = b

    def __str__ (self):
        return "EBoolean({})".format(self._boolean)

    def eval (self):
        return VBoolean(self._boolean)


class EIsZero (Exp):
    # IsZero operation

    def __init__ (self, e):
        self._exp = e

    def __str__ (self):
        return "EIsZero({})".format(self._exp)

    def eval (self):
        v = self._exp.eval()

        if v.type == "integer":
            return VBoolean(v.value == 0)

        raise Exception ("Runtime error: EZero not supported for {}".format(v.type))


class EPlus (Exp):
    # Addition operation

    def __init__ (self,e1,e2):
        self._exp1 = e1
        self._exp2 = e2

    def __str__ (self):
        return "EPlus({},{})".format(self._exp1,self._exp2)

    def eval (self):
        v1 = self._exp1.eval()
        v2 = self._exp2.eval()
        return self._add(v1, v2)

    def _add (self, v1, v2):
        if v1.type == "integer":
            if v2.type == "integer":
                return VInteger(v1.value + v2.value)
            elif v2.type == "rational":
                return ERational((v1.value*v2.denom) + v2.numer, v2.denom).eval()
            elif v2.type == "vector":
                vSum = []
                for i in range(v2.length):
                    vSum.append(self._add(v1, v2.get(i)))
                return VVector(vSum)

        elif v1.type == "rational":
            if v2.type == "integer":
                return ERational((v2.value*v1.denom) + v1.numer, v1.denom).eval()
            elif v2.type == "rational":
                return ERational((v1.numer*v2.denom) + (v2.numer*v1.denom), v2.denom * v1.denom).eval()
            elif v2.type == "vector":
                vSum = []
                for i in range(v2.length):
                    vSum.append(self._add(v1, v2.get(i)))
                return VVector(vSum)

        elif v1.type == "vector":
            vSum = []
            if v2.type == "vector":
                if (v1.length != v2.length):
                    raise Exception ("Runtime error: EAdd not supported for vectors with different lengths")
                for i in range(v1.length):
                    vSum.append(self._add(v1.get(i), v2.get(i)))
                return VVector(vSum)
            elif v2.type == "integer" or v2.type == "rational":
                for i in range(v1.length):
                    vSum.append(self._add(v1.get(i), v2))
            return VVector(vSum)

        raise Exception ("Runtime error: EAdd not supported for {} and {}".format(v1.type, v2.type))


class EMinus (Exp):
    # Subtraction operation

    def __init__ (self,e1,e2):
        self._exp1 = e1
        self._exp2 = e2

    def __str__ (self):
        return "EMinus({},{})".format(self._exp1,self._exp2)

    def eval (self):
        v1 = self._exp1.eval()
        v2 = self._exp2.eval()
        return self._subtract(v1, v2)

    def _subtract (self, v1, v2):
        if v1.type == "integer":
            if v2.type == "integer":
                return VInteger(v1.value - v2.value)
            elif v2.type == "rational":
                return ERational((v1.value*v2.denom) - v2.numer, v2.denom).eval()
            elif v2.type == "vector":
                vDiff = []
                for i in range(v2.length):
                    vDiff.append(self._subtract(v1, v2.get(i)))
                return VVector(vDiff)

        elif v1.type == "rational":
            if v2.type == "integer":
                return ERational(v1.numer - (v2.value * v1.denom), v1.denom).eval()
            elif v2.type == "rational":
                return ERational((v1.numer*v2.denom) - (v2.numer*v1.denom), v2.denom * v1.denom).eval()
            elif v2.type == "vector":
                vDiff = []
                for i in range(v2.length):
                    vDiff.append(self._subtract(v1, v2.get(i)))
                return VVector(vDiff)

        elif v1.type == "vector":
            vDiff = []
            if v2.type == "vector":
                if (v1.length != v2.length):
                    raise Exception ("Runtime error: trying to subtract vectors with different lengths")
                for i in range(v1.length):
                    vDiff.append(self._subtract(v1.get(i), v2.get(i)))
                return VVector(vDiff)
            elif v2.type == "integer" or v2.type == "rational":
                for i in range(v1.length):
                    vDiff.append(self._subtract(v1.get(i), v2))
            return VVector(vDiff)

        raise Exception ("Runtime error: EMinus not supported for {} and {}".format(v1.type, v2.type))


class ETimes (Exp):
    # Multiplication operation

    def __init__ (self,e1,e2):
        self._exp1 = e1
        self._exp2 = e2

    def __str__ (self):
        return "ETimes({},{})".format(self._exp1,self._exp2)

    def eval (self):
        v1 = self._exp1.eval()
        v2 = self._exp2.eval()
        return self._multiply(v1, v2)

    def _multiply (self, v1, v2):
        if v1.type == "integer":
            if v2.type == "integer":
                return VInteger(v1.value * v2.value)
            elif v2.type == "rational":
                return ERational(v1.value*v2.numer, v2.denom).eval()
            elif v2.type == "vector":
                vProd = []
                for i in range(v2.length):
                    vProd.append(self._multiply(v1, v2.get(i)))
                return VVector(vProd)


        elif v1.type == "rational":
            if v2.type == "integer":
                return ERational(v1.numer * v2.value, v1.denom).eval()
            elif v2.type == "rational":
                return ERational(v1.numer * v2.numer, v1.denom * v2.denom).eval()
            elif v2.type == "vector":
                vProd = []
                for i in range(v2.length):
                    vProd.append(self._multiply(v1, v2.get(i)))
                return VVector(vProd)

        elif v1.type == "vector":
            if v2.type == "vector":
                if v1.length != v2.length:
                    raise Exception ("Runtime error: ETimes not supported for vectors of different lengths")
                innerProduct = EInteger(0)
                for i in range(v1.length):
                    term = self._multiply(v1.get(i), v2.get(i))
                    if term.type == "integer":
                        innerProduct = EPlus(innerProduct, EInteger(term.value))
                    elif term.type == "rational":
                        innerProduct = EPlus(innerProduct, ERational(term.numer, term.denom))
                    else:
                        raise Exception("Runtime error: ETimes not supported for vectors containing elements which are not rational or integer")
                return innerProduct.eval()
            if v2.type == "integer" or v2.type == "rational":
                vProd = []
                for i in range(v1.length):
                    vProd.append(self._multiply(v1.get(i), v2))
                return VVector(vProd)

        raise Exception ("Runtime error: ETimes not supported for {} and {}".format(v1.type, v2.type))


class EDiv (Exp):
    # Division operation

    def __init__ (self,e1,e2):
        self._exp1 = e1
        self._exp2 = e2

    def __str__ (self):
        return "EDiv({},{})".format(self._exp1,self._exp2)

    def eval (self):
        v1 = self._exp1.eval()
        v2 = self._exp2.eval()
        return self._divide(v1, v2)

    def _divide (self, v1, v2):
        if v1.type == "integer":
            if v2.type == "integer":
                return ERational(v1.value, v2.value).eval()
            elif v2.type == "rational":
                return ERational(v1.value*v2.denom, v2.numer).eval()
            elif v2.type == "vector":
                vDiv = []
                for i in range(v2.length):
                    vDiv.append(self._divide(v1, v2.get(i)))
                return VVector(vDiv)

        elif v1.type == "rational":
            if v2.type == "integer":
                return ERational(v1.numer, v1.denom*v2.value).eval()
            elif v2.type == "rational":
                return ERational(v1.numer*v2.denom, v1.denom*v2.numer).eval()
            elif v2.type == "vector":
                vDiv = []
                for i in range(v2.length):
                    vDiv.append(self._divide(v1, v2.get(i)))
                return VVector(vDiv)

        elif v1.type == "vector":
            vDiv = []
            if v2.type == "vector":
                if v1.length != v2.length:
                    raise Exception ("Runtime error: EDiv not supported for vectors of different lengths")
                for i in range(v1.length):
                    vDiv.append(self._divide(v1.get(i), v2.get(i)))
            elif v2.type == "integer" or v2.type == "rational":
                for i in range(v1.length):
                    vDiv.append(self._divide(v1.get(i), v2))
            return VVector(vDiv)

        raise Exception ("Runtime error: EDiv not supported for {} and {}".format(v1.type, v2.type))


class EIf (Exp):
    # Conditional expression

    def __init__ (self,e1,e2,e3):
        self._cond = e1
        self._then = e2
        self._else = e3

    def __str__ (self):
        return "EIf({},{},{})".format(self._cond,self._then,self._else)

    def eval (self):
        v = self._cond.eval()

        if v.type != "boolean":
            raise Exception ("Runtime error: condition not a Boolean")
        if v.value:
            return self._then.eval()
        else:
            return self._else.eval()


class EAnd (Exp):
    # Boolean And operation

    def __init__ (self, b1, b2):
        self._b1 = b1
        self._b2 = b2

    def __str__ (self):
        return "EAnd({})".format(self._b1, self._b2)

    def eval (self):
        # NOTE: can't short-circuit if we're allowing scalar + vector operations.
        # Need to eval v2 to check what its type is.
        v1 = self._b1.eval()
        v2 = self._b2.eval()

        if v1.type == "boolean":
            if v2.type == "boolean":
                return VBoolean(v1.value and v2.value)
            elif v2.type == "vector":
                vAnd = []
                for i in range(v2.length):
                    vAnd.append(VBoolean(v1.value and v2.get(i).value))
                return VVector(vAnd)

        elif v1.type == "vector":
            vAnd = []
            v2 = self._b2.eval()
            if v2.type == "vector":
                if v1.length != v2.length:
                    raise Exception ("Runtime error: EAnd not supported for vectors of different lengths")
                for i in range(v1.length):
                    if v1.get(i).type == "boolean" and v2.get(i).type == "boolean":
                        vAnd.append(VBoolean(v1.get(i).value and v2.get(i).value))
                    else:
                        raise Exception ("Runtime error: EAnd not supported for vectors containing non-booleans")
                return VVector(vAnd)
            elif v2.type == "boolean":
                for i in range(v1.length):
                    vAnd.append(VBoolean(v1.get(i).value and v2.value))
                return VVector(vAnd)

        raise Exception ("Runtime error: EAnd not supported for {} and {}".format(v1.type, v2.type))


class EOr (Exp):
    # Boolean Or operation

    def __init__ (self, e1, e2):
        self._exp1 = e1
        self._exp2 = e2

    def __str__ (self):
        return "EOr({},{})".format(self._exp1,self._exp2)

    def eval (self):
        # NOTE: can't short-circuit if we're allowing scalar + vector operations.
        # Need to eval v2 to check what its type is.
        v1 = self._exp1.eval()
        v2 = self._exp2.eval()

        if v1.type == "boolean":
            if v2.type == "boolean":
                return VBoolean(v1.value or v2.value)
            elif v2.type == "vector":
                vOr = []
                for i in range(v2.length):
                    vOr.append(VBoolean(v1.value or v2.get(i).value))
                return VVector(vOr)

        elif v1.type == "vector":
            vOr = []
            v2 = self._exp2.eval()
            if v2.type == "vector":
                if v1.length != v2.length:
                    raise Exception ("Runtime error: EOr not supported for vectors of different lengths")
                for i in range(v1.length):
                    if v1.get(i).type == "boolean" and v2.get(i).type == "boolean":
                        vOr.append(VBoolean(v1.get(i).value or v2.get(i).value))
                    else:
                        raise Exception ("Runtime error: EOr not supported for vectors containing non-booleans")
                return VVector(vOr)
            elif v2.type == "boolean":
                for i in range(v1.length):
                    vOr.append(VBoolean(v1.get(i).value or v2.value))
                return VVector(vOr)

        raise Exception ("Runtime error: EOr not supported for {} and {}".format(v1.type, v2.type))


class ENot (Exp):
    # Boolean Not operation

    def __init__ (self, e):
        self._exp = e

    def __str__ (self):
        return "ENot({})".format(self._exp)

    def eval (self):
        v = self._exp.eval()

        if v.type == "boolean":
            return VBoolean(not v.value)

        elif v.type == "vector":
            vNot = []
            for i in range(v.length):
                vNot.append(VBoolean(not v.get(i).value))
            return VVector(vNot)

        raise Exception ("Runtime error: ENot not supported for {}".format(v.type))


class EVector (Exp):
    # Vector expression

    def __init__ (self, e):
        self._exp = e

    def __str__ (self):
        return "EVector({})".format(self._exp)

    def eval (self):
        v = []
        for item in self._exp:
            v.append(item.eval())
        return VVector(v)


#
# Values
#

class Value (object):
    pass


class VInteger (Value):
    # Value representation of integers
    def __init__ (self,i):
        self.value = i
        self.type = "integer"


class VBoolean (Value):
    # Value representation of booleans
    def __init__ (self,b):
        self.value = b
        self.type = "boolean"


class VRational (Value):
    # Value representation of rationals
    def __init__ (self, numer, denom):
        self.factorer = Factorer()
        (self.numer, self.denom) = self._simplify(numer, denom)
        self.type = "rational"

    def _mul (self, x, y):
        return x * y

    def _simplify (self, numer, denom):
        numer_factors = self.factorer.factor(numer)
        denom_factors = self.factorer.factor(denom)

        # List difference to find the factors unique to the numerator & to the denominator
        i = 0
        while i < len(numer_factors):
            factor = numer_factors[i]

            if factor in denom_factors:
                # if the numerator and denominator share a factor...
                # remove first instance of the factor from each list
                numer_factors.remove(factor)
                denom_factors.remove(factor)

                # step backwards to account for the removed factor
                i -= 1

            # step forwards to the next factor
            i += 1

        new_numer = reduce(self._mul, numer_factors, 1)
        new_denom = reduce(self._mul, denom_factors, 1)

        return (new_numer, new_denom)


class VVector (Value):
    # Value representation of vectors
    def __init__ (self,vector):
        self.value = vector
        self.type = "vector"
        self.length = len(vector)

    def get (self, index):
        return self.value[index]


class Factorer:
    def __init__ (self):
        self._cache = {}

    def factor (self, n):
        if n in self._cache:
            return self._cache[n]
        else:
            cap = int(sqrt(n) + 1)
            for i in range(2, cap):
                if n/i == float(n)/i:
                    factorization = self.factor(n/i) + [i]
                    self._cache[n] = factorization
                    return factorization
            return [1, n]
