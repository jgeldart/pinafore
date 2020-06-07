from .base import Clause


class DatatypeDecl(Clause):

    def clause(self):
        return """
        ${this} a rdfs:Datatype;
            rdfs:isDefinedBy ${ontology}.
        """


class DatatypeAxiomSpecializes(Clause):

    def clause(self):
        return """
        ${parent} rdfs:subClassOf ${expression}.
        """


class DatatypeAxiomEquivalence(Clause):

    def clause(self):
        return """
        ${parent} owl:equivalentClass ${expression}.
        """


MODELS = [
    DatatypeDecl,
    DatatypeAxiomSpecializes,
    DatatypeAxiomEquivalence,
]
