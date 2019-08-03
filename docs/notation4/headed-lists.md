# Headed lists

Notation3 and SPARQL often use a pattern called 'magic properties' to express
functions in a RDF-like way. In this pattern, the arguments to the function
are given as a list in the subject position, the function itself (or a name for
it) is the property, and the result is (usually a variable) in the object
position. For example, the addition of two people's heights might be expressed
as:

```
  (?height1 ?height2) math:add ?heightSum .
```

While this allows for a very straightforward mapping of functions to the graph
model of RDF, it can lead to hard to read expressions when you need to do
nested calculations. Getting the x-coordinate from a polar-to-cartesian
transformation becomes the following:

```
  (?theta) math:cos ?xFrac.
  (?r ?xFrac) math:multiply ?x.
```

As the expression becomes more nested, more and more variables are needed to
track intermediate results, and the meaning of the calculation becomes
harder and harder to understand.

Headed lists are a syntactic sugar in Notation4 that allow computations like
these to be expressed succinctly as easily as `(?r * math:cos(?theta))`, with
a purely mechanical translation to and from each syntax.

## A functional sugar

Imagine we have a headed list in object position:

```
  :s :p :h(:arg1 .. :argN).
```

This is equivalent to:

```
  (:arg1 .. :argN) :h ?newVar.
  :s :p ?newVar.
```

where `?newVar` is a fresh universal variable not used elsewhere.

Nested headed lists are translated from the *inside out*, so the following:

```
  :s :p :h1(:h2(:arg1 .. :argN)).
```

would become:

```
  (:arg1 .. :argN) :h2 ?newVar1.
  (?newVar1) :h1 ?newVar2.
  :s :p ?newVar2.
```

To reduce the visual noise of arithmetic, Notation4 has a syntax for infix
expressions that is first desugared to headed lists, then to a magic property
style. We can see this used in the coordinate transformation example. The
expression `(?r * math:cos(?theta))` is first desugared to:

```
  math:multiply(?r math:cos(?theta))
```

and then this becomes:

```
  (?theta) math:cos ?newVar1.
  (?r ?newVar1) math:multiply ?newVar2.
```

The mathematical expression syntax follows the normal rules for precedence and
has the following operators:

* Modular arithmetic (`mod`)
* Addition (`+`) and subtraction (`-`)
* Multiplication (`*`), division (`/`), and integer division (`%`)
* Exponentiation (`^`)

There is also an infix syntax for appending to lists (using `::`).

To use an infix expression, you must wrap it in parentheses as shown above.

## Binding and using results

The outermost fresh variable in the desugared representation is substituted
into the position the headed list appears. This allows headed lists to be
used for both constraining matches (allowing common patterns to be modularised)
and also as a way of calculating values.

To access the resulting value of a headed list, we can declare a variable in
lexical scope is symbolically the same (`log:equalTo`) as the fresh variable
from the desugaring process. This is so common, that Notation4 has a shorthand
for `log:equalTo`, the `=` operator.

Continuing with our coordinate transformations, we can finally fully sugar the
original calculation by declaring that `?x` is equal to the result variable:

```
  ?x = (?r * math:cos(?theta)).
```

Under the meaning of `log:equalTo`, this could be equivalently expressed as:

```
  (?r * math:cos(?theta)) = ?x
```

although the former is preferred for consistency with other, less logical
programming languages.

## Defining 'functions'

Combining headed lists with backward chaining gives a convenient way to define
your own functions.

Let's say we want to package our coordinate transformation as a single function
that can be reused. To do this, we could write a backward chaining rule like:

```
  { ?result = ex:polar-to-cartesian(?r ?theta) } 
    <- {
      ?result = ((?r * math:cos(?theta)) (?r * math:sin(?theta)))
    }
```

Standard backward chaining can then be used to bind `?result` appropriately,
and ensure it is treated as `log:equalTo` the desugaring process' fresh 
variable.

However, for the common situation where the result of the function is
determined by a calculation and does not rely on any special pattern matching
over the underlying graph, we can use a simpler syntax:

```
  ex:polar-to-cartesian(?r ?theta) <- ((?r * math:cos(?theta)) (?r * math:sin(?theta)))
```

This is desugared to the above, more standard, backward chaining rule.

## Symbolic programming

Sometimes, we don't merely want to *compute* some value, but rather we want to
transform the original computation to a new, easier to work with form. Such
rule-oriented programming has been the hallmark of homoiconic programming
languages, going by names such as 'macros' (in LISP), or 'downvalues' (in the
Wolfram Language). Notation4 has similar capabilities through its 'deep' rule
type.

A common example of this style of programming is symbolic differentiation. In
this problem, we are looking to automatically transform a mathematical 
expression to its derivative via a series of mechanical steps. This derivative
can then be used for exact calculations. Doing symbolic differentiation in
languages which are not homoiconic is awkward, and requires the computation to
be (re-)expressed indirectly. With homoiconic languages, code is data and so
can be transformed by other code just as easily.

Let's imagine defining a symbolic differentiation operator `ex:diff`. We can
do this by defining how it transforms different expressions using deep rule
application. For example, the way differentiation works with addition could be
written:

```
  {
    ex:diff((?f + ?g) ?x)
  } := { (ex:diff(?f ?x) + ex:diff(?g ?x)) }
```

Similar to the case for value-oriented functions, we support a sugaring for
the simplest left-hand side:

```
  ex:diff((?f + ?g) ?x) := (ex:diff(?f ?x) + ex:diff(?g ?x))
```