from rdflib import BNode
from .base import Clause


class BNodeDecl(Clause):

    # def resource_reference(self):
    #     if hasattr(self, "name") and self.name is not None:
    #         return BNode(self.name)
    #     else:
    #         return BNode()

    def clause(self):
        return ""


MODELS = [
    BNodeDecl
]
