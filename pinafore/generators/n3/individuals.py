from rdflib import URIRef
from .base import Clause


class IndividualDecl(Clause):

    # def resource_reference(self):
    #     if hasattr(self, "subject") and self.subject is not None:
    #         return self.subject.resource()
    #     else:
    #         return URIRef(self.full_iri)

    def clause(self):
        return """
        ${this} a owl:NamedIndividual;
            rdfs:isDefinedBy ${ontology}.
        """


class IndividualAxiomInstanceOf(Clause):

    def resource_reference(self):
        return None

    def clause(self):
        return """
        ${parent} a ${expression}.
        """


MODELS = [
    IndividualDecl,
    IndividualAxiomInstanceOf
]
