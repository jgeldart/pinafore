'''
pinafore/model/base.py

Base classes for use by other models
'''

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
