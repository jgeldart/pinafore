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
        if hasattr(obj, 'triples'):
          for t in obj.triples:
            yield t
            
        yield (subject_ref, predicate_ref, obj.reference)

class BNode(Resource, TripleSource):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)

    self._bnode = None

  @property
  def triples(self):
    subject_ref = self.reference

    for predicate in self.predicates:
      predicate_ref = predicate.predicate.reference

      for obj in predicate.objects:
        if hasattr(obj, 'triples'):
          for t in obj.triples:
            yield t
        yield (subject_ref, predicate_ref, obj.reference)

  @property
  def reference(self):
    if self._bnode is not None:
      return self._bnode
    else:
      if self.identifier is not None:
        return self.identifier.reference
      else:
        self._bnode = rdflib.BNode()
        return self._bnode

MODEL_CLASSES = [
  BNodeStatement,
  BNode
]