############################################################
# HOMEWORK 2
#
# Team members:
#
# Emails:
#
# Remarks:
# How do we do concurrent bindings? (last case for 1a)



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

    def eval (self,prim_dict):
        return VInteger(self._integer)

    def substitute (self,id,new_e):
        return self


class EBoolean (Exp):
    # Boolean literal

    def __init__ (self,b):
        self._boolean = b

    def __str__ (self):
        return "EBoolean({})".format(self._boolean)

    def eval (self,prim_dict):
        return VBoolean(self._boolean)

    def substitute (self,id,new_e):
        return self


class EPrimCall (Exp):

    def __init__ (self,name,es):
        self._name = name
        self._exps = es

    def __str__ (self):
        return "EPrimCall({},[{}])".format(self._name,",".join([ str(e) for e in self._exps]))

    def eval (self,prim_dict):
        vs = [ e.eval(prim_dict) for e in self._exps ]
        return apply(prim_dict[self._name],vs)

    def substitute (self,id,new_e):
        new_es = [ e.substitute(id,new_e) for e in self._exps]
        return EPrimCall(self._name,new_es)


class EIf (Exp):
    # Conditional expression

    def __init__ (self,e1,e2,e3):
        self._cond = e1
        self._then = e2
        self._else = e3

    def __str__ (self):
        return "EIf({},{},{})".format(self._cond,self._then,self._else)

    def eval (self,prim_dict):
        v = self._cond.eval(prim_dict)
        if v.type != "boolean":
            raise Exception ("Runtime error: condition not a Boolean")
        if v.value:
            return self._then.eval(prim_dict)
        else:
            return self._else.eval(prim_dict)

    def substitute (self,id,new_e):
        return EIf(self._cond.substitute(id,new_e),
                   self._then.substitute(id,new_e),
                   self._else.substitute(id,new_e))


class ELet (Exp):
    # concurrent local binding

    def __init__ (self,bindings,letExp):
        self._bindings = bindings
        self._letExp = letExp

    def __str__ (self):
        return "ELet({},{})".format(self._bindings, self._letExp)

    def eval (self,prim_dict):
        new_letExp = self._letExp
        for (id, e) in self._bindings:
            new_letExp = new_letExp.substitute(id,e)

        return new_letExp.eval(prim_dict)

    def substitute (self,id,new_e):
        selfIds = [i for (i, e) in self._bindings] # the ids associated with this ELet

        # apply let statements concurrently
        substitutedBindings = [(i, e.substitute(id, new_e)) for (i, e) in self._bindings]

        if id in selfIds:
            return ELet(substitutedBindings,
                        self._letExp)
        return ELet(substitutedBindings,
                    self._letExp.substitute(id,new_e))


class ELetS (Exp):
    # sequential local binding

    def __init__ (self,bindings,letExp):
        self._bindings = bindings
        self._letExp = letExp

    def __str__ (self):
        return "ELet({},{})".format(self._bindings, self._letExp)

    def eval (self,prim_dict):
        new_letExp = self._letExp
        for (id, e) in self._bindings:
            new_letExp = new_letExp.substitute(id,e)

        return new_letExp.eval(prim_dict)

    def substitute (self,id,new_e):
        selfIds = [i for (i, e) in self._bindings] # the ids associated with this ELet

        # apply let statements sequentially
        index = 0
        substitutedBindings = []
        for (i, e) in self._bindings:
            for (si, se) in substitutedBindings:
                e = e.substitute(si, se)
            substitutedBindings.append((i, e))

        if id in selfIds:
            return ELet(substitutedBindings,
                        self._letExp)
        return ELet(substitutedBindings,
                    self._letExp.substitute(id,new_e))


class EId (Exp):
    # identifier

    def __init__ (self,id):
        self._id = id

    def __str__ (self):
        return "EId({})".format(self._id)

    def eval (self,prim_dict):
        raise Exception("Runtime error: unknown identifier {}".format(self._id))

    def substitute (self,id,new_e):
        if id == self._id:
            return new_e
        return self



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





# Primitive operations

def oper_plus (v1,v2):
    if v1.type == "integer" and v2.type == "integer":
        return VInteger(v1.value + v2.value)
    raise Exception ("Runtime error: trying to add non-numbers")

def oper_minus (v1,v2):
    if v1.type == "integer" and v2.type == "integer":
        return VInteger(v1.value - v2.value)
    raise Exception ("Runtime error: trying to add non-numbers")

def oper_times (v1,v2):
    if v1.type == "integer" and v2.type == "integer":
        return VInteger(v1.value * v2.value)
    raise Exception ("Runtime error: trying to add non-numbers")


# Initial primitives dictionary

INITIAL_PRIM_DICT = {
    "+": oper_plus,
    "*": oper_times,
    "-": oper_minus
}


if __name__ == "__main__":
    print "none"