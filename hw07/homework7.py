############################################################
# Simple imperative language
# C-like surface syntax
# with S-expression syntax for expressions
# (no recursive closures)
#

import sys
import random

#
# Expressions
#

class Exp (object):
    pass


class EValue (Exp):
    # Value literal (could presumably replace EInteger and EBoolean)
    def __init__ (self,v):
        self._value = v

    def __str__ (self):
        return "EValue({})".format(self._value)

    def eval (self,env):
        return self._value


class EPrimCall (Exp):
    # Call an underlying Python primitive, passing in Values
    #
    # simplifying the prim call
    # it takes an explicit function as first argument

    def __init__ (self,prim,es):
        self._prim = prim
        self._exps = es

    def __str__ (self):
        return "EPrimCall(<prim>,[{}])".format(",".join([ str(e) for e in self._exps]))

    def eval (self,env):
        vs = [ e.eval(env) for e in self._exps ]
        return apply(self._prim,vs)


class ELookup (Exp):
    # Index/key into an array, dictionary, or string
    # Can provide multiple indices -- e.g. arr[0]["a"] surface syntax
    # translates to abstract representation parameter indices = [0,"a"]
    # (useful for nesting arrays/dictionaries/strings)

    def __init__ (self, obj, indices):
        self._obj = obj
        self._indices = indices

    def __str__ (self):
        pretty_indices = ",".join([str(idx) for idx in self._indices])
        return "ELookup({},{})".format(self._obj, pretty_indices)

    def eval (self, env):
        vObj = self._obj.eval(env)
        vIndices = [index.eval(env).value for index in self._indices]

        v = vObj
        indices = vIndices
        while len(indices) > 0:
            if not v.type in ["array", "dictionary", "string"]:
                raise Exception ("Runtime error: cannot index {}".format(v.type))

            head, indices = indices[0], indices[1:]
            v = vObj.get(head)

        return v


class ELookupAssign (Exp):
    # Set value at index/key in an array, dictionary, or string
    # Can provide multiple indices -- e.g. arr[0]["a"] surface syntax
    # translates to abstract representation parameter indices = [0,"a"]
    # (useful for nesting arrays/dictionaries/strings)

    def __init__ (self, obj, indices, exp):
        self._obj = obj
        self._indices = indices
        self._exp = exp

    def __str__ (self):
        pretty_indices = ",".join([str(idx) for idx in self._indices])
        return "ELookupAssign({},{},{})".format(self._obj, pretty_indices,self._exp)

    def eval (self, env):
        vObj = self._obj.eval(env)
        vIndices = [index.eval(env).value for index in self._indices]

        v = vObj
        indices = vIndices
        while len(indices) > 1:
            if not v.type in ["array", "dictionary", "string"]:
                raise Exception ("Runtime error: cannot index {}".format(v.type))

            head, indices = indices[0], indices[1:]
            v = vObj.get(head)

        v.set(indices[0], self._exp.eval(env))
        return VNone()


class EVariableAssign (Exp):
    # Set value of a variable in the environment

    def __init__ (self, name, exp):
        self._name = name
        self._exp = exp

    def __str__ (self):
        return "EVariableAssign({},{})".format(self._refcell, self._exp)

    def eval (self, env):
        refcell = EId(self._name).eval(env)
        refcell.content = self._exp.eval(env)
        return VNone()


class EIf (Exp):
    # Conditional expression

    def __init__ (self,e1,e2,e3):
        self._cond = e1
        self._then = e2
        self._else = e3

    def __str__ (self):
        return "EIf({},{},{})".format(self._cond,self._then,self._else)

    def eval (self,env):
        v = self._cond.eval(env)
        if v.type != "boolean":
            raise Exception ("Runtime error: condition not a Boolean")
        if v.value:
            return self._then.eval(env)
        else:
            return self._else.eval(env)


class ELet (Exp):
    # local binding
    # allow multiple bindings
    # eager (call-by-avlue)

    def __init__ (self,bindings,e2):
        self._bindings = bindings
        self._e2 = e2

    def __str__ (self):
        return "ELet([{}],{})".format(",".join([ "({},{})".format(id,str(exp)) for (id,exp) in self._bindings ]),self._e2)

    def eval (self,env):
        new_env = [ (id,e.eval(env)) for (id,e) in self._bindings] + env
        return self._e2.eval(new_env)

class EId (Exp):
    # identifier

    def __init__ (self,id):
        self._id = id

    def __str__ (self):
        return "EId({})".format(self._id)

    def eval (self,env):
        for (id,v) in env:
            if self._id == id:
                return v
        raise Exception("Runtime error: unknown identifier {}".format(self._id))


class ECall (Exp):
    # Call a defined function in the function dictionary

    def __init__ (self,fun,exps):
        self._fun = fun
        self._args = exps

    def __str__ (self):
        return "ECall({},[{}])".format(str(self._fun),",".join(str(e) for e in self._args))

    def eval (self,env):
        f = self._fun.eval(env)
        if f.type != "function" and f.type != "procedure":
            raise Exception("Runtime error: trying to call a non-function")
        args = [ e.eval(env) for e in self._args]
        if len(args) != len(f.params):
            raise Exception("Runtime error: argument # mismatch in call")
        new_env = zip(f.params,args) + f.env
        return f.body.eval(new_env)


class EFunction (Exp):
    # Creates an anonymous function

    def __init__ (self,params,body,name=None):
        self._params = params
        self._body = body
        self._name = name

    def __str__ (self):
        return "EFunction([{}],{})".format(",".join(self._params),str(self._body))

    def eval (self,env):
        return VClosure(self._params,self._body,env,self._name)


class EProcedure (Exp):
    # Creates an anonymous function

    def __init__ (self,params,body):
        self._params = params
        self._body = body

    def __str__ (self):
        return "EProcedure([{}],{})".format(",".join(self._params),str(self._body))

    def eval (self,env):
        return VProcedure(self._params,self._body,env)

class ERefCell (Exp):
    # this could (should) be turned into a primitive
    # operation.  (WHY?)

    def __init__ (self,initialExp):
        self._initial = initialExp

    def __str__ (self):
        return "ERefCell({})".format(str(self._initial))

    def eval (self,env):
        v = self._initial.eval(env)
        return VRefCell(v)


class EDo (Exp):

    def __init__ (self,exps):
        self._exps = exps

    def __str__ (self):
        return "EDo([{}])".format(",".join(str(e) for e in self._exps))

    def eval (self,env):
        # default return value for do when no arguments
        v = VNone()
        for e in self._exps:
            v = e.eval(env)
        return v


class EWhile (Exp):

    def __init__ (self,cond,exp):
        self._cond = cond
        self._exp = exp

    def __str__ (self):
        return "EWhile({},{})".format(str(self._cond),str(self._exp))

    def eval (self,env):
        c = self._cond.eval(env)
        if c.type != "boolean":
            raise Exception ("Runtime error: while condition not a Boolean")
        while c.value:
            self._exp.eval(env)
            c = self._cond.eval(env)
            if c.type != "boolean":
                raise Exception ("Runtime error: while condition not a Boolean")
        return VNone()


class EFor (Exp):

    def __init__ (self, variable, array, body):
        self._variable = variable
        self._array = array
        self._body = body

    def __str__ (self):
        return "EFor({},{},{})".format(self._variable,self._array,self._body)

    def eval (self, env):
        vArray = self._array.eval(env)
        if vArray.type != "array":
            raise Exception ("Runtime error: cannot iterate over a {}".format(self._array.type))

        for (_, exp) in enumerate(vArray.elts):
            new_env = [(self._variable, ERefCell(EValue(exp)).eval(env))] + env
            self._body.eval(new_env)

        return VNone()


class EArray (Exp):
    # creates a mutable array
    def __init__ (self, elts):
        self._elts = elts

    def __str__ (self):
        pretty_elts = [str(elt) for elt in self._elts]
        return "EArray([{}])".format(pretty_elts)

    def eval (self, env):
        elts = [elt.eval(env) for elt in self._elts]
        return VArray(elts)


class EDictionary (Exp):
    # creates a mutable dictionary
    def __init__ (self, bindings):
        self._bindings = bindings

    def __str__ (self):
        pretty_bindings = ', '.join(["{}:{}".format(b[0], str(b[1])) for b in self._bindings])
        return "EDictionary[{}]".format(pretty_bindings)

    def eval (self, env):
        bindings = [(b[0], b[1].eval(env).value) for b in self._bindings]
        return VDictionary(bindings)


class EWith (Exp):
    def __init__ (self, arrExp, bodyExp):
        self._arrExp = arrExp
        self._bodyExp = bodyExp

    def __str__ (self):
        return "EWith({}, {})".format(str(self._arrExp), str(self._bodyExp))

    def eval (self, env):
        array = self._arrExp.eval(env)
        if array.type != "array":
            raise Exception ("Runtime error: expected an array")

        methods = [methodGenerator(env) for methodGenerator in array.methods]
        new_env = methods + env
        return self._bodyExp.eval(new_env)

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

    def __str__ (self):
        return str(self.value)


class VBoolean (Value):
    # Value representation of Booleans

    def __init__ (self,b):
        self.value = b
        self.type = "boolean"

    def __str__ (self):
        return "true" if self.value else "false"


class VString (Value):
    # Value representation of strings

    def __init__ (self,b):
        self.value = b
        self.type = "string"

    def __str__ (self):
        return self.value

    def get(self, idx):
        print "sth"
        return self.value[idx]


class VClosure (Value):
    # Value representation of closures

    def __init__ (self,params,body,env,name=None):
        self.params = params
        self.body = body
        self.name = name
        self.env = env
        self.type = "function"

    def __str__ (self):
        return "<function [{}] {}>".format(",".join(self.params),str(self.body))


class VProcedure (Value):

    def __init__ (self,params,body,env):
        self.params = params
        self.body = body
        self.env = env
        self.type = "procedure"

    def __str__ (self):
        return "<procedure [{}] {}>".format(",".join(self.params),str(self.body))


class VRefCell (Value):

    def __init__ (self,initial):
        self.content = initial
        self.type = "ref"

    def __str__ (self):
        return "<ref {}>".format(str(self.content))


class VArray (Value):

    def __init__ (self, elts):
        self.elts = elts
        self.type = "array"

    def __str__ (self):
        return "<arr [{}]>".format(",".join([str(elt) for elt in self.elts]))

    def get (self, idx):
        return self.elts[idx]

    def set (self, idx, v):
        self.elts[idx] = v


class VDictionary (Value):
    def __init__ (self, bindings):
        self.bindings = dict(bindings)
        self.type = "dictionary"

    def __str__ (self):
        pretty_bindings = ', '.join(["{}:{}".format(k, str(v)) for (k,v) in self.bindings.iteritems()])
        return "<dict [{}]>".format(pretty_bindings)

    def get (self, key):
        if key in self.bindings:
            return self.bindings[key] # just return the value, not the (key,value) tuple
        else:
            return VNone() # return none if not in dictionary

    def set (self, key, v):
        self.bindings[key] = v


class VNone (Value):

    def __init__ (self):
        self.type = "none"

    def __str__ (self):
        return "none"


# Primitive operations

def oper_plus (v1,v2):
    if v1.type == "integer" and v2.type == "integer":
        return VInteger(v1.value + v2.value)
    raise Exception ("Runtime error: trying to add non-numbers")

def oper_minus (v1,v2):
    if v1.type == "integer" and v2.type == "integer":
        return VInteger(v1.value - v2.value)
    raise Exception ("Runtime error: trying to subtract non-numbers")

def oper_times (v1,v2):
    if v1.type == "integer" and v2.type == "integer":
        return VInteger(v1.value * v2.value)
    raise Exception ("Runtime error: trying to multiply non-numbers")

def oper_zero (v1):
    if v1.type == "integer":
        return VBoolean(v1.value==0)
    raise Exception ("Runtime error: type error in zero?")

def oper_lt (v1, v2):
    if v1.type == "integer" and v2.type == "integer":
        return VBoolean(v1.value < v2.value)
    raise Exception ("Runtime error: type error in lt?")

def oper_lte (v1, v2):
    if v1.type == "integer" and v2.type == "integer":
        return VBoolean(v1.value <= v2.value)
    raise Exception ("Runtime error: type error in lte?")

def oper_gt(v1, v2):
    if v1.type == "integer" and v2.type == "integer":
        return VBoolean(v1.value > v2.value)
    raise Exception ("Runtime error: type error in gt?")

def oper_gte(v1, v2):
    if v1.type == "integer" and v2.type == "integer":
        return VBoolean(v1.value >= v2.value)
    raise Exception ("Runtime error: type error in gte?")

def oper_not(v1):
    if v1.type == "boolean":
        return VBoolean(not v1.value)
    raise Exception ("Runtime error: type error in not")

def oper_deref (v1):
    if v1.type == "ref":
        return v1.content
    raise Exception ("Runtime error: dereferencing a non-reference value")

def oper_update (v1,v2):
    if v1.type == "ref":
        v1.content = v2
        return VNone()
    raise Exception ("Runtime error: updating a non-reference value")

def oper_update_arr (varray, v1, v2): # array, index, new element
    if varray.type == "array":
        if v1.type == "integer":
            varray.set(v1.value, v2)
            return VNone()
    raise Exception ("Runtime error: invalid types for array update")

def oper_print (*args):
    print ", ".join(str(arg) for arg in args)
    return VNone()

def oper_do (v1):
    return VNone()

def oper_length (v1):
    if v1.type == "string":
        return VInteger(len(v1.value))
    elif v1.type == "array":
        return VInteger(len(v1.elts))
    raise Exception ("Runtime error: invalid types for length function")

def oper_substring (v1, v2, v3):
    if v1.type == "string" and v2.type == "integer" and v3.type == "integer":
        return VString(v1.value[v2.value:v3.value])
    raise Exception ("Runtime error: Improper arguements for substring function")

def oper_concat (v1, v2):
    if v1.type == "string" and v2.type == "string":
        return VString(v1.value + v2.value)
    raise Exception ("Runtime error: concat with non-string value(s)")

def oper_startswith (v1, v2):
    if v1.type == "string" and v2.type == "string":
        return VBoolean(v1.value.startswith(v2.value))
    raise Exception ("Runtime error: startswith with non-string value(s)")

def oper_endswith (v1, v2):
    if v1.type == "string" and v2.type == "string":
        return VBoolean(v1.value.endswith(v2.value))
    raise Exception ("Runtime error: endswith with non-string value(s)")

def oper_lower (v1):
    if v1.type == "string":
        return VString(v1.value.lower())
    raise Exception ("Runtime error: getting the lower of a non-string value")

def oper_upper (v1):
    if v1.type == "string":
        return VString(v1.value.upper())
    raise Exception ("Runtime error: getting the upper of a non-string value")

def oper_random (v1):
    if v1.type == "integer":
        return VInteger(random.randint(0, v1.value))
    raise Exception ("Runtime error: type error in random")



############################################################
# IMPERATIVE SURFACE SYNTAX
#



##
## PARSER
##
# cf http://pyparsing.wikispaces.com/

from pyparsing import Word, Literal, ZeroOrMore, OneOrMore, delimitedList, Keyword, QuotedString, Forward, alphas, alphanums, NoMatch, Optional


def initial_env_imp ():
    # A sneaky way to allow functions to refer to functions that are not
    # yet defined at top level, or recursive functions
    env = []
    env.insert(0, ("test_arr", VRefCell(VArray([VInteger(42),VInteger(43),VInteger(44)]))))
    env.insert(0, ("test_dict", VRefCell(VDictionary([('a',VInteger(42)),('b',VInteger(43))]))))
    env.insert(0,
               ("+",
                VRefCell(VClosure(["x","y"],
                                  EPrimCall(oper_plus,[EId("x"),EId("y")]),
                                  env))))
    env.insert(0,
               ("-",
                VRefCell(VClosure(["x","y"],
                                  EPrimCall(oper_minus,[EId("x"),EId("y")]),
                                  env))))
    env.insert(0,
               ("*",
                VRefCell(VClosure(["x","y"],
                                  EPrimCall(oper_times,[EId("x"),EId("y")]),
                                  env))))
    env.insert(0,
               ("zero?",
                VRefCell(VClosure(["x"],
                                  EPrimCall(oper_zero,[EId("x")]),
                                  env))))
    env.insert(0,
              ("lt?",
               VRefCell(VClosure(["x","y"],
                                 EPrimCall(oper_lt,[EId("x"),EId("y")]),
                                 env))))

    env.insert(0,
              ("lte?",
               VRefCell(VClosure(["x","y"],
                                 EPrimCall(oper_lte,[EId("x"),EId("y")]),
                                 env))))

    env.insert(0,
              ("gt?",
               VRefCell(VClosure(["x","y"],
                                 EPrimCall(oper_gt,[EId("x"),EId("y")]),
                                 env))))
    env.insert(0,
              ("gte?",
               VRefCell(VClosure(["x","y"],
                                 EPrimCall(oper_gte,[EId("x"),EId("y")]),
                                 env))))
    env.insert(0,
               ("not",
                VRefCell(VClosure(["x"],
                                  EPrimCall(oper_not,[EId("x")]),
                                  env))))
    env.insert(0,
               ("len",
                VRefCell(VClosure(["x"],
                                  EPrimCall(oper_length,[EId("x")]),
                                  env))))
    env.insert(0,
               ("substring",
                VRefCell(VClosure(["x","y","z"],
                                  EPrimCall(oper_substring,[EId("x"),EId("y"), EId("z")]),
                                  env))))
    env.insert(0,
               ("concat",
                VRefCell(VClosure(["x","y"],
                                  EPrimCall(oper_concat,[EId("x"),EId("y")]),
                                  env))))
    env.insert(0,
               ("startswith",
                VRefCell(VClosure(["x","y"],
                                  EPrimCall(oper_startswith,[EId("x"),EId("y")]),
                                  env))))
    env.insert(0,
               ("endswith",
                VRefCell(VClosure(["x","y"],
                                  EPrimCall(oper_endswith,[EId("x"),EId("y")]),
                                  env))))
    env.insert(0,
               ("lower",
                VRefCell(VClosure(["x"],
                                  EPrimCall(oper_lower,[EId("x")]),
                                  env))))
    env.insert(0,
               ("upper",
                VRefCell(VClosure(["x"],
                                  EPrimCall(oper_upper,[EId("x")]),
                                  env))))
    env.insert(0,
               ("random",
                VRefCell(VClosure(["x"],
                                  EPrimCall(oper_random,[EId("x")]),
                                  env))))
    return env


def parse_pj (input):
    ### EXPRESSIONS ###
    idChars = alphas+"_+*-?!=<>"

    pIDENTIFIER = Word(idChars, idChars+"0123456789")
    pIDENTIFIER.setParseAction(lambda result: EPrimCall(oper_deref,[EId(result[0])]))
    pINTEGER = Word("0123456789")
    pINTEGER.setParseAction(lambda result: EValue(VInteger(int(result[0]))))
    pBOOLEAN = Keyword("true") | Keyword("false")
    pBOOLEAN.setParseAction(lambda result: EValue(VBoolean(True if result[0] == "true" else False)))
    pSTRING = QuotedString('"', escChar="\\", multiline=True)
    pSTRING.setParseAction(lambda result: EValue(VString(result[0])))
    pPRIMITIVE = (pINTEGER | pBOOLEAN | pSTRING | pIDENTIFIER)

    pNAME = Word(idChars,idChars+"0123456789") # like an identifier but does not parse to EId

    pNAMES = "(" + Optional(delimitedList(pNAME, delim=","))("namelist") + ")"
    pNAMES.setParseAction(lambda result: [result["namelist"] if "namelist" in result else []])

    pEXPR = Forward()

    pPARAMS = "(" + Optional(delimitedList(pEXPR, delim=","))("paramlist") + ")"
    pPARAMS.setParseAction(lambda result: [result["paramlist"] if "paramlist" in result else []])

    pBINDING = pEXPR + "=" + pEXPR
    pBINDING.setParseAction(lambda result: [(result[0], result[2])])
    pBINDINGS = "(" + delimitedList(pBINDING,  delim=",")("bindinglist") + ")"
    pBINDINGS.setParseAction(lambda result: [result["bindinglist"]])

    pARRAY = "[" + Optional(delimitedList(pEXPR, delim=","))("array") + "]"
    pARRAY.setParseAction(lambda result: EArray(result["array"] if "array" in result else []))

    pENTRY = pNAME("_e1") + ":" + pEXPR("_e2")
    pENTRY.setParseAction(lambda result: [(result["_e1"], result["_e2"])])
    pDICTIONARY = "{" + Optional(delimitedList(pENTRY, delim=","))("dict") + "}"
    pDICTIONARY.setParseAction(lambda result: EDictionary(result["dict"] if "dict" in result else []))

    pFUNTOCALL = (pIDENTIFIER) # TODO allow more?
    pARGLISTS = OneOrMore(pPARAMS)
    pCALL = pFUNTOCALL("funtocall") + pARGLISTS("arglists")
    pCALL.setParseAction(lambda result: unpack_pcall(result["funtocall"], result["arglists"]))

    def mkExprFunBody (params,body):
        bindings = [ (p,ERefCell(EId(p))) for p in params ]
        return ELet(bindings,body)

    pANONUSERFUNC = "fun" + pNAMES("names") + pEXPR("expr")
    pANONUSERFUNC.setParseAction(lambda result: EFunction(result["names"], mkExprFunBody(result["names"], result["expr"])))

    pNAMEDUSERFUNC = "fun" + pNAME("name") + pNAMES("names") + pEXPR("expr")
    pNAMEDUSERFUNC.setParseAction(lambda result: EFunction(result["names"], mkExprFunBody(result["names"], result["expr"]), result["name"]))

    pOBJECTNAME = (pCALL | pIDENTIFIER | pSTRING) # TODO allow more?
    pOBJECTINDEX = "[" + pEXPR + "]"
    pOBJECTINDEX.setParseAction(lambda result: result[1])
    pOBJECTREST = OneOrMore(pOBJECTINDEX)
    pOBJECTLOOKUP = pOBJECTNAME("object") + pOBJECTREST("indices")
    pOBJECTLOOKUP.setParseAction(lambda result: ELookup(result["object"], result["indices"]))

    pCONDSTART = (pBOOLEAN) # TODO allow more
    pELSE = Keyword(":") + pEXPR("e2")
    pCOND = pCONDSTART("condition") + Keyword("?") + pEXPR("e1") + pELSE("else")
    pCOND.setParseAction(lambda result: EIf(result["condition"], result["e1"], result["else"]["e2"]))

    pPARENS = "(" + pEXPR  + ")"
    pPARENS.setParseAction(lambda result: result[1])

    pNOT = "not" + pEXPR("expr")
    pNOT.setParseAction(lambda result: EPrimCall(oper_not,[result["expr"]]))

    pLET = "let" + pBINDINGS("bindings") + pEXPR("expr")
    pLET.setParseAction(lambda result: ELet(result["bindings"], result["expr"]))

    pEXPR << (pLET | pNOT | pANONUSERFUNC | pNAMEDUSERFUNC | pPARENS | pCALL | pOBJECTLOOKUP | pCOND | pPRIMITIVE | pARRAY | pDICTIONARY)

    ### DECLARATIONS ####
    pBODY = Forward()

    pDEF_VAR = "var" + pNAME("name") + ";"
    pDEF_VAR.setParseAction(lambda result: (result["name"], EValue(VNone())))

    pDECL_VAR = "var" + pNAME("name") + "=" + pEXPR("expr") + ";"
    pDECL_VAR.setParseAction(lambda result: (result["name"], result["expr"]))

    def mkDefunBody (params,body):
        bindings = [ (p,ERefCell(EId(p))) for p in params ]
        return ELet(bindings,body)

    pDEFUN = "def" + pNAME('name') + pNAMES('names') + pBODY('body')
    pDEFUN.setParseAction(lambda result: (result["name"], EFunction(result["names"], mkDefunBody(result["names"], result["body"]), result["name"])))

    pDECL = (pDECL_VAR | pDEF_VAR | pDEFUN)

    pDECLS = ZeroOrMore(pDECL)
    pDECLS.setParseAction(lambda result: [result])

    ### BODY ###
    pSTMT = Forward()
    pSTMTS = ZeroOrMore(pSTMT)
    pSTMTS.setParseAction(lambda result: [result])

    pBODY << ("{" + pDECLS + pSTMTS + "}")
    pBODY.setParseAction(lambda result: mkBlock(result[1],result[2]))

    def mkBlock (decls,stmts):
        bindings = [ (n,ERefCell(expr)) for (n,expr) in decls ]
        return ELet(bindings,EDo(stmts))

    ### STATEMENTS ###
    pSTMT_DO = pEXPR + ";"
    pSTMT_DO.setParseAction(lambda result: EDo([result[0]]))

    pSTMT_PRINT = "print" + delimitedList(pEXPR, delim=",")("exprs") + ";"
    pSTMT_PRINT.setParseAction(lambda result: EPrimCall(oper_print,result["exprs"].asList()))

    pSTMT_IF = "if (" + pEXPR("expr") + ")" + pBODY("body")
    pSTMT_IF.setParseAction(lambda result: EIf(result["expr"],result["body"],EValue(VBoolean(True))))

    pSTMT_IFELSE = "if (" + pEXPR("expr") + ")" + pBODY("then") + "else" + pBODY("else")
    pSTMT_IFELSE.setParseAction(lambda result: EIf(result["expr"],result["then"],result["else"]))

    pSTMT_ASSIGN = pNAME("name") + "=" + pEXPR("expr") + ";"
    pSTMT_ASSIGN.setParseAction(lambda result: EVariableAssign(result["name"], result["expr"]))

    pSTMT_OBJECTASSIGN = pOBJECTNAME("object") + pOBJECTREST("indices") + "=" + pEXPR("expr") + ";"
    pSTMT_OBJECTASSIGN.setParseAction(lambda result: ELookupAssign(result["object"], result["indices"], result["expr"]))

    pSTMT_WHILE = "while (" + pEXPR("expr") + ")" + pBODY("body")
    pSTMT_WHILE.setParseAction(lambda result: EWhile(result["expr"],result["body"]))

    pSTMT_FOR = "for (" + pNAME("name") + "in" + pEXPR("expr") + ")" + pBODY("body")
    pSTMT_FOR.setParseAction(lambda result: EFor(result["name"], result["expr"], result["body"]))

    pSTMT << (pSTMT_PRINT | pSTMT_IFELSE | pSTMT_IF | pSTMT_WHILE | pSTMT_FOR |
              pSTMT_ASSIGN | pSTMT_OBJECTASSIGN | pSTMT_DO)

    ### TOP LEVEL ###
    pTOPEXPR = pEXPR.copy()
    pTOPEXPR.setParseAction(lambda result: {"result":"expression",
                                            "expr":result[0]})
    pTOPSTMT = pSTMT.copy()
    pTOPSTMT.setParseAction(lambda result: {"result":"statement",
                                            "stmt":result[0]})
    pTOPDECL = pDECL.copy()
    pTOPDECL.setParseAction(lambda result: {"result":"declaration",
                                            "decl":result[0]})
    pTOP = (pTOPSTMT | pTOPDECL | pTOPEXPR)

    result = pTOP.parseString(input)[0]
    return result # the first element of the result is the expression


def unpack_pcall(funtocall, arglists):
    head = arglists[-1]
    tail = arglists[:-1]

    if len(tail) == 0:
        return ECall(funtocall, head)
    else:
        return ECall(unpack_pcall(funtocall, tail), head)


def switch_pj (result, env):
    if result["result"] == "statement":
        stmt = result["stmt"]
        stmt.eval(env)

    elif result["result"] == "abstract":
        print result["stmt"]

    elif result["result"] == "quit":
        return

    elif result["result"] == "declaration":
        (name,expr) = result["decl"]
        v = expr.eval(env)
        env.insert(0,(name,VRefCell(v)))
        print "{} defined".format(name)

    return env


def shell_pj ():
    print "Homework 7 - PJ Language"
    env = initial_env_imp()

    while True:
        inp = raw_input("pj> ")

        try:
            result = parse_pj(inp)
            env = switch_pj(result, env)

        except Exception as e:
            print "Exception: {}".format(e)

if __name__ == "__main__":
    env = initial_env_imp()

    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            # load the program
            content = f.read()
            result = parse_pj(content)
            env = switch_pj(result, env)

            # call the main method
            result = parse_pj("main();")
            env = switch_pj(result, env)
    else:
        shell_pj()
