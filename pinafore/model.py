from rdflib import URIRef, Namespace
import rdflib
from rdflib.namespace import XSD

class Node(object):

  def __init__(self, **kwargs):
    for name, value in kwargs.items():
      setattr(self, name, value)

  @property
  def context(self):
    '''
    The context used to understand a set of resources and triples.
    '''
    if self.parent is not None:
      return self.parent.context

  def resolve_iri(self, iri):
    '''
    Resolve the IRI given relative to the document's base.
    '''
    return self.context.resolve_iri(iri)

  def resolve_curie(self, ns, qname):
    '''
    Resolve a CURIE based on the declared prefixes.
    '''
    return self.context.resolve_curie(ns, qname)

  def resolve_keyword(self, keyword):
    '''
    Resolve a defined keyword.
    '''
    return self.context.resolve_keyword(keyword)

class TripleSource(Node):
  '''
  A triple source is anything that can produce triples.
  '''

  @property
  def triples(self):
    '''
      Returns a generator that yields triples.
    '''
    raise NotImplementedError

class Resource(Node):
  '''
  A resource is anything that can be referred to in a statement.
  '''

  @property
  def reference(self):
    '''
      Returns an RDF term.
    '''
    raise NotImplementedError

class Document(TripleSource):

  @property
  def namespaces(self):
    if self.prolog is not None:
      return self.prolog.namespaces
    else:
      return {}

  @property
  def context(self):
    if self.prolog is not None:
      return self.prolog.context
    else:
      self.prolog = Prolog(pragmas=[])
      return self.prolog.context

  def set_base(self, iri):
    if self.prolog is not None:
      return self.prolog.set_base(iri)
    else:
      self.prolog = Prolog(pragmas=[])
      return self.prolog.set_base(iri)

  @property
  def triples(self):
    
    for declaration_triple in self.declaration.triples:
      yield declaration_triple

    for prolog_triple in self.prolog.triples:
      yield prolog_triple

class Prolog(TripleSource):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)

    self._base_iri = None
    self._namespaces = {}
    self._default_ns = None
    self._keywords = {}
    self._imports = []

    self._fetch_base()

    self._ns_fetched = False
    self._kw_fetched = False
    

  def resolve_iri(self, iri):
    return URIRef(iri, base=self._base_iri)

  def resolve_curie(self, ns, qname):
    self._fetch_namespaces()
    if ns is None and self._default_ns is None:
      if self._base_iri.endswith('/'):
        return self.resolve_iri('./{0}'.format(qname))
      else:
        return self.resolve_iri('#{0}'.format(qname))
    elif ns is None and self._default_ns is not None:
      return self._default_ns[qname]
    elif ns in self._namespaces.keys():
      return self._namespaces[ns][qname]
    else:
      return None

  def resolve_keyword(self, keyword):
    self._fetch_namespaces()
    self._fetch_keywords()
    if keyword in self._keywords.keys():
      return self._keywords[keyword]
    else:
      return None

  @property
  def triples(self):
    base = self.resolve_iri('')
    owl_imports = URIRef('http://www.w3.org/2002/07/owl#imports')
    for iri in self._imports:
      yield (base, owl_imports, iri)

  @property
  def context(self):
    return self

  @property
  def namespaces(self):
    '''
    Return the set of namespaces registered in this pragmas block
    '''
    return self._namespaces

  def _register_namespace(self, ns, iri, should_import=False):
    '''
    Register a namespace with the given prefix.
    '''
    if ns is not None:
      self._namespaces[ns] = Namespace(iri)
    else:
      self._default_ns = Namespace(iri)
    if should_import:
      self._imports.append(URIRef(iri))

  def set_base(self, iri):
    '''
    Set the document's base IRI
    '''
    if self._base_iri is None:
      self._base_iri = iri

  def _register_keyword(self, keyword, iri_term):

    if isinstance(iri_term, CURIE):
      iri = self.resolve_curie(iri_term.namespace, iri_term.qname)
    elif isinstance(iri_term, ExplicitIRI):
      iri = self.resolve_iri(iri_term.iri)
    else:
      iri = None

    if iri is not None:
      self._keywords[keyword] = URIRef(iri)

  def _fetch_base(self):
    for pragma in self.pragmas:
      if isinstance(pragma, BasePragma):
        self._base_iri = pragma.iri

  def _fetch_namespaces(self):
    if not self._ns_fetched:
      for pragma in self.pragmas:
        if isinstance(pragma, PrefixPragma):
          self._register_namespace(pragma.prefix, pragma.iri)
        elif isinstance(pragma, ImportPragma):
          self._register_namespace(pragma.prefix, pragma.iri, should_import=True)
      self._ns_fetched = True

  def _fetch_keywords(self):
    if not self._kw_fetched:
      for pragma in self.pragmas:
        if isinstance(pragma, KeywordPragma):
          self._register_keyword(pragma.shorthand, pragma.iri)
      self._kw_fetched = True

class BasePragma(Node):
  pass

class PrefixPragma(Node):
  pass

class ImportPragma(Node):
  pass

class KeywordPragma(Node):
  pass

class CURIE(Resource):
  
  @property
  def reference(self):
    return self.resolve_curie(self.namespace, self.qname)

class ExplicitIRI(Resource):
  
  @property
  def reference(self):
    return self.resolve_iri(self.iri)

class Keyword(Resource):

  @property
  def reference(self):
    return self.resolve_keyword(self.keyword)

class Declaration(TripleSource):

  @property
  def triples(self):
    for statement in self.statements:
      for triple in statement.triples:
        yield triple

class SubjectStatement(TripleSource):

  @property
  def triples(self):

    subject_reference = self.subject.reference

    for predicate_block in self.predicates:
      predicate_reference = predicate_block.predicate.reference
      
      for obj in predicate_block.objects:
        obj_reference = obj.reference

        yield (subject_reference, predicate_reference, obj_reference)

class PredicateBlock(Node):
  pass

class Literal(Resource):

  @property
  def reference(self):
    literal_datatype = None
    literal_lang = None
    literal_value = None
    if self.dtlang is not None:
      if self.dtlang.dtype is not None:
        literal_datatype = self.dtlang.dtype.reference
        literal_value = self.literal.value
      elif self.dtlang.language is not None:
        literal_datatype = XSD.string
        literal_lang = self.dtlang.language
        literal_value = self.literal.value
    else:
      if isinstance(self.literal, DecimalExpression):
        literal_datatype = XSD.float
        literal_value = self.literal.value
      elif isinstance(self.literal, IntegerExpression):
        literal_datatype = XSD.integer
        literal_value = self.literal.value
      elif isinstance(self.literal, RationalExpression):
        literal_datatype = XSD.rational
        literal_value = '{0}/{1}'.format(self.literal.numerator, self.literal.denominator)
      elif isinstance(self.literal, DateExpression):
        literal_datatype = XSD.date
        literal_value = self.literal.value
      elif isinstance(self.literal, TimeExpression):
        literal_datatype = XSD.time
        literal_value = self.literal.value
      elif isinstance(self.literal, DateTimeExpression):
        literal_datatype = XSD.dateTime
        literal_value = self.literal.value
      elif isinstance(self.literal, DurationExpression):
        literal_datatype = XSD.duration
        literal_value = self.literal.value
      elif isinstance(self.literal, BooleanExpression):
        literal_datatype = XSD.boolean
        literal_value = self.literal.value
      else:
        literal_datatype = XSD.string
        literal_value = self.literal.value

    if literal_lang is not None:
      return rdflib.Literal(literal_value, lang=literal_lang)
    else:
      return rdflib.Literal(literal_value, datatype=literal_datatype)

class DTLang(Resource):
  pass

class DecimalExpression(Resource):
  pass

class RationalExpression(Resource):
  pass

class IntegerExpression(Resource):
  pass

class DateExpression(Resource):
  pass

class TimeExpression(Resource):
  pass

class DateTimeExpression(Resource):
  pass

class DurationExpression(Resource):
  pass

class BooleanExpression(Resource):
  pass

class StringExpression(Resource):
  pass

MODEL_CLASSES = [
  Document,
  Prolog,
  BasePragma,
  PrefixPragma,
  ImportPragma,
  KeywordPragma,
  CURIE,
  ExplicitIRI,
  Keyword,
  Declaration,
  SubjectStatement,
  PredicateBlock,
  Literal,
  DTLang,
  DecimalExpression,
  RationalExpression,
  IntegerExpression,
  DateExpression,
  TimeExpression,
  DateTimeExpression,
  DurationExpression,
  BooleanExpression,
  StringExpression
]