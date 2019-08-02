# Statements

# Making simple statements

```
  :John foaf:homepage <http://example.com/johnsmith>.
```

## Referencing things with IRIs and CURIES

## Don't repeat yourself

### Multiple objects

```
  :John ex:hasVisited <http://www.google.com>.
  :John ex:hasVisited <http://www.w3.org>.
```

```
  :John ex:hasVisited <http://www.google.com>, <http://www.w3.org>.
```

### Multiple predicates

```
  :John foaf:homepage <http://example.com/johnsmith>;
    ex:hasVisited <http://www.google.com>, <http://www.w3.org>.
```

## Some convenient shorthands

### Declaring something's type

```
  :John a foaf:Person .
```

### Things without names

```
  [

  ]
```

```
  [
    :- _:x
  ]
```

### Logical relationships

```
  :dog123 === :dog444 .
```

```
  :dog123 !== :dog444 .
```

```
  ?x == 2 .
```

```
  ?x =/= 3 .
```

```
  ?x in (2 3) .
```

### Mathematical relationships

```
  (2 2) math:add ?x .
  ?x = 4 .
```

```
  (2 2) math:add ?x .
  ?x != 5 .
```

```
  2 > 1 .
  2 < 5 .
  2 >= 2 .
  3 <= math:pi .
```

### The meaning of things

```
  <> |- this .
```

```
  <facts.n4> |= ?conclusions .
```

