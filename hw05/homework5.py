############################################################
# HOMEWORK 5
#
# Team members: Austin Greene, Sarah Walters
#
# Emails: austin.greene@students.olin.edu, sarah.walters@students.olin.edu
#
# Remarks:
#



import sys

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
        prettyArgs = [str(arg) for arg in self._args]
        return "ECall({},{})".format(str(self._fun),prettyArgs)

    def eval (self,env):
        f = self._fun.eval(env)
        if f.type != "function":
            raise Exception("Runtime error: trying to call a non-function")
        args = [arg.eval(env) for arg in self._args]
        new_env = zip(f.params,args) + f.env()
        return f.body.eval(new_env)


class EFunction (Exp):
    # Creates an anonymous function

    def __init__ (self,params,body,name=None):
        self._params = params
        self._body = body
        self._name = name

    def __str__ (self):
        return "EFunction([{}],{})".format(self._params,str(self._body))

    def eval (self, env):
        return VClosure(self._params, self._body, env, self._name)


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


class VClosure (Value):

    def __init__ (self,params,body,env,name=None):
        self.params = params
        self.body = body
        self.name = name
        self._env = env
        self.type = "function"

    def env(self):
        if self.name:
            return [(self.name, VClosure(self.params, self.body, self._env, self.name))] + self._env
        else:
            return self._env

    def __str__ (self):
        return "<function [{}] {}>".format(self.params,str(self.body))



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


# Initial environment

# this initial environment works with Q1 when you've completed it

def initial_env ():
    # A sneaky way to allow functions to refer to functions that are not
    # yet defined at top level, or recursive functions
    env = []
    base = [
        ("+",
         VClosure(["x","y"],EPrimCall(oper_plus,
                                      [EId("x"),EId("y")]),
                  env)),
        ("-",
         VClosure(["x","y"],EPrimCall(oper_minus,
                                      [EId("x"),EId("y")]),
                  env)),
        ("*",
         VClosure(["x","y"],EPrimCall(oper_times,
                                      [EId("x"),EId("y")]),
                  env)),
        ("zero?",
         VClosure(["x"],EPrimCall(oper_zero,
                                  [EId("x")]),
                  env)),
        ("square",
         VClosure(["x"],ECall(EId("*"),[EId("x"),EId("x")]),
                  env)),
        ("=",
         VClosure(["x","y"],ECall(EId("zero?"),
                                  [ECall(EId("-"),[EId("x"),EId("y")])]),
                  env)),
        ("+1",
         VClosure(["x"],ECall(EId("+"),[EId("x"),EValue(VInteger(1))]),
                  env)),
        ("sum_from_to",
         VClosure(["s","e"],
                  EIf(ECall(EId("="),[EId("s"),EId("e")]),
                      EId("s"),
                      ECall(EId("+"),[EId("s"),
                                       ECall(EId("sum_from_to"),
                                             [ECall(EId("+1"),[EId("s")]),
                                              EId("e")])])),
                  env)),
    ]
    env.extend(base)
    return env



##
## PARSER
##
# cf http://pyparsing.wikispaces.com/

from pyparsing import Word, Literal, ZeroOrMore, OneOrMore, Keyword, Forward, alphas, alphanums


def letUnimplementedError ():
    raise Exception ("ERROR: let functionality not implemented yet")

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
    #            (function ( <name> ) <expr> )
    #            ( <expr> <expr> )
    #
    # <definition> ::= ( defun <name> ( <name> ) <expr> )
    #


    idChars = alphas+"_+*-~/?!=<>"

    pIDENTIFIER = Word(idChars, idChars+"0123456789")
    pIDENTIFIER.setParseAction(lambda result: EId(result[0]))

    # A name is like an identifier but it does not return an EId...
    pNAME = Word(idChars,idChars+"0123456789")

    pINTEGER = Word("0123456789")
    pINTEGER.setParseAction(lambda result: EValue(VInteger(int(result[0]))))

    pBOOLEAN = Keyword("true") | Keyword("false")
    pBOOLEAN.setParseAction(lambda result: EValue(VBoolean(result[0]=="true")))

    pEXPR = Forward()

    pIF = "(" + Keyword("if") + pEXPR + pEXPR + pEXPR + ")"
    pIF.setParseAction(lambda result: EIf(result[2],result[3],result[4]))

    pBINDING = "(" + pNAME + pEXPR + ")"
    pBINDING.setParseAction(lambda result: (result[1],result[2]))

    pBINDINGS = OneOrMore(pBINDING)
    pBINDINGS.setParseAction(lambda result: [ result ])

    pLET = "(" + Keyword("let") + "(" + pBINDINGS + ")" + pEXPR + ")"
    pLET.setParseAction(lambda result: transform_let(result[3], result[5]))

    pCALL = "(" + pEXPR('fun') + OneOrMore(pEXPR)('args') + ")"
    pCALL.setParseAction(lambda result: ECall(result['fun'], result['args'].asList()))

    pANONFUN = "(" + Keyword("function") + "(" + OneOrMore(pNAME)('args') + ")" + pEXPR('body') + ")"
    pANONFUN.setParseAction(lambda result: EFunction(result['args'].asList(),result['body']))

    pNAMEDFUN = "(" + Keyword("function") + pNAME('name') + "(" + OneOrMore(pNAME)('args') + ")" + pEXPR('body') + ")"
    pNAMEDFUN.setParseAction(lambda result: EFunction(result['args'].asList(),result['body'],result['name']))

    pFUN = (pANONFUN | pNAMEDFUN)

    pEXPR << (pINTEGER | pBOOLEAN | pIDENTIFIER | pIF | pLET | pFUN | pCALL)

    # can't attach a parse action to pEXPR because of recursion, so let's duplicate the parser
    pTOPEXPR = pEXPR.copy()
    pTOPEXPR.setParseAction(lambda result: {"result":"expression","expr":result[0]})

    pDEFUN = "(" + Keyword("defun") + pNAME('name') + "(" + OneOrMore(pNAME)('params') + ")" + pEXPR('body') + ")"
    pDEFUN.setParseAction(lambda result: {"result":"function",
                                          "name":result['name'],
                                          "params":result['params'].asList(),
                                          "body":result['body']})
    pTOP = (pDEFUN | pTOPEXPR)

    result = pTOP.parseString(input)[0]
    return result    # the first element of the result is the expression


def transform_let (bindings, letexp):
    functionParams = [binding[0] for binding in bindings]
    function = EFunction(functionParams, letexp)
    functionArgs = [binding[1] for binding in bindings]
    return ECall(function, functionArgs)


def shell ():
    # A simple shell
    # Repeatedly read a line of input, parse it, and evaluate the result

    print "Homework 5 - Func Language"
    print "#quit to quit"
    env = []

    ## UNCOMMENT THIS LINE WHEN YOU COMPLETE Q1 IF YOU WANT TO TRY
    ## EXAMPLES
    env = initial_env()
    while True:
        inp = raw_input("func> ")

        if inp == "#quit":
            return

        try:
            result = parse(inp)

            if result["result"] == "expression":
                exp = result["expr"]
                print "Abstract representation:", exp
                v = exp.eval(env)
                print v

            elif result["result"] == "function":
                # the top-level environment is special, it is shared
                # amongst all the top-level closures so that all top-level
                # functions can refer to each other
                env.insert(0,(result["name"],VClosure(result["params"],result["body"],env)))
                print "Function {} added to top-level environment".format(result["name"])

        except Exception as e:
            print "Exception: {}".format(e)



# increase stack size to let us call recursive functions quasi comfortably
sys.setrecursionlimit(10000)



def initial_env_curry ():
    # A sneaky way to allow functions to refer to functions that are not
    # yet defined at top level, or recursive functions
    env = []
    base = [
        ("+",
         VClosure(["x"],EFunction("y",EPrimCall(oper_plus,
                                              [EId("x"),EId("y")])),
                  env)),
        ("-",
         VClosure(["x"],EFunction("y",EPrimCall(oper_minus,
                                              [EId("x"),EId("y")])),
                  env)),
        ("*",
         VClosure(["x"],EFunction("y",EPrimCall(oper_times,
                                              [EId("x"),EId("y")])),
                  env)),
        ("zero?",
         VClosure(["x"],EPrimCall(oper_zero,
                                         [EId("x")]),
                           env)),
        ("square",
         VClosure(["x"],ECall(ECall(EId("*"),[EId("x")]),
                            [EId("x")]),
                  env)),
        ("=",
         VClosure(["x"],EFunction("y",ECall(EId("zero?"),
                                          [ECall(ECall(EId("-"),[EId("x")]),
                                                 [EId("y")])])),
                  env)),
        ("+1",
         VClosure(["x"],ECall(ECall(EId("+"),[EId("x")]),
                            [EValue(VInteger(1))]),
                  env)),
        ("sum_from_to",
         VClosure(["s"],EFunction("e",
                                  EIf(ECall(ECall(EId("="),[EId("s")]),[EId("e")]),
                                      EId("s"),
                                      ECall(ECall(EId("+"),[EId("s")]),
                                            [ECall(ECall(EId("sum_from_to"),
                                                         [ECall(EId("+1"),[EId("s")])]),
                                                   [EId("e")])]))),
                  env)),
    ]
    env.extend(base)
    return env


def parse_curry (input):
    # parse a string into an element of the abstract representation,
    # currying multi-argument functions

    # Grammar:
    #
    # <expr> ::= <integer>
    #            true
    #            false
    #            <identifier>
    #            ( if <expr> <expr> <expr> )
    #            ( let ( ( <name> <expr> ) ) <expr )
    #            (function ( <name> ) <expr> )
    #            ( <expr> <expr> )
    #
    # <definition> ::= ( defun <name> ( <name> ) <expr> )
    #


    idChars = alphas+"_+*-~/?!=<>"

    pIDENTIFIER = Word(idChars, idChars+"0123456789")
    pIDENTIFIER.setParseAction(lambda result: EId(result[0]))

    # A name is like an identifier but it does not return an EId...
    pNAME = Word(idChars,idChars+"0123456789")

    pINTEGER = Word("0123456789")
    pINTEGER.setParseAction(lambda result: EValue(VInteger(int(result[0]))))

    pBOOLEAN = Keyword("true") | Keyword("false")
    pBOOLEAN.setParseAction(lambda result: EValue(VBoolean(result[0]=="true")))

    pEXPR = Forward()

    pIF = "(" + Keyword("if") + pEXPR + pEXPR + pEXPR + ")"
    pIF.setParseAction(lambda result: EIf(result[2],result[3],result[4]))

    pBINDING = "(" + pNAME + pEXPR + ")"
    pBINDING.setParseAction(lambda result: (result[1],result[2]))

    pBINDINGS = OneOrMore(pBINDING)
    pBINDINGS.setParseAction(lambda result: [ result ])

    pLET = "(" + Keyword("let") + "(" + pBINDINGS + ")" + pEXPR + ")"
    pLET.setParseAction(lambda result: transform_let(result[3], result[5]))

    pCALL = "(" + pEXPR('fun') + OneOrMore(pEXPR)('args') + ")"
    pCALL.setParseAction(lambda result: call_curry(result['fun'], result['args'].asList()))

    pFUN = "(" + Keyword("function") + "(" + OneOrMore(pNAME)('params') + ")" + pEXPR('body') + ")"
    pFUN.setParseAction(lambda result: defun_curry(result['params'].asList(),result['body']))

    pEXPR << (pINTEGER | pBOOLEAN | pIDENTIFIER | pIF | pLET | pFUN | pCALL)

    # can't attach a parse action to pEXPR because of recursion, so let's duplicate the parser
    pTOPEXPR = pEXPR.copy()
    pTOPEXPR.setParseAction(lambda result: {"result":"expression","expr":result[0]})

    pDEFUN = "(" + Keyword("defun") + pNAME('name') + "(" + OneOrMore(pNAME)('params') + ")" + pEXPR('body') + ")"
    pDEFUN.setParseAction(lambda result: {"result":"function",
                                          "name":result['name'],
                                          "params":result['params'].asList(),
                                          "body":result['body']})
    pTOP = (pDEFUN | pTOPEXPR)

    result = pTOP.parseString(input)[0]
    return result    # the first element of the result is the expression


def defun_curry(params, body):
    head = params[0]
    tail = params[1:]

    if (tail == []):
        return EFunction([head], body)
    else:
        return EFunction([head], defun_curry(tail, body))


def call_curry(fun, args):
    # grab arguments from the end of the list so, e.g.,
    # (+ 2 3)
    # produces the same abstract representation as
    # ((+ 2) 3)
    head = args[-1]
    tail = args[:-1]

    if (tail == []):
        return ECall(fun, [head])
    else:
        return ECall(call_curry(fun, tail), [head])


def shell_curry ():
    print "Homework 5 - Func Language"
    print "#quit to quit"
    env = initial_env_curry()

    while True:
        inp = raw_input("func/curry> ")

        if inp == "#quit":
            return

        try:
            result = parse_curry(inp)

            if result["result"] == "expression":
                exp = result["expr"]
                print "Abstract representation:", exp
                v = exp.eval(env)
                print v

            elif result["result"] == "function":
                # the top-level environment is special, it is shared
                # amongst all the top-level closures so that all top-level
                # functions can refer to each other
                curried_fun = defun_curry(result["params"], result["body"]).eval(env)
                env.insert(0,(result["name"],curried_fun))
                print "Function {} added to top-level environment".format(result["name"])

        except Exception as e:
            print "Exception: {}".format(e)
