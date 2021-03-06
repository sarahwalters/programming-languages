############################################################
# HOMEWORK 3
#
# Team members: Sarah Walters, Austin Greene
#
# Emails: sarah.walters@students.olin.edu, austin.greene@students.olin.edu
#
# Remarks:
#

import sys
from pyparsing import Word, Literal, Keyword, Forward, alphas, alphanums, OneOrMore, delimitedList, Group


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

    def eval (self,fun_dict):
        return self._value

    def substitute (self,id,new_e):
        return self


class EInteger (Exp):
    # Integer literal

    def __init__ (self,i):
        self._integer = i

    def __str__ (self):
        return "EInteger({})".format(self._integer)

    def eval (self,fun_dict):
        return VInteger(self._integer)

    def substitute (self,id,new_e):
        return self


class EBoolean (Exp):
    # Boolean literal

    def __init__ (self,b):
        self._boolean = b

    def __str__ (self):
        return "EBoolean({})".format(self._boolean)

    def eval (self,fun_dict):
        return VBoolean(self._boolean)

    def substitute (self,id,new_e):
        return self


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

    def eval (self,fun_dict):
        vs = [ e.eval(fun_dict) for e in self._exps ]
        return apply(self._prim,vs)

    def substitute (self,id,new_e):
        new_es = [ e.substitute(id,new_e) for e in self._exps]
        return EPrimCall(self._prim,new_es)


class EIf (Exp):
    # Conditional expression

    def __init__ (self,e1,e2,e3):
        self._cond = e1
        self._then = e2
        self._else = e3

    def __str__ (self):
        return "EIf({},{},{})".format(self._cond,self._then,self._else)

    def eval (self,fun_dict):
        v = self._cond.eval(fun_dict)
        if v.type != "boolean":
            raise Exception ("Runtime error: condition not a Boolean")
        if v.value:
            return self._then.eval(fun_dict)
        else:
            return self._else.eval(fun_dict)

    def substitute (self,id,new_e):
        return EIf(self._cond.substitute(id,new_e),
                   self._then.substitute(id,new_e),
                   self._else.substitute(id,new_e))


class ELet (Exp):
    # local binding
    # allow multiple bindings
    # eager (call-by-avlue)

    def __init__ (self,bindings,e2):
        self._bindings = bindings
        self._e2 = e2

    def __str__ (self):
        return "ELet([{}],{})".format(",".join([ "({},{})".format(id,str(exp)) for (id,exp) in self._bindings ]),self._e2)

    def eval (self,fun_dict):
        # by this point, all substitutions in bindings expressions have happened already (!)
        new_e2 = self._e2
        for (id,e) in self._bindings:
            v = e.eval(fun_dict)
            new_e2 = new_e2.substitute(id,EValue(v))
        return new_e2.eval(fun_dict)

    def substitute (self,id,new_e):
        new_bindings = [ (bid,be.substitute(id,new_e)) for (bid,be) in self._bindings]
        if id in [ bid for (bid,_) in self._bindings]:
            return ELet(new_bindings, self._e2)
        return ELet(new_bindings, self._e2.substitute(id,new_e))


class EId (Exp):
    # identifier

    def __init__ (self,id):
        self._id = id

    def __str__ (self):
        return "EId({})".format(self._id)

    def eval (self,fun_dict):
        raise Exception("Runtime error: unknown identifier {}".format(self._id))

    def substitute (self,id,new_e):
        if id == self._id:
            return new_e
        return self


class ECall (Exp):
    # Call a defined function in the function dictionary

    def __init__ (self,name,es):
        self._name = name
        self._exps = es

    def __str__ (self):
        return "ECall({},[{}])".format(self._name,",".join([ str(e) for e in self._exps]))

    def eval (self,fun_dict):
        vs = [ e.eval(fun_dict) for e in self._exps ]
        params = fun_dict[self._name]["params"]
        body = fun_dict[self._name]["body"]
        if len(params) != len(vs):
            raise Exception("Runtime error: wrong number of argument calling function {}".format(self._name))
        for (val,p) in zip(vs,params):
            body = body.substitute(p,EValue(val))
        return body.eval(fun_dict)

    def substitute (self,var,new_e):
        new_es = [ e.substitute(var,new_e) for e in self._exps]
        return ECall(self._name,new_es)



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


# Initial primitives dictionary
FUN_DICT = {
    "+": {"params":["x","y"],
          "body":EPrimCall(oper_plus,[EId("x"),EId("y")])},
    "-": {"params":["x","y"],
          "body":EPrimCall(oper_minus,[EId("x"),EId("y")])},
    "*": {"params":["x","y"],
          "body":EPrimCall(oper_times,[EId("x"),EId("y")])},
    "zero?": {"params":["x"],
              "body":EPrimCall(oper_zero,[EId("x")])},
    "square": {"params":["x"],
               "body":ECall("*",[EId("x"),EId("x")])},
    "=": {"params":["x","y"],
          "body":ECall("zero?",[ECall("-",[EId("x"),EId("y")])])},
    "+1": {"params":["x"],
           "body":ECall("+",[EId("x"),EValue(VInteger(1))])},
    "sum_from_to": {"params":["s","e"],
                    "body":EIf(ECall("=",[EId("s"),EId("e")]),
                               EId("s"),
                               ECall("+",[EId("s"),
                                          ECall("sum_from_to",[ECall("+1",[EId("s")]),
                                                               EId("e")])]))}
}

class EDef (Exp):

    def __init__ (self, e1, e2, e3):
        self._name = e1
        self._params= e2
        self._body= e3

    def __str__ (self):
        return "EDef({},{},{})".format(self._name,self._params,self._body)

    def eval (self,fun_dict):
        if type(self._params) is str:
            FUN_DICT[self._name] = {
                "params": [self._params],
                "body": self._body
            }
        elif type(self._params) is list:
            if all([isinstance(x, str) for x in self._params]):
                FUN_DICT[self._name] = {
                    "params": self._params,
                    "body": self._body
                }
            else:
                raise Exception ("params should be a list")



##
## PARSER
##
# cf http://pyparsing.wikispaces.com/


def parse (input):
    # parse a string into an element of the abstract representation

    # Grammar:
    #
    # <expr> ::= <integer>
    #            true
    #            false
    #            <identifier>
    #            ( if <expr> <expr> <expr> )
    #            ( let ( ( <name> <expr> ) ) <expr )
    #            ( + <expr> <expr> )
    #            ( * <expr> <expr> )
    #


    idChars = alphas+"_+*-?!=<>"

    pIDENTIFIER = Word(idChars, idChars+"0123456789")
    pIDENTIFIER.setParseAction(lambda result: EId(result[0]))

    # A name is like an identifier but it does not return an EId...
    pNAME = Word(idChars,idChars+"0123456789")

    pPARAMS = OneOrMore(Word(idChars, idChars+"0123456789"))

    pINTEGER = Word("-0123456789","0123456789")
    pINTEGER.setParseAction(lambda result: EInteger(int(result[0])))

    pBOOLEAN = Keyword("true") | Keyword("false")
    pBOOLEAN.setParseAction(lambda result: EBoolean(result[0]=="true"))

    pEXPR = Forward()

    pIF = "(" + Keyword("if") + pEXPR("e1") + pEXPR("e2") + pEXPR("e3") + ")"
    pIF.setParseAction(lambda result: EIf(result["e1"], result["e2"], result["e3"]))

    pBINDING = "(" + pNAME("name") + pEXPR("exp") + ")"
    pBINDING.setParseAction(lambda result: (result["name"], result["exp"]))

    pLET = "(" + Keyword("let") + "(" + OneOrMore(pBINDING)("bindings") + ")" + pEXPR("exp") + ")"
    pLET.setParseAction(lambda result: ELet(result["bindings"], result["exp"]))

    pPLUS = "(" + Keyword("+") + Group(pEXPR + OneOrMore(pEXPR))("exps") + ")"
    pPLUS.setParseAction(lambda result: recursiveExpand("+", result["exps"]))

    pTIMES = "(" + Keyword("*") + Group(pEXPR + OneOrMore(pEXPR))("exps") + ")"
    pTIMES.setParseAction(lambda result: recursiveExpand("*", result["exps"]))

    pUSERFUNC = "(" + pNAME("name") + OneOrMore(pEXPR)("params") + ")"
    pUSERFUNC.setParseAction(lambda result: ECall(result["name"], result["params"]))

    pEXPR << (pINTEGER | pBOOLEAN | pIDENTIFIER | pIF | pLET | pPLUS | pTIMES | pUSERFUNC)

    pDEF = "(" + Keyword("defun") + pNAME("name") + "(" + pPARAMS("params") + ")" + pEXPR("body") + ")"

    if pDEF.matches(input):
        res = pDEF.parseString(input)
        return {
            'result': "function",
            'name': res["name"],
            'params': res["params"].asList(),
            'body': res["body"],
        }
    elif pEXPR.matches(input):
        res = pEXPR.parseString(input)[0]
        return {
            'result': "expression",
            'expr': res,
        }
    else:
        raise Exception("PARSING ERROR: UNABLE TO PARSE")


def recursiveExpand(operation, args):
    if len(args) == 2:
        return ECall(operation, [args[0], args[1]])
    else:
        return ECall(operation, [args[0], recursiveExpand(operation, args[1:])])


def parse_natural (input):
    # parse a string into an element of the abstract representation
    # Math grammar from https://www.cs.rochester.edu/~nelson/courses/csc_173/grammars/parsetrees.html

    # Grammar:

    # <expr> ::= <integer>
    #            <boolean>
    #            <identifier>
    #            <math>
    #            ( <expr> )
    #            <boolean> <cond_rest>
    #            let ( <bindings> ) <expr>
    #            <name> ( <expr-seq> )

    # <math> ::= <plus>
    #            <minus>
    #            <math_expandable>
    # <math_expandable> ::= <times>
    #                       <math_nonexpandable>
    # <math_nonexpandable> ::= ( <math> )
    #                          <integer>
    # <plus> ::= <math_expandable> + <math>
    # <minus> ::= <math_expandable> - <math>

    # <cond_rest> :: ? <expr> : <expr>

    # <bindings> ::= <name> = <expr>, bindings
    #                <name> = <expr>

    # <expr_seq> ::= <expr>, <expr_seq>
    #                <expr>

    pEXPR = Forward()
    pPARENEXPR = Forward()
    pUSERFUNC = Forward()
    pMATH = Forward()
    pMATHEXPANDABLE = Forward()
    pMATHNONEXPANDABLE = Forward()

    idChars = alphas+"_+*-?!=<>"

    pIDENTIFIER = Word(idChars, idChars+"0123456789")
    pIDENTIFIER.setParseAction(lambda result: EId(result[0]))

    # A name is like an identifier but it does not return an EId...
    pNAME = Word(idChars,idChars+"0123456789")

    pINTEGER = Word("-0123456789","0123456789")
    pINTEGER.setParseAction(lambda result: EInteger(int(result[0])))

    pBOOLEAN = Keyword("true") | Keyword("false")
    pBOOLEAN.setParseAction(lambda result: EBoolean(result[0]=="true"))

    pCONDREST = Keyword("?") + pEXPR("e1") + Keyword(":") + pEXPR("e2")
    pCONDREST.setParseAction(lambda result: {"e1": result["e1"], "e2": result["e2"]})

    pBOOLEANRESULT = (pBOOLEAN | pPARENEXPR | pUSERFUNC)
    pIF = pBOOLEANRESULT("condition") + pCONDREST("exps")
    pIF.setParseAction(lambda result: EIf(result["condition"], result["exps"]["e1"], result["exps"]["e2"]))

    pPARENEXPR << "(" + pEXPR("exp") + ")"
    pPARENEXPR.setParseAction(lambda result: result["exp"])

    pPLUS = pMATHEXPANDABLE("math1") + Keyword("+") + pMATH("math2")
    pPLUS.setParseAction(lambda result: ECall("+", [result["math1"], result["math2"]]))

    pMINUS = pMATHEXPANDABLE("math1") + Keyword("-") + pMATH("math2")
    pMINUS.setParseAction(lambda result: ECall("-", [result["math1"], result["math2"]]))

    pTIMES = pMATHNONEXPANDABLE("math1") + Keyword("*") + pMATHEXPANDABLE("math2")
    pTIMES.setParseAction(lambda result: ECall("*", [result["math1"], result["math2"]]))

    pPARENMATH = "(" + pMATH("math") + ")"
    pPARENMATH.setParseAction(lambda result: result["math"])

    pMATH << (pPLUS | pMINUS | pMATHEXPANDABLE)

    pMATHEXPANDABLE << (pTIMES | pMATHNONEXPANDABLE)

    pMATHNONEXPANDABLE << (pPARENMATH | pINTEGER | pIF | pUSERFUNC | pIDENTIFIER)

    pBINDING = pNAME("name") + Keyword("=") + pEXPR("exp")
    pBINDING.setParseAction(lambda result: (result["name"], result["exp"]))

    pLET = Keyword("let") + "(" + delimitedList(pBINDING)("bindings") + ")" + pEXPR("exp")
    pLET.setParseAction(lambda result: ELet(result["bindings"], result["exp"]))

    pFUNCPARAM = (pIF | pMATH | pBOOLEAN | pINTEGER | pUSERFUNC | pIDENTIFIER)

    pUSERFUNC << pNAME("name") + "(" + delimitedList(pFUNCPARAM)("params") + ")"
    pUSERFUNC.setParseAction(lambda result: ECall(result["name"], result["params"]))

    pEXPR << (pIF | pBOOLEAN | pLET | pMATH | pUSERFUNC | pIDENTIFIER | pINTEGER | pPARENEXPR)

    if pEXPR.matches(input):
        res = pEXPR.parseString(input)[0] # the first element of the result is the expression
        return {
            'result': "expression",
            'expr': res,
        }
    else:
        raise Exception("PARSING ERROR: UNABLE TO PARSE")


def shell ():
    # A simple shell
    # Repeatedly read a line of input, parse it, and evaluate the result

    print "Homework 3 - Calc Language"
    while True:
        inp = raw_input("calc> ")
        if not inp:
            return
        res = parse(inp)
        if res['result'] == "expression":
            v = res['expr'].eval(FUN_DICT)
            print v
        else:
            name = res['name']
            params = res['params']
            body = res['body']
            EDef(name, params, body).eval(FUN_DICT)
            print(name + " added to functions")


def shell_natural ():
    # A simple shell with natural syntax
    # Repeatedly read a line of input, parse it, and evaluate the result

    print "Homework 3 - Natural Calc Language"
    while True:
        inp = raw_input("calc/nat> ")
        if not inp:
            return
        res = parse_natural(inp)
        print "Abstract representation:", res["expr"]
        v = res["expr"].eval(FUN_DICT)
        print v


# increase stack size to let us call recursive functions quasi comfortably
sys.setrecursionlimit(10000)

if __name__ == "__main__":
    shell_natural()
