# Pattern Matching

## Problem
We implemented functional-style match statements. Match statements are like switch statements: they compare an input to a list of cases and evaluate the result which corresponds to the first case the input matches. The match statement we implemented is more powerful than a switch statement in that it is able to "unpack" array inputs, either by defining variables for every element of an array of a certain length or by defining variables for the array's head (first element) and tail (array of the non-head elements). Because pattern-matching is often able to "unpack" array inputs like this, it's commonly used to implement recursion over arrays.

Also, the OCaml documentation calls match statements a "Cool Feature"... so, we figured this would be a Cool Project.

## Approach
We added match statements to [one of Riccardo's sample languages](http://rpucella.net/courses/pl-fa16/code-lect-10-types.py) (the one with typechecking). We implemented a `pMATCH` nonterminal, an `EMatch` expression, and a group of `Pattern` classes. We also added simple arrays to the language so we could pattern-match on arrays -- but that's nothing new.

## Solution
### Surface Syntax
Here's the surface syntax for a simple function which uses a match statement to count the length of an array:

```
(defun length (xs) (array) (
	match xs with
	| [] : 0
	| h :: t : (+ 1 (length t))
))
```

### Parsing
On the parsing side, we added a `pMATCH` nonterminal.

```
pMATCH = "(" + Keyword("match") + pEXPR("exp") + Keyword("with") + OneOrMore(pPATTERN)("patterns") + Optional(pDEFAULT)("default") + ")"
```

The `pMATCH` nonterminal depends on `pEXPR` (defined as we've been defining it) and two helper nonterminals, `pPATTERN` and `pDEFAULT`.

The `pPATTERN` nonterminal is defined as follows:

```
pPATTERN = Keyword("|") + (pPATTERN_INSTANCEOF | pPATTERN_LESSTHAN | pPATTERN_GREATERTHAN | pPATTERN_EQUAL | pPATTERN_ARRAYUNPACK | pPATTERN_ARRAYMATCH) + Keyword(":") + pEXPR("res")
```

Each of the specific `pPATTERN_...` nonterminals (`pPATTERN_LESSTHAN`, etc) specifies a single pattern which an input can match. For instance, `pPATTERN_LESSTHAN` is defined as follows:

```
pPATTERN_LESSTHAN = Keyword("<") + pEXPR("exp")
```

The `pDEFAULT` nonterminal is for specifying a default result for the match statement -- what is evaluated if none of the specified patterns match the input. It is defined as follows:

```
pDEFAULT = Keyword("|") + Keyword("default") + ":" + pEXPR("default")
```

### Abstract Syntax Tree
On the syntax tree side, we added an `EMatch` expression class and a pattern system (base class `Pattern`, child classes `PInstanceOf`, `PLessThan`, `PGreaterThan`, `PEquals`, `PArrayUnpack`, `PArrayMatch`).

The `EMatch` class takes as arguments an input expression which is an `Exp`, a list of (pattern, result) tuples where the patterns are `Pattern`s and the results are `Exp`s, and an optional default result which is an `Exp`.
- `typecheck`ing an `EMatch` involves typechecking each result, making sure all of the result types are the same, and returning the most specific type. Typechecking a result is easy in the `PInstanceOf`, `PLessThan`, `PGreaterThan`, and `PEquals` cases -- the pattern doesn't define new variables, so the `symtable` has everything it needs to be specific abou the result's type. However, typechecking a `PArrayUnpack` (| h :: t) or a `PArrayMatch` (| [a, b, c]) is a little more complicated because our arrays aren't typed -- when you unpack elements from an array you don't know what types you're getting. As a workaround, we specify that the elements unpacked from arrays have type `TAny()`, and in many cases the rest of the match statement is structured such that we're able to make a better guess about the type it evaluates to when we look at all of the result types together and choose the most specific one. We also thought about typing our arrays but decided not to for the sake of simple surface syntax.
- `eval`ing an `EMatch` is fairly simple: run through its list of (pattern, result) tuples and return the `eval` of the result which corresponds to the first pattern the input matches. If no pattern matches and there's a default, return the `eval` of the default; if there's no default, throw a "can't match" exception.

The classes in the `Pattern` system are essentially predicates: each has a `matches` method that takes two arguments, the expression to test (an `Exp`) and the environment, and returns `True` or `False`. As an example, here's the class definition for `PLessThan`:

```
class PLessThan (Pattern):
    def __init__ (self, exp):
        self._exp = exp
        self.patternType = "PLessThan"

    def __str__ (self):
        return "PLessThan({})".format(self._exp)

    def matches (self, expToTest, env):
        vToTest = expToTest.eval(env)
        v = self._exp.eval(env)
        return vToTest.type.isEqual(TInteger()) and vToTest.value < v.value
```

## Demo
The `programs` directory contains sample programs. To run a program, execute `python project.py programs/filename.rm`, using the filename of the program in question.

## Reflection
Overall, the implementation worked smoothly -- in fact, we started by coming up with class definitions for `EMatch` and the `Pattern`s, then we implemented the parser and the syntax tree separately... and when we glued them together, everything just worked.

Two things we're thinking of improving:
- Because arrays aren't typed, when we unpack them with match patterns we don't know what types we're getting. We could type the arrays... maybe explicitly, maybe implicitly. Advice?
- We're having trouble thinking of uses for instance-of pattern-matching... would love pointers towards interesting applications.
