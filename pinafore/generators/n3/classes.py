from .base import Clause


class ClassDecl(Clause):

    def clause(self):
        return """
        ${this} a owl:Class;
            rdfs:isDefinedBy ${ontology}.
        """


class ClassAxiomSpecializes(Clause):

    def clause(self):
        return """
        ${parent} rdfs:subClassOf ${expression}.
        """


class ClassAxiomEquivalence(Clause):

    def clause(self):
        return """
        ${parent} owl:equivalentClass ${expression}.
        """


class ClassAxiomInstanceOf(Clause):

    def clause(self):
        return """
        ${parent} a ${expression}.
        """


MODELS = [
    ClassDecl,
    ClassAxiomSpecializes,
    ClassAxiomEquivalence,
    ClassAxiomInstanceOf,
]
