from .base import Clause, Resource


class PropertyExpression(Clause):

    def resource_reference(self, **kwargs):
        if self.left_plural is None and self.right_plural is None:
            if self.expression.__class__.__name__ == "PropertyRef":
                return self.expression.ref.resource_reference(**kwargs)
            else:
                return super().resource_reference(**kwargs)
        else:
            return super().resource_reference(**kwargs)

    def clause(self):
        left_plural = self.left_plural
        right_plural = self.right_plural
        if left_plural is not None:
            if left_plural.__class__.__name__ == "PluralCumulative":
                return """
                ${this} a owl:ObjectProperty;
                    mel:cumulativeSubjectOver ${expression}.
                """
            if left_plural.__class__.__name__ == "PluralDistributive":
                return """
                ${this} a owl:ObjectProperty;
                    mel:distributiveSubjectOver ${expression}.
                """
        if right_plural is not None:
            if right_plural.__class__.__name__ == "PluralCumulative":
                return """
                ${this} a owl:ObjectProperty;
                    mel:cumulativeObjectOver ${expression}.
                """
            if right_plural.__class__.__name__ == "PluralDistributive":
                return """
                ${this} a owl:ObjectProperty;
                    mel:distributiveObjectOver ${expression}.
                """
        return ""


class PropertyExpressionDisjunction(Clause):

    def clause(self):
        return """
        ${this} a owl:ObjectProperty;
            mel:propertyUnionOf (
                % for d in disjuncts:
                ${d}
                % endfor
            ).
        """


class PropertyExpressionConjunction(Clause):

    def clause(self):
        return """
        ${this} a owl:ObjectProperty;
            mel:propertyIntersectionOf (
                % for c in conjuncts:
                ${c}
                % endfor
            ).
        """


class PropertyExpressionComplement(Clause):

    def clause(self):
        return """
        ${this} a owl:ObjectProperty;
            mel:propertyComplementOf ${expression}.
        """


class PropertyExpressionChain(Clause):

    def clause(self):
        return """
        ${this} a owl:ObjectProperty;
            mel:propertyChainOf (
                % for s in reversed(steps):
                ${s}
                % endfor
            ).
        """


class PropertyExpressionInverse(Clause):

    def clause(self):
        return """
        ${this} a owl:ObjectProperty;
            owl:inverseOf ${expression}.
        """


class PropertyExpressionProduct(Clause):

    def clause(self):
        return [
            "${this} a owl:ObjectProperty.",
            "${this} rdfs:domain ${domain}.",
            "${this} rdfs:range ${range}.",
        ]


class PropertyExpressionTop(Resource):

    def resource_reference(self, **kwargs):
        return "http://www.w3.org/2002/07/owl#topObjectProperty"


class PropertyExpressionBottom(Resource):

    def resource_reference(self, **kwargs):
        return "http://www.w3.org/2002/07/owl#bottomObjectProperty"


class QualifiedPropertyRef(Clause):

    def clause(self):
        return """
        ${this} a owl:ObjectProperty;
            mel:propertyChainOf (
                ${expression}
                ${qualification['isa']}
            ).
        """


MODELS = [
    PropertyExpression,
    PropertyExpressionDisjunction,
    PropertyExpressionConjunction,
    PropertyExpressionComplement,
    PropertyExpressionChain,
    PropertyExpressionTop,
    PropertyExpressionBottom,
    PropertyExpressionInverse,
    PropertyExpressionProduct,
    QualifiedPropertyRef,
]
