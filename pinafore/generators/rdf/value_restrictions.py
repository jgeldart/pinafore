from .base import Clause


class NominalPropertyRestriction(Clause):

    def resource_reference(self, is_anonymous=False, file_hash=None):
        return None

    def clause(self):
        if not self.is_local:
            return """
            ${class_decl} rdfs:subClassOf [
                a owl:Restriction;
                owl:onProperty ${expression};
                owl:someValuesFrom ${this['binding']}
            ].

            ${this['binding']} a owl:ObjectVariable;
                owl:variableId "${this}".

            ${this} a owl:ObjectVariable;
                owl:variableId "${this}".
            """
        else:
            return """
            ${this['binding']} a owl:ObjectVariable;
                owl:variableId "${this}".

            ${this} a owl:ObjectVariable;
                owl:variableId "${this}".
            """


MODELS = [
    NominalPropertyRestriction,
]
