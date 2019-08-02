# Literals

Notation4 recognizes a wide range of types of literal expression.

## Numbers

### Integers

```
  :John foaf:age 24 .
```

### Rationals

```
  :Project1 proj:riskRating 3/5 .
```

### Decimals

```
  :Project1 proj:hourlyRate 75.24 .
```

## Dates and times

### Dates

```
  :John foaf:birthDate 1994-05-02 .
```

```
  :John foaf:birthDate 1994-05-02Z .
```

### Times


```
  :timesheetRecord1 ts:startTime 08:49:04+01:00 .
```

```
  :timesheetRecord1 ts:startTime 08:49 .
```

### Datetimes

```
  :doc1 dc:created 2019-04-22T01:02:45.23Z .
```

### Durations

```
  :Project proj:duration P3M .
```

## Booleans

```
  :John proj:signedNDA true .
```

## Strings

### Single-line strings

```
  :John foaf:name "John" .
```

```
  :John foaf:name 'John' .
```

### Multi-line strings

```
  :Project1 dc:description """
    A project to project the projection of the project.
  """.
```

```
  :Project1 dc:description '''
    A project to... you get the idea.
  '''.
```