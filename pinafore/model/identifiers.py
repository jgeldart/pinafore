'''
pinafore/model/identifiers.py

Model classes for things that stand for URIs.
'''

from pinafore.model.base import Resource

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

MODEL_CLASSES = [
  CURIE,
  ExplicitIRI,
  Keyword
]
