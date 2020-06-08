from .base import Clause


class PropertyDecl(Clause):

    def clause(self):
        return """
        ${this} a owl:ObjectProperty;
            rdfs:isDefinedBy ${ontology}.
        """


class PropertyAxiomSpecializes(Clause):

    def clause(self):
        return """
        ${parent} rdfs:subPropertyOf ${expression}.
        """


class PropertyAxiomEquivalence(Clause):

    def clause(self):
        return """
        ${parent} owl:equivalentProperty ${expression}.
        """


class PropertyAxiomInstanceOf(Clause):

    def clause(self):
        return """
        ${parent} a ${expression}.
        """


MODELS = [
    PropertyDecl,
    PropertyAxiomSpecializes,
    PropertyAxiomEquivalence,
    PropertyAxiomInstanceOf,
]
