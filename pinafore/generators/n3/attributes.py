from .base import Clause


class AttributeDecl(Clause):

    def clause(self):
        return """
        ${this} a owl:DatatypeProperty;
            rdfs:isDefinedBy ${ontology}.
        """


MODELS = [
    AttributeDecl,
]
