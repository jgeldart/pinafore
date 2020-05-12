from rdflib import BNode
from rdflib.namespace import RDF
from pinafore.model.base import Resource, TripleSource

class List(Resource, TripleSource):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)

    self._listBNodes = None

  @property
  def reference(self):
    if len(self.members) == 0:
      return RDF.nil
    elif self._listBNodes is not None:
      return self._listBNodes[0]
    else:
      self._listBNodes = [BNode() for _ in range(len(self.members))]
      return self._listBNodes[0]

  @property
  def triples(self):
    if len(self.members) > 0:
      last_member = len(self.members)
      for i in range(last_member):
        if i == 0:
          current_list_node = self._listBNodes[i]
          current_member = self.members[i]
          yield (self.reference, RDF.type, RDF.List)
          yield (current_list_node, RDF.first, current_member.reference)
          if i == last_member - 1:
            yield (current_list_node, RDF.rest, RDF.nil)
        elif i < last_member:
          last_list_node = self._listBNodes[i-1]
          current_list_node = self._listBNodes[i]
          current_member = self.members[i]

          yield (last_list_node, RDF.rest, current_list_node)
          yield (current_list_node, RDF.type, RDF.List)
          yield (current_list_node, RDF.first, current_member.reference)
          if hasattr(current_member, 'triples'):
            for t in current_member.triples:
              yield t

          if i == last_member - 1:
            yield (current_list_node, RDF.rest, RDF.nil)
        


MODEL_CLASSES = [
  List
]