# Introduction

## Features

* Rich programming model allows for knowledge-informed computations.
* Graph-oriented rather than tree-oriented.
* Can be used both 'one-shot', and to express continuously changing knowledge.
* Combines forward-chaining, backward-chaining, and streaming rules into a single language.
* Supports integration with subsymbolic reasoning like neural link prediction.
* A natural and comfortable extension of Notation3 and SPARQL.
* Future-oriented with a design based on an RDF\* world.

## Design principles

### Knowledge-driven

Computation is contextual. Traditionally, that context is kept in an external system and using it requires a lot of ceremony. In Notation4, the knowledge that can determine what to do and the best way to do it is pervasively available to the code.

### Partial world assumption

Notation4 dances on the edge between open world reasoning and the closed world assumption. Much like *cwm* before it, the ability to selectively assume total knowledge makes certain computations possible without significantly impacting the ability for different systems to work together.

### Homoiconic

Homoiconic systems are often described pithily as those where 'code is data, data is code'. Everything in Notation4 is expressed as (nested sets of) RDF graphs, the same as the underlying knowledge. This lets rules blend code with data. Unlike existing homoiconic systems, which are list or tree oriented ours is graph-oriented through and through, allowing rich introspection and pattern matching.

### Concise

The right level of concision is important for maintainability. Notation3, Adenine, and other linked data languages have often made the graph-oriented aspects concise, but at the expense of the more traditional computational elements of programming. Notation4 strives to strike a balance between the two, allowing computational thinking to be used with pervasive knowledge.

## A historical perspective

I've been working on the main ideas in Notation4 since the early 2000s. The key idea of modelling complex web-based information systems as a set of simpler interacting agents (in an 'active' web) prioritising *coherence* over *strong consistency* was a major focus of my academic research from 2005 to 2009. Notation4 is designed to be a programming language for the active web.

Its main inspirations and influences are, in no particular order:

* Tim Berners-Lee's Notation3 and the *cwm* reasoner for it.
* Adenine, the programming language built for the Haystack semantic desktop.
* Prolog and the query-oriented logic programming model
* LISP for its simple underlying, homoiconic model
* Wolfram Language for its application of the LISP model to provide rich, rule-oriented symbolic computing.
* SPARQL for making querying complex graphs simple.
* Ripple and the vision of linked programs for linked data.