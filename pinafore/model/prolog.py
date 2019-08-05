'''
pinafore/model/prolog.py

Model classes to set up the pragmas used to interpret the rest of the document.
'''

from rdflib import URIRef, Namespace
from pinafore.model.base import Node, TripleSource
from pinafore.model.identifiers import CURIE, ExplicitIRI

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

MODEL_CLASSES = [
  Prolog,
  BasePragma,
  PrefixPragma,
  ImportPragma,
  KeywordPragma
]
