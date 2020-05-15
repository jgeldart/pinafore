# Use-cases

## Fact representation

### Simple facts

> When representing information about an item in the world, you can express facts with minimum syntactic boilerplate.

The base use-case for Notation4 is expressing facts about things in the world. You should be able to express these facts quickly, precisely, and without lots of syntactic 'noise' (such as you might see in RDF/XML). This is the same base use-case as N3, where the goal was *scribblebility*: in N3, the idea was to create a notation that could be used in short IRC messages (which was the communication system used for lots of the early Semantic Web development).

### Multiple facts

> When representing information about an item in the world, you can express multiple facts simultaneously without lots of repetition.

Another basic requirement is that the amount of effort required to express additional information should be proportional to the amount of novel information that is added. That is, you should be able to express an additional data point or relationship about an item without repeating that item. The notation should be concise and precise.

### Relations

> When representing complex states of affairs, you can express n-ary relations between items compactly and cleanly.

<br>
### Rich data

> When dealing with concrete data, you can use a rich set of primitive data literals to precisely express some fact.

### Internationalization

> When working with data sets that must be usable by audiences across the globe, you can internationalize text for those audiences.

### Talking about facts

> When capturing information about provenance or argumentation structure, you can express facts about facts themselves.

### Talking about change

> When handling dynamic domains, you can express the truth validity period of a fact.

### Specialization for domains

> When working in a specialized domain with common patterns, you can create shorthands that allow you to reduce the boilerplate of those patterns.

## Knowledge representation
<br>
## Logic programming