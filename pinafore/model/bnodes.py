import rdflib
from pinafore.model.base import Resource, TripleSource

class BNodeStatement(TripleSource):

  @property
  def triples(self):
    subject = self.subject
    subject_ref = subject.reference

    for predicate in subject.predicates:
      predicate_ref = predicate.predicate.reference
      
      for obj in predicate.objects:
        yield (subject_ref, predicate_ref, obj.reference)

class BNode(Resource):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)

    self._bnode = None

  @property
  def reference(self):
    if self._bnode is not None:
      return self._bnode
    else:
      self._bnode = rdflib.BNode()
      return self._bnode

MODEL_CLASSES = [
  BNodeStatement,
  BNode
]