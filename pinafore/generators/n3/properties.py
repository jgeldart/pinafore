from .base import Clause


class PropertyDecl(Clause):

    def clause(self):
        return """
        ${this} a owl:ObjectProperty;
            rdfs:isDefinedBy ${ontology}.
        """


MODELS = [
    PropertyDecl
]
