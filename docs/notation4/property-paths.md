# Property paths

Sometimes, the information you need from a graph is a long way from where you start. Getting to that information through basic graph patterns quickly becomes tedious. Worse, the sheer number of patterns required often obscures intent, making it harder to understand the code.

```
  { 
    ?person foaf:knows ?friend;
      foaf:name ?personName.
    ?friend foaf:knows ?friendOfAFriend.
    ?friendOfAFriend foaf:interest dbo:Soccer;
      foaf:name ?friendOfAFriendName.
  } ==> {
    # Now imagine writing a pattern to capture friends, friends-of-friends,
    # and friends-of-friends-of-friends who have a particular interest.
  }
```

This is why people were suggesting 'RDF path' syntaxes nearly as soon as RDF was first standardised. Many such syntaxes have been proposed over the years, from Versapath to RDFPath and even a simple syntax added to Notation3, but only one has stood the test of time: SPARQL 1.1's *property path* syntax.

Based on familiarity and power, Notation4 adopts and (moderately) extends this syntax. We allow the second component of any basic graph pattern to be an arbitrary path. With this, the above formula becomes:

```
  ?person (foaf:knows+)[foaf:interest dbo:Soccer]/foaf:name ?friendName.
```

Not only is this much more compact, but it produces more useful matches when you do not care about the intermediate resources you have to go through to get to the information you want to work with.

**Note**: Property paths can *only* be used in the antecedent side of a rule as they are intentionally ambiguous.

## Not just a convenient shorthand

As with SPARQL 1.1's property paths, those in Notation4 are more than just a pretty piece of syntactic sugar. Whilst the intermediate nodes are traversed, they do not contribute bindings to the match. This means that alternative ways of getting from the subject to the object do not cause a new rule firing. This is important to focus rule firings to things you care about, and reduce the number of redundant or duplicate firings.

For example, the previous query will only produce one binding per `?person` and `?friendName` pair (remembering that literals are always unique). This holds whether or not the pair have multiple mutual friends.

Our property path syntax also allows for deduplication of rules. To extend the soccer-loving friends query to match multiple lengths of `foaf:knows` chains would be challenging, and to support arbitrary lengths would be impossible. You might need to duplicate the consequent, or large chunks of the antecedent, for each depth you wanted to handle. With property paths, this becomes easy. You can add a repetition modifier (like the 'one-or-more' modifier on `foaf:knows` above) to any step in a path.

## Inverse paths

Sometimes, to go forwards you must go backwards. Inverse paths allow you to do this without fear. An inverse modifier on any path segment or subpath tells the reasoner to follow the links backwards, from tail to head.

Let's say we have a very simple data set that looks like:

```
  :Fido rdf:type :Dog
```

Then, the following will create the same matches:

```
  ?animal rdf:type :Dog.
  :Dog ^rdf:type ?animal.
```

Inverses can be applied to whole property paths too:

```
  ?friendName ^((foaf:knows+)[foaf:interest dbo:Soccer]/foaf:name) ?person.
```

They can also be used on subsections of a path.

## Sequences and alternatives

We can glue together properties head to tail by using the sequence operator `/`. The basic graph pattern `?a p/q ?b` produces the same matches as `?a p ?newVar. ?newVar q ?b.`, with `?newVar` being ignored. This can be chained into longer paths to traverse more of the graph.

Alternative paths can be expressed using the operator `|`. This can be applied to both individual properties, and whole paths. For example:

```
  ?person (foaf:member/^foaf:member)|foaf:knows ?accquaintance.
```

This will get everyone a person is friends with, or who are members of the same `foaf:Organization`.

## Repetition

There are four kinds of repetition that you can express by adding a suffix to a property path or subpath.

* Saying that a property or subpath should be followed **zero or more** times with a `*` suffix. For example `?person foaf:knows* ?otherPerson` will bind `?otherPerson` to everyone `?person` knows, everyone `?otherPerson` knows, and so on recursively. It will *also* bind `?otherPerson` to the same value as `?person`.

* Saying that a property or subpath should be followed **one or more** times with a `+` suffix.

* Saying that a property may *optionally* be followed with a `?` suffix.

* Saying that a property should be followed a certain number of times. Either an exact number of times (with `{n}`, where `n` is the number of time), or with a range using `{m, n}`, where it is followed between `m` and `n` times.

Repetition allows long, hard-to-understand and redundant chains to be reduced to their core essence.

## Negation

Notation4's semantics are a hybrid between open and closed world. As such, it has a notion of negation. The meaning of negation for a property path can be subtle, so we'll start with a more detailed example.

Imagine you have a software company. You want to produce a list of predicted suitability of all possible programming pairs so you can do some resource planning. This requires you first to enumerate all the pairs, but with an open world assumption this requires you to check that two distinct nodes do not denote the same person.

We can solve this problem using a negation operator. The negation operator is written `!` and is applied as a prefix to a path or subpath. In our case, we might write a pattern:

```
  ?programmer1 a ex:Programmer.
  ?programmer2 a ex:Programmer.
  ?programmer1 !owl:sameAs ?programmer2.
```

The meaning of `?a !p ?b` is to return all matches for `?a` and `?b` where they are not known to have the path `p` between them. So, for the above, this means matching `?programmer1` and `?programmer2` only if the system can't prove they are the same person.

Negations are powerful, and this means they need to be used carefully. It is worth remembering that in Notation4 a negative means 'can't be proven' *not* 'is false'.

## Filters

Filters are the first major extension that Notation4 has over SPARQL 1.1 property paths. A filter allows you to apply a restriction to traversal *without* breaking a path in two or introducing new bindings that could cause extra rule firings.

A filter is expressed using square brackets, similar to how you'd write a BNode expression. This is no coincidence. You can imagine the brackets as standing for an arbitrary match of the path to the left. You can then write whatever restrictions you'd like inside the brackets.

In the first example on this page, the expression `(foaf:knows+)[foaf:interest dbo:Soccer]` takes the result of traversing one or more `foaf:knows` links, and filters the resulting set to only those with a `foaf:interest` of `dbo:Soccer`. The same syntax as for BNodes applies, with the ability to add multiple statements. For example, to instead get only those who are interested in both soccer *and* cricket, you could use:

```
  (foaf:knows+)[foaf:interest dbo:Soccer, dbo:Cricket]
```

Sometimes, you'll want to write filters that add restrictions that cross-reference different properties of the filtered node. This can be done by binding variables inside the filter. Any variables bound in a filter *do not* become available outside the filter, preserving the execution properties of property paths.

As an illustration, imagine you have a set of graphics and you want to get all squares inside those graphics. Your vocabulary only has a notion of rectangle, so you need to find those rectangles where their width and height are equal. The following property path might be used:

```
  ?graphic (gr:hasPart+)[a gr:Rectangle; gr:height ?h; gr:width ?h] ?square.
```

The rest of the rule (and property path) never sees the variable `?h`, and so variation in it can never cause a new rule firing.

## Link prediction

While it would be lovely if everything were known for certain, in real world situations we often need to make our best guess. This goes doubly so for information systems, which often rely on a partial picture of the world. Of course, while we sometimes don't mind (or even welcome) uncertainty, we also often don't want a computer making its own inferences.

Property paths can be annotated to tell the Notation4 engine that it is OK to guess at the existence of a relationship. An engine can support many, or no, inference systems for this. The meaning of the annotation is just that it is OK to use inferencing in this situation. We expect various pragmas to be defined to allow parameters for this inferencing process to be defined.

The syntax for expressing a predicted relationship is a prefix `~`. As usual this can be applied to both individual properties, and to whole paths or subpaths. Asking for everyone a person knows, or may know is then as simple as `?person ~foaf:knows ?otherPerson`.

A crucial part of the semantics of the `~` annotation is that it *always* matches anything that is *known* to be true. This means that inference engines can only add to that set of known relationships. This is important in the context of what asserted knowledge means and truth maintenance.