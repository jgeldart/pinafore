from .base import Clause


class PropertyExpression(Clause):

    def resource_reference(self):
        if self.left_plural is None and self.right_plural is None:
            if self.expression.__class__.__name__ == "PropertyRef":
                return self.expression.ref.resource_reference()
            else:
                return super().resource_reference()
        else:
            return super().resource_reference()

    def clause(self):
        return """
        """


MODELS = [
    PropertyExpression,
]
