'''
pinafore/model/statements.py

Model classes for statements.
'''

from pinafore.model.base import Node, TripleSource

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

    if hasattr(self.subject, 'triples'):
      for t in self.subject.triples:
        yield t

    for predicate_block in self.predicates:
      predicate_reference = predicate_block.predicate.reference
      
      for obj in predicate_block.objects:
        obj_reference = obj.reference

        if hasattr(obj, 'triples'):
          for t in obj.triples:
            yield t

        yield (subject_reference, predicate_reference, obj_reference)

class PredicateBlock(Node):
  pass

MODEL_CLASSES = [
  Declaration,
  SubjectStatement,
  PredicateBlock
]
