# A Gentle Guide to Notation4 for the Hungry

Notation4 is a high-level ontology and knowledge representation language that makes it easy to create and maintain domain knowledge. This document introduces the concepts and syntax gradually, helping you understand the philosophy behind the language and how you can use it to model your own domains.

You can think of Notation4 as a programming language for knowledge. We will, therefore, come at modelling from the perspective of human-centred design with a clear motivating scenario. The running example used is of a takeaway pizza restaurant looking to model its delicious food and its relationships with its customers. At each step, you will learn new concepts from the language as we build them a bespoke ontology.

## Scenarios and competency questions

As with any ontology, it is good practice to start by defining the core scenarios you intend to capture and the questions users may want to answer. Our takeaway restaurant prides itself on the quality and healthiness of its food. It is looking to make it easier for potential customers to find pizzas that are good for them as well as their budget. To that end, the restaurant wants to provide machine readable descriptions of its menu and ordering services.

After some thought, they decide the key competency questions they want potential customers to be able to answer are:

* What pizzas can I get in a particular category?
* What ingredients are in a pizza?
* What bases are available?
* Which pizzas have which base?
* What sizes are available for a particular combination?
* What changes can I make to a particular pizza?
* What is the nutritional information for a particular pizza?
* How much does a pizza cost?
* How much is the delivery charge?
* How long can I expect to wait for delivery based on my location?
* What are the terms and conditions for buying a pizza?
* What terms can we use to talk about pizzas when I call you?

With those questions in mind, let us start modelling!

## Getting started

Like a good pizza chef, we must start by preparing our workspace by making a file, `pizza.n4`, to contain our creation. The file extension `n4` is the standard extension for Notation4 files. Each Notation4 file starts with a declaration saying what kind of knowledge we are representing. For the moment, we are only interested in creating an ontology so let's start our file:
<br>
```
ontology <https://example.com/healthy-pizzas/0.1#>.
```

The keyword `ontology` tells software reading this file that it should expect an ontology (that is, a collection of definitions of concepts from a domain). The bit in the angle brackets, `<https://example.com/healthy-pizzas/0.1#>`, is a unique identifier for this ontology and the concepts we're going to define. We use IRIs to identify ontologies. A good IRI is one that we control, and where we can place the compiled ontology once we're ready to share it with the world. This stops our definitions clashing with others, and allows users' software to look up (the fancy term for this is 'dereference') our concepts to find out what they mean and how to use them.

It is good practice to provide a little metadata about our ontology so that people can understand it a little easier. Notation4 allows us to add annotations to the ontology declaration. Let's help users out by adding some annotations for the title, a description, and a version:
<br>
```
ontology <https://example.com/healthy-pizzas/0.1#>;
  title "Healthy Pizzas";
  version "0.1";
  description """
  An ontology for the Healthy Pizza Restaurant, providing customers with easy access to the best pizzas in the world
  """
.
```

The key-value pairs after the ontology IRI describe the metadata. The key of each pair is called the annotation's *predicate*. The value is called its *object*. In this case, all the values are strings (in one case, a multiline string). However, we aren't limited to strings for objects! Predicates might also take booleans, numbers (of various sorts), dates, times, and even durations. You can also add more structured objects. Let's add a creator, so search engines know which maestro was responsible for this glorious confection:
<br>
```
ontology <https://example.com/healthy-pizzas/0.1#>;
  title "Healthy Pizzas";
  version "0.1";
  description """
  An ontology for the Healthy Pizza Restaurant, providing customers with easy access to the best pizzas in the world
  """;
  creator [
    a foaf:Person;
    foaf:mbox <mailto:joe@example.com>;
    foaf:mbox <mailto:sales@example.com>;
    foaf:homepage <http://www.example.com>, <https://www.example.com>;
  ]
.

import <http://xmlns.com/foaf/0.1/> as foaf.
```
<br>
There are a few new pieces of syntax here. Firstly, we introduce an anonymous individual as the object of the creator predicate using the `[ ... ]` syntax. An anonymous individual is one where we don't care about the IRI: the software reading the file can make up any identifier it likes. Within the square brackets, you can define any predicate-object pairs you like to add information about the individual.

In this case, we first want to say this individual is a person, so we use the special predicate `a` to declare its type. Declaring types is optional, one of the benefits of ontologies is that types can often be inferred, but good practice. The object of this predicate is a special sort of value called a qualified name (or QName for short). QNames are namespaced identifiers, letting us modularise our ontologies and reference the good work of other people. The bit before the colon (`foaf` in this case) is called the prefix of the QName and the bit after (`Person` here) is called the local name. To use a QName, we must tell our users what the prefix means. We do that with the `import` statement in the last line above, saying that QNames with the prefix `foaf` refer to concepts from the ontology with the IRI `http://xmlns.com/foaf/0.1/`.

Since ontologies are identified by IRIs, it makes sense to be able to use IRIs to identify other things. We use that to identify the creator's mailbox using a `mailto` link. We use the same angle bracket syntax to indicate that the value is an IRI. In this case, we have two mailboxes and two homepages for this person. This is perfectly allowed in Notation4, and we don't need to force ordering on unordered duplicate predicates like this. We can either use the same predicate twice (as above with `foaf:mbox`) or separate the multiple objects using commas (see `foaf:homepage`).

With that done, we are ready to begin defining some concepts.

### Review

In this section we have learnt:

* How to start defining an ontology;
* How to add annotations to describe metadata about an ontology;
* The different types of value available in Notation4 (IRIs, QNames, literals);
* How to introduce anonymous individuals to provide more complex metadata;
* How to provide more than one value for a predicate; and
* How to import ontologies and give them a pithy prefix.

## I bake, therefore I am

We should always try to reuse existing ontologies where possible. For this work, we're going to make use of the [FOODON](https://www.ebi.ac.uk/ols/ontologies/foodon) ontology, developed by the [OBO Foundry](http://www.obofoundry.org/). This is a broad ontology of concepts related to food and its production, making it an ideal starting point for our definitions. We add an import for the ontology to the top of our file, below the import for FOAF:
<br>
```
import <http://purl.obolibrary.org/obo/FOODON> as foodon.
```

FOODON uses the OBO convention for naming things using numeric IDs, which can be a bit unwieldy so let's alias a couple of relevant terms to something more convenient first:
<br>
```
class PizzaCrust ~= foodon:_03317327.

class PizzaSauce ~= foodon:_03306786.
```

The `class` keyword says that we're introducing a new type of entity with a given name. In this case, we're using QNames without a prefix which means they use the ontology's IRI. The `~=` operator says that the class on the left is *equivalent* to the one on the right. Equivalence means that whenever we have an individual of type `PizzaSauce`, say, we can treat it as also being of the type `foodon:_`<span class="colour" style="color:rgb(252, 246, 255)">`03306786` (and vice versa). We want to be less strict with our pizzas, however, as they're a specialised category of things onto themselves. We can do that by using the *subclass* operator, `<|`, instead:</span>
<br>
```
class Pizza <| foodon:_03310775;
  status "testing";
  label "pizza".
```

<span class="colour" style="color:rgb(252, 246, 255)">As can be seen, we can add annotations to classes just like we can to ontologies. In this case, we're giving the class a label and telling user's what its status is (a useful thing to do particularly while you're developing an ontology).</span>

<span class="colour" style="color:rgb(252, 246, 255)">We also want to define our own predicates. There are two important types of predicate to consider:</span>

* **Properties:** which relate two individuals together; and
* **Attributes:** which relate an individual with some literal value (such as a number or string).

Start by defining a property for our bases:
<br>
```
property has_base <| foodon:_00001563;
  status "stable";
  label "has base".
```

The `<|` operator here means that `has_base` is a *subproperty* of <span class="colour" style="color:rgb(252, 246, 255)">`foodon:_00001563` (the </span>['has defining ingredient'](https://www.ebi.ac.uk/ols/ontologies/foodon/properties?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FFOODON_00001563)<span class="colour" style="color:rgb(252, 246, 255)"> property). Once again, we add some annotations for our users.</span>

<span class="colour" style="color:rgb(252, 246, 255)">This is all well and good, but we would like to say what types of individuals this property can relate. This is called the *domain* (for the left side) and *range* (for the right side) of the predicate. Let's say that this property relates a `Pizza` with a `PizzaCrust`:</span>
<br>
```
property has_base <| foodon:_00001563;
  <| with domain Pizza with range PizzaCrust;
  status "stable";
  label "has base".
```

Now, whenever a piece of software sees an individual on the left side of a `has_base` assertion it can infer that this individual is a `Pizza` (and that the individual on the right is a `PizzaCrust`).

We can define a property for toppings similarly using the more general ['has ingredient'](https://www.ebi.ac.uk/ols/ontologies/foodon/properties?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FFOODON_00002420) property (from now on, we will skip the annotations unless they are relevant):
<br>
```
property has_topping <| foodon:_00002420;
  <| with domain Pizza.
```

Note that we have only defined the domain of this property, not the range.

Some toppings are special, in that they define the type of pizza we're dealing with. Let's create a new property for these toppings:
<br>
```
property has_defining_topping ~= has_topping and foodon:_00001563.
```

Here we have said that our `has_defining_topping` property is equivalent in meaning to being both `has_topping` and the FOODON has defining ingredient property. That is, when we assert that property it is the same thing as asserting the other two (and vice versa).

We can wrap up this section by adding a little more meaning to our `Pizza` class. We'll alter our previous definition to say that our pizzas must have only bases that are `PizzaCrusts` and that they must have a topping that's a `PizzaSauce`:
<br>
```
class Pizza <| foodon:_03310775;
  <| has_base only PizzaCrust and has_topping a PizzaSauce;
  status "testing";
  label "pizza".
```

Instead of saying `Pizza` is a subclass of another simple class, in this case we're using a *class expression* to state more complex relationships. The `only` keyword is used to assert that whenever an individual of type `Pizza` has a predicate of `has_base` then the object can only be a `PizzaCrust`. The `a` keyword says that any individual of type `Pizza` **must** be related to some instance of type `PizzaSauce` by the `has_topping` property. This makes precise the informal description above.

### Exercises

* Add some extra annotations to one of the classes

### Review

In this section we have learnt:

* How to declare classes and properties;
* How to define equivalences between classes and properties;
* How to define subclass and subproperty relationships;
* What the domain and range of a property are, and how to declare them;
* That we can define complex meanings for classes and properties through expressions; and
* Basic examples of class and property expressions.

## Non-taxing taxonomies

Our customers want to be able to easily browse and search for the perfect pizza for their current cravings. To help them do that, we will define some categories, in the form of classes, that can be used to organize our pizzas. These classes will form a taxonomy that can be used to perform [Ontology Based Data Access](http://optique-project.eu/training-programme/module-introduction-to-ontology-based-data-access/) (OBDA). This is a powerful, yet simple, way to use ontologies to improve an information system.

Our first categories will be around our bases. The restaurant sells pizzas with four types of crust. We can quickly define them with simple subclassing:
<br>
```
class StandardCrust <| PizzaCrust.
class ItalianStyleCrust <| PizzaCrust.
class GlutenFreeCrust <| PizzaCrust.
class ThinGlutenFreeCrust <| GlutenFreeCrust.
```

However, on second thought, we want to provide a bit more information about our gluten-free crusts. To do this, add a new import for the [Human Phenotype](https://www.ebi.ac.uk/ols/ontologies/hp) and [Relation](http://www.obofoundry.org/ontology/ro.html) ontologies, and use their concepts to assert that our gluten-free crusts do not trigger gluten intolerance:
<br>
```
import <http://purl.obolibrary.org/obo/HP> as hp.
import <http://purl.obolibrary.org/obo/RO> as ro.

...

property causes_allergic_reaction ~= ro:_0001020.
class GlutenIntolerance ~= hp:_0012538.
class GlutenFreeCrust <| PizzaCrust and not causes_allergic_reaction a GlutenIntolerance.
```

We can now define a class for gluten-free pizzas:
<br>
```
class GlutenFreePizza <| Pizza that has_base only GlutenFreeCrust.
```

Customers with a gluten-intolerance can now find safe-to-eat pizzas by looking for all inferred subclasses of `GlutenFreePizza`.

Continuing to build out out our taxonomy, we will define some other classes representing common customer queries:
<br>
```
class VegetarianFoodProduct ~= foodon:_00003194.
property derived_from ~= ro:_0001000.
class MammalianMilk ~= foodon:_03315150.

class VegetarianPizza <| Pizza that has_topping only VegetarianFoodProduct.
class VeganPizza <| VegetarianPizza that has_topping only not (MammalianMilk or derived_from a MammalianMilk).

class SimplePizza ~= Pizza that has_topping max 3 object.
class FullyLoadedPizza ~= Pizza that has_defining_topping min 6 object.
```

Since this is a knowledge-based approach, we can continually evolve our categories to meet changing customer needs. By defining the categories in terms of more primitive facts, as soon as we add the class it will automatically apply to all relevant individuals and subclasses. Say goodbye to lots of tedious, manual, and error-prone tagging work.

### Exercises

* Define your own crust class
* Define some additional categories that you think customers will want to search for using the properties we defined above and concepts from FOODON

### Review

In this section, we have learnt:

* The benefits of using ontologies for organizing and querying in everyday information systems;
* How to quickly define human-centred taxonomies by declaring classes that capture the meaning of each category;
* The ease with which we can combine concepts across multiple ontologies (here, FOODON, HP, and RO); and
* How to build more complex expressions including cardinality constraints (`max`/`min`), complements (`not`), and disjunctions (`or`).

## Portion control

To let you in on a secret, one of the main reasons that our healthy Italian restaurant is so healthy is because they are very strict on portioning their ingredients. This allows them to deliver a perfectly balanced taste with the minimum overhead in fat and sugar. They want us to model their standard mozzerella cheese portion, which we can do using the `portion` constructor:
<br>
```
import <http://www.ontology-of-units-of-measure.org/resource/om-2/> as om.

...

class Mozzerella ~= foodon:_03303578.
class StandardChessePortion ~= [123..127] om:gram portion Mozzerella.
```

We have imported the [Ontology of Units of Measure](https://github.com/HajoRijgersberg/OM), the most broad and consistent ontology of measurement available today, and use its concept of a gram to define our standard portion of cheese. The size of this portion is given using an (inclusive) range from 123 to 127g. This class will match any portion of mozzerella cheese that has an amount in that range.

This is the first major piece of syntactic sugar we have used. The `portion` constructor is shorthand for a much more complex (and tedious to write) set of ontological statements that (together) capture the meaning of being a measured portion of some substance (together known as the quantity ontology design pattern). This sugar is built on the concepts within the [Basic Formal Ontology 2](https://basic-formal-ontology.org/) and [Common Core Ontology](https://github.com/CommonCoreOntology/CommonCoreOntologies), which are used as the foundational upper ontologies for all knowledge bases written using Notation4.

The use of upper ontologies has long been considered best practice for knowledge engineers. In Notation4, their use is assumed and encouraged through the default *prelude* included in the language. This prelude (which may be turned off by adding without prelude after the ontology IRI) defines a series of shorthand keywords for common concepts from the upper ontologies. These keywords are there to make it easier to write logically consistent and composable knowledge bases without deep specialist skill. In fact, we have been using these keywords quietly without mentioning it: predicates like `title`, `status`, `version`, or `description`, and classes like `object` are defined using keywords in our prelude. A full list of the keywords defined in the standard prelude is available here.

Sometimes though, you'd like to expand the upper ontology with extra shorthand labels  (or override existing ones). We can do that by using a `keyword` declaration. Such declarations are out of scope for this tutorial, and you are referred to the language documentation for more information.

### Review

In this section, we have learnt:

* How to express an amount of a substance using the portion constructor;
* The importance of upper ontologies and why Notation4 makes strong assumptions about them;
* The existance of the prelude, and how to turn it off when desired; and
* That we can define new keywords for specific domains when needed.

## Nutritional information

The quantity ontology design pattern shows up in a few other ways within Notation4. The language provides a lot of syntactic sugar for this pattern specifically as it is one of the most complex (and error-prone) patterns to define. In this section, we will use some other sugar for this pattern that will allow us to consistently work with measurements (with conversions and ontological typechecking of dimensional errors available for free!).

One of the competency questions we are interested in is about nutrition, specifically nutritional information. Our next step is to define what this means so our users' fitness trackers can stay up-to-date even as the restaurant's customers find it impossible to resist their pizzas. Nutritional information is an example of a quantity. Quantities are qualities of things that have a particular metrological dimension and (sometimes, for numeric quantities) a preferred unit of measure (which may also have an acceptable range). The first quantity we will define is the concept of a food's overall energy content. This may be represented as kcals or kilojoules or any other unit that has dimension energy (although, measuring the energy content of food using electronvolts may be impractical).

```
quantity FoodEnergyContent 
  with dimension <http://www.ontology-of-units-of-measure.org/resource/om-2/energy-Dimension> 
  with property has_energy_content
.
```

Dimension is a fundamental concept in measurement: quantities can only be added or subtracted if they have the same dimension (and equations must have the same dimension on each side). This concept underlies dimensional analysis, a powerful tool for discovering scientific laws, but is more prosaically useful in allowing sanity checking of calculations and facilitating automatic unit conversions.

In the above declaration, we also provide an (optional) instruction to define a property to relate things to this quantity. This may be useful when we want to use our quantities to describe classes.

For now, lets add some more quantities for the other standard nutritional data that food labels tend to focus on:
<br>
```
quantity FatContent with unit [0 ..) om:gram with property has_fat_content.

quantity ProteinContent with unit [0 ..) om:gram with property has_protein_content.

quantity CarbohydrateContent with unit [0 ..) om:gram with property has_carbohydrate_content.

quantity FibreContent with unit [0 ..) om:gram with property has_fibre_content.

quantity SodiumContent with unit [0 ..) om:gram with property has_sodium_content.
```

In these cases, we have chosen to define them using a preferred unit rather than dimension. This lets us place restrictions on the range of values this quantity may take (here, that they're all non-negative).

With these in hand, we can describe a category of especially healthy pizzas:
<br>
```
property has_ingredient ~= foodon:_00002420.

class SuperLeanPizza ~= Pizza 
  that 
      quantity FoodEnergyContent measuring [.. 1000] om:kilocalorie
  and quantity CarbohydrateContent of has_ingredient measuring [.. 180] om:gram total
  and quantity FatContent of has_ingredient measuring [.. 30] om:gram total.
```

Whew. That's a lot of new syntax. We might need a couple of these delicious-yet-healthy pizzas after we've gone through it. Let's break it down.

The `measuring` constructor allows us to easily assert restrictions on the values of quantities. The statement '*property* measuring *range* *unit*' matches any individual where the quantity value of that property (remember the quantity pattern) when converted to that unit lies in the given range. This makes it easy to express the semantics of measurement without the ten or so separate components that would be required to do it 'natively'.

The (optional) extra `total` at the end of two of the measuring constructors is called a *value aggregation function*. It says that the reasoner should take the set of all values that are described by the property and add them all together before comparing to the range. There are a handful of these functions defined in Notation4:

* `total`: add all the values together
* `maximum`: take the largest value
* `minimum`: take the smallest value
* `average`: take the arithmetic mean of the values

We are not limited to simple properties however. This constructor (and all constructors that take properties, such as `only`, `a`, `max`, and `min`) allowsyou to specify a *property expression*: a chain of properties separated by the keyword `of`. The chain is traversed from right to left (like the common English reading of the phrase) and the constructor works on whatever is reached after those traversals.

Property expressions are powerful, and can be used to define more complex properties much like class expressions can be used to define complex classes. There are more ways to construct property expressions than just chains. You can use inverses (which says to traverse the expression component from object to subject instead of subject to object), conjunction, disjunction, and more. In this case, we're using a special piece of syntactic sugar `quantity` for referencing whatever property is created for a quantity (either the default one, or a manually declared one).

### Exercises

* Add quantities for some micronutrients (such as iron) with the appropriate units
* Define a class for vitamins and some quantities for different kinds of vitamins with the appropriate units
* Define a class for a particular diet that is rich in, say, iron

### Review

In this section, we have learnt:

* About the quantity pattern, and how it is supported in Notation4;
* Ways of expressing measurable quantities so that we gain automatic unit conversion and dimensional consistency can be checked;
* How we can use the values of quantities to define classes through the measuring class expression constructor;
* About property expressions and the ways we can build complex traversals over a knowledge base when working with classes and properties;
* The use of value aggregation functions to apply calculations across all values for a property expression; and
* How we can use the quantity property expression constructor to reference a quantity without manually tracking the associated property.

## Product safety

As a quick aside, now we know about property expressions we can express some knowledge about product safety. We will begin by amending our declaration of `has_ingredient`:
<br>
```
transitive property has_ingredient ~= foodon:_00002420.
```

The `transitive` modifer on the property says that whenever we see three entities related by a chain of `has_ingredient` predicates, we can treat the first and last in the chain as also being related by a `has_ingredient` predicate. The following modifiers are available:

* `transitive`: if `p` is transitive and we have `a p b` and `b p c`, then we have `a p c`
* `functional`: if `p` is functional and we have `a p b` and `a p c`, then `b` must refer to the same thing as `c`
* `inversefunctional`: if `p` is inverse functional and we have `a p b` and `c p b`, then `a` must refer to the same thing as `c`
* `symmetric`: if `p` is symmetric and `a p b`, then `b p a`
* `asymmetric`: if `p` is asymmetric and `a p b`, then we cannot also have `b p a`
* `reflexive`: if `p` is reflexive and `a p b`, then we must also have `a p a`
* `irreflexive`: if `p` is irreflexive and `a p b`, then we cannot also have `a p a`

These modifiers could be expressed in other, more cumbersome ways, but the syntactic sugar is provided to make them easier to use.

With that definition of `has_ingredient`, we can now state an important product safety principle:
<br>
```
property causes_allergic_reaction of has_ingredient <| causes_allergic_reaction.
```

That is, any allergic reaction caused by an ingredient is an allergic reaction of the thing with that ingredient. This sort of declaration is called a property chain axiom, and is a simple (and efficient) way of stating basic rules about the world.

### Exercises

* The above rule for allergic reactions isn't quite enough to capture our product safety requirement. Define an additional rule to state that if a pizza derives from (ro:\_0001000) another food and that food causes an allergic reaction then the pizza also causes the allergic reaction

### Review

In this aside, we have learnt:

* That property declarations can take modifiers that provide a shorthand for asserting particular properties; and
* That property declarations don't have to declare a simple QName, but can declare complex property expressions.

## On the menu

Describing individual pizzas, available sizes.
<br>
## The real Italian

Values (is constructor), nominals, and referencing individuals from a vocabulary.

## Processed food

Representing processes, production.

## Order for table 1

Modal logic and terms and conditions using DActs and OCE.

## On time, you're full

Delivery times, introduction to rules, headed lists, functional definitions.

## Cosmopolitan crowds

Internationalization.

## Chatty customers

Lexicons and possible NLP techniques over ontologies and knowledge bases.

## Conclusion

What we've learnt. Applications (such as to COVID-19 food security). Built-in testing framework. Other resources.