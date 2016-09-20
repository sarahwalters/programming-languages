############################################################
# HOMEWORK 2
#
# Team members:
#
# Emails:
#
# Remarks:
# questions on ELetS test cases -- should ELet have an expand method?

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

#
# Operations Dicts
#

# Initial primitives dictionary
INITIAL_PRIM_DICT = {
    "+": oper_plus,
    "*": oper_times,
    "-": oper_minus,
}

# Initial function dictionary
FUNC_DICT = {}

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

    def eval (self,prim_dict,fun_dict=FUNC_DICT):
        return VInteger(self._integer)

    def substitute (self,id,new_e):
        return self


class EBoolean (Exp):
    # Boolean literal

    def __init__ (self,b):
        self._boolean = b

    def __str__ (self):
        return "EBoolean({})".format(self._boolean)

    def eval (self,prim_dict,fun_dict=FUNC_DICT):
        return VBoolean(self._boolean)

    def substitute (self,id,new_e):
        return self

class EValue (Exp):
    # Boolean literal

    def __init__ (self,v):
        self._value = v

    def __str__ (self):
        return "EValue({})".format(self._value)

    def eval (self,prim_dict,fun_dict=FUNC_DICT):
        return self._value

    def substitute (self,id,new_e):
        return self


class EPrimCall (Exp):

    def __init__ (self,name,es):
        self._name = name
        self._exps = es

    def __str__ (self):
        return "EPrimCall({},[{}])".format(self._name,",".join([ str(e) for e in self._exps]))

    def eval (self,prim_dict,fun_dict=FUNC_DICT):
        vs = [ e.eval(prim_dict,fun_dict) for e in self._exps ]
        return apply(prim_dict[self._name],vs)

    def substitute (self,id,new_e):
        new_es = [ e.substitute(id,new_e) for e in self._exps]
        return EPrimCall(self._name,new_es)

class ECall (Exp):

    def __init__ (self,name,es):
        self._name = name
        if not isinstance(es, list):
            self._exps = [es]
        else:
            self._exps = es

    def __str__ (self):
        return "ECall({},[{}])".format(self._name,",".join([ str(e) for e in self._exps]))

    def eval (self, prim_dict, fun_dict=FUNC_DICT):
        if self._name in fun_dict:
            fun = fun_dict[self._name]
            params = fun["params"]
            body = fun["body"]
            if len(self._exps) == len(params):
                return ELet(zip(params, self._exps), body).eval(prim_dict, fun_dict)
            else:
                raise Exception("Runtime error: Wrong number of arguements for function call")

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

    def eval (self,prim_dict, fun_dict=FUNC_DICT):
        v = self._cond.eval(prim_dict,fun_dict)
        if v.type != "boolean":
            raise Exception ("Runtime error: condition not a Boolean")
        if v.value:
            return self._then.eval(prim_dict,fun_dict)
        else:
            return self._else.eval(prim_dict,fun_dict)

    def substitute (self,id,new_e):
        return EIf(self._cond.substitute(id,new_e),
                   self._then.substitute(id,new_e),
                   self._else.substitute(id,new_e))

class EDef (Exp):

    def __init__ (self, e1, e2, e3):
        self._name = e1
        self._params= e2
        self._body= e3

    def __str__ (self):
        return "EDef({},{},{})".format(self._name,self._params,self._body)

    def eval (self,prim_dict, fun_dict=FUNC_DICT):
        if type(self._params) is str:
            FUNC_DICT[self._name] = {
                "params": [self._params],
                "body": self._body
            }
        elif type(self._params) is list:
            if all([isinstance(x, str) for x in self._params]):
                FUNC_DICT[self._name] = {
                    "params": self._params,
                    "body": self._body
                }
        else:
            raise Exception ("params should be a list")


class ELet (Exp):
    # concurrent local binding

    def __init__ (self,bindings,letExp):
        self._bindings = bindings
        self._letExp = letExp

    def __str__ (self):
        prettyBindings = [(i, str(e)) for (i, e) in self._bindings]
        return "ELet({},{})".format(prettyBindings, self._letExp)

    def eval (self,prim_dict,fun_dict=FUNC_DICT):
        new_letExp = self._letExp
        for (id, e) in self._bindings:
            new_letExp = new_letExp.substitute(id, e)

        return new_letExp.eval(prim_dict, fun_dict)

    def substitute (self,id,new_e):
        selfIds = [i for (i, e) in self._bindings] # the ids associated with this ELet

        # Apply substitutions to list of bindings concurrently
        substitutedBindings = [(i, e.substitute(id, new_e)) for (i, e) in self._bindings]

        # Always apply substitutions to bindings; only apply substitutions to the
        # expression-to-be-evaluated if the id in question isn't part of this let statement
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
        prettyBindings = [(i, str(e)) for (i, e) in self._bindings]
        return "ELetS({},{})".format(prettyBindings, self._letExp)

    def eval (self,prim_dict):
        new_letExp = self._letExp
        for (id, e) in self._bindings:
            new_letExp = new_letExp.substitute(id, e)

        return new_letExp.eval(prim_dict)

    def substitute (self,id,new_e):
        selfIds = [i for (i, e) in self._bindings] # the ids associated with this ELet

        # Apply substitutions to list of bindings sequentially
        index = 0
        substitutedBindings = []
        for (i, e) in self._bindings:
            for (si, se) in substitutedBindings:
                e = e.substitute(si, se)
            substitutedBindings.append((i, e))

        # Always apply substitutions to bindings; only apply substitutions to the
        # expression-to-be-evaluated if the id in question isn't part of this let statement
        if id in selfIds:
            return ELet(substitutedBindings,
                        self._letExp)
        return ELet(substitutedBindings,
                    self._letExp.substitute(id,new_e))

    def expand (self):
        if len(self._bindings) == 1:
            return ELet(self._bindings, self._letExp)
        else:
            innerLet = ELetS(self._bindings[1:], self._letExp).expand()
            return ELet([self._bindings[0]], innerLet)


class ELetV (Exp):
    # local eager binding

    def __init__ (self,id,e1,e2):
        self._id = id
        self._e1 = e1
        self._e2 = e2

    def __str__ (self):
        return "ELetV({},{},{})".format(self._id,self._e1,self._e2)

    def eval (self,prim_dict,fun_dict=FUNC_DICT):
        new_e2 = self._e2.substitute(self._id, EValue(self._e1.eval(INITIAL_PRIM_DICT)))
        return new_e2.eval(prim_dict)

    def substitute (self,id,new_e):
        if id == self._id:
            return ELet(self._id,
                        self._e1.substitute(id,new_e),
                        self._e2)
        return ELet(self._id,
                    self._e1.substitute(id,new_e),
                    self._e2.substitute(id,new_e))


class EId (Exp):
    # identifier

    def __init__ (self,id):
        self._id = id

    def __str__ (self):
        return "EId({})".format(self._id)

    def eval (self,prim_dict,fun_dict=FUNC_DICT):
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
