'''
pinafore/model/document.py

Model for a Notation4 document, providing a root for interpretation.
'''

from pinafore.model.base import TripleSource 
from pinafore.model.prolog import Prolog

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

MODEL_CLASSES = [
  Document
]
