from .base import Clause


class NominalVariable(Clause):

    def resource_reference(self, **kwargs):
        return None

    def clause(self):
        return """
        ${this} a owl:ObjectVariable;
            owl:variableId "${this}".
        """


MODELS = [
    NominalVariable,
]
