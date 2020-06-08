from rdflib import Literal as L
from .base import Resource


class Literal(Resource):

    def resource_reference(self, **kwargs):
        return L(self.literal.value)


MODELS = [
    Literal
]
