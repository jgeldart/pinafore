from .base import Clause


class AttributeDecl(Clause):

    def clause(self):
        return """
        ${this} a owl:DatatypeProperty;
            rdfs:isDefinedBy ${ontology}.
        """


class AttributeAxiomSpecializes(Clause):

    def clause(self):
        return """
        ${parent} rdfs:subPropertyOf ${expression}.
        """


class AttributeAxiomEquivalence(Clause):

    def clause(self):
        return """
        ${parent} owl:equivalentProperty ${expression}.
        """


class AttributeAxiomInstanceOf(Clause):

    def clause(self):
        return """
        ${parent} a ${expression}.
        """


MODELS = [
    AttributeDecl,
    AttributeAxiomSpecializes,
    AttributeAxiomEquivalence,
    AttributeAxiomInstanceOf
]
