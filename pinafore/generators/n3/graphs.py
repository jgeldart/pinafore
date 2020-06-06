from rdflib import URIRef, BNode
from .base import Clause


class GraphDecl(Clause):

    # def resource_reference(self):
    #     if hasattr(self, "name") and self.name is not None:
    #         return URIRef(self.full_iri)
    #     else:
    #         return BNode()

    # def clause(self):
    #     return ""

    def is_context(self):
        return True


MODELS = [
    GraphDecl
]
