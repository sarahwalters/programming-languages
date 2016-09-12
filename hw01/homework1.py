############################################################
# HOMEWORK 1
#
# Team members: Sarah Walters, Austin Greene
#
# Emails: Sarah.Walters@students.olin.edu, Austin.Greene@students.olin.edu
#
# Remarks:
# should we test mixed integer/rational vectors?
# should we allow EInteger +-*/ EVector? (currently allow EVector +-*/ EInteger)
# should we support boolean operations over vector & scalar?




#
# Expressions
#

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
        return VRational(self._numer, self._denom)


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
                return VRational((v1.value*v2.denom) + v2.numer, v2.denom)

        elif v1.type == "rational":
            if v2.type == "integer":
                return VRational((v2.value*v1.denom) + v1.numer, v1.denom)
            elif v2.type == "rational":
                return VRational((v1.numer*v2.denom) + (v2.numer*v1.denom), v2.denom * v1.denom)

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
                return VRational((v1.value*v2.denom) - v2.numer, v2.denom)

        elif v1.type == "rational":
            if v2.type == "integer":
                return VRational(v1.numer - (v2.value * v1.denom), v1.denom)
            elif v2.type == "rational":
                return VRational((v1.numer*v2.denom) - (v2.numer*v1.denom), v2.denom * v1.denom)

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
                return VRational(v1.value*v2.numer, v2.denom)

        elif v1.type == "rational":
            if v2.type == "integer":
                return VRational(v1.numer * v2.value, v1.denom)
            elif v2.type == "rational":
                return VRational(v1.numer * v2.numer, v1.denom * v2.denom)

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
                return VRational(v1.value, v2.value)
            elif v2.type == "rational":
                return VRational(v1.value*v2.denom, v2.numer)

        elif v1.type == "rational":
            if v2.type == "integer":
                return VRational(v1.numer, v1.denom*v2.value)
            elif v2.type == "rational":
                return VRational(v1.numer*v2.denom, v1.denom*v2.numer)

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
        v1 = self._b1.eval()

        if v1.type == "boolean":
            if v1.value:
                v2 = self._b2.eval()
                if v2.type == "boolean":
                    return VBoolean(v2.value)
            else:
                return VBoolean(False)

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
        v1 = self._exp1.eval()

        if v1.type == "boolean":
            if v1.value:
                return VBoolean(True) # short-circuit
            else:
                v2 = self._exp2.eval()
                if v2.type == "boolean":
                    return VBoolean(v2.value)

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
        self.numer = numer
        self.denom = denom
        self.type = "rational"


class VVector (Value):
    # Value representation of vectors
    def __init__ (self,vector):
        self.value = vector
        self.type = "vector"
        self.length = len(vector)

    def get (self, index):
        return self.value[index]
