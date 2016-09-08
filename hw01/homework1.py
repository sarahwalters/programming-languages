############################################################
# HOMEWORK 1
#
# Team members:
#
# Emails:
#
# Remarks:
#




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


class EBoolean (Exp):
    # Boolean literal

    def __init__ (self,b):
        self._boolean = b

    def __str__ (self):
        return "EBoolean({})".format(self._boolean)

    def eval (self):
        return VBoolean(self._boolean)

class EIsZero (Exp):
    # Boolean literal

    def __init__ (self, e):
        self._exp = e

    def __str__ (self):
        return "EIsZero({})".format(self._exp)

    def eval (self):
        v = self._exp.eval()
        if v.type == "integer":
            return VBoolean(v.value == 0)
        raise Exception ("Runtime error: trying to check zero of non-number")


class EAnd (Exp):
    # Boolean literal

    def __init__ (self, b1, b2):
        self._b1 = b1
        self._b2 = b2

    def __str__ (self):
        return "EAnd({})".format(self._b1, self._b2)

    def eval (self):
        v1 = self._b1.eval()
        if v1.type == "boolean":
            if (v1.value):
                v2 = self._b2.eval()
                if (v2.type == "boolean"):
                    return VBoolean(v2.value)
            else:
                return VBoolean(False)

        raise Exception ("Runtime error: trying to check zero of non boolean expressions")

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
        if v1.type == "integer" and v2.type == "integer":
            return VInteger(v1.value + v2.value)
        raise Exception ("Runtime error: trying to add non-numbers")


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
        if v1.type == "integer" and v2.type == "integer":
            return VInteger(v1.value - v2.value)
        raise Exception ("Runtime error: trying to subtract non-numbers")


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
        if v1.type == "integer" and v2.type == "integer":
            return VInteger(v1.value * v2.value)
        raise Exception ("Runtime error: trying to multiply non-numbers")


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


class EOr (Exp):
    # Boolean or operation

    def __init__ (self, e1, e2):
        self._exp1 = e1
        self._exp2 = e2

    def __str__ (self):
        return "EOr({},{})".format(self._exp1,self._exp2)

    def eval (self):
        v1 = self._exp1.eval()
        if v1.type != "boolean":
            raise Exception ("Runtime error: value not a boolean")
        if v1.value:
            return VBoolean(True)

        v2 = self._exp2.eval()
        if v2.type != "boolean":
            raise Exception ("Runtime error: value not a boolean")
        return VBoolean(v2.value)


class ENot (Exp):
    # Boolean not operation

    def __init__ (self, e):
        self._exp = e

    def __str__ (self):
        return "ENot({})".format(self._exp)

    def eval (self):
        v = self._exp.eval()
        if v.type != "boolean":
            raise Exception ("Runtime error: value not a boolean")
        return VBoolean(not v.value)

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
    # Value representation of Booleans
    def __init__ (self,b):
        self.value = b
        self.type = "boolean"
