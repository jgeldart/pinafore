from .base import Clause, Resource


class AttributeExpression(Clause):

    def resource_reference(self, **kwargs):
        if self.left_plural is None:
            if self.expression.__class__.__name__ == "AttributeRef" and self.property is None:
                return self.expression.ref.resource_reference(**kwargs)
            else:
                return super().resource_reference(**kwargs)
        else:
            return super().resource_reference(**kwargs)

    def clause(self):
        clauses = ""
        left_plural = self.left_plural
        if self.property is not None:
            if left_plural is None:
                clauses = """
                            ${this} a owl:DatatypeProperty;
                                mel:propertyChainOf (${property} ${expression}).
                          """
            else:
                if left_plural.__class__.__name__ == "PluralCumulative":
                    clauses = """
                                ${this['propchain']} a owl:DatatypeProperty;
                                  mel:propertyChainOf (${property} ${expression}).
                                ${this} a owl:DatatypeProperty;
                                  mel:cumulativeSubjectOver ${this['propchain']}.
                              """
                if left_plural.__class__.__name__ == "PluralDistributive":
                    clauses = """
                                ${this['propchain']} a owl:DatatypeProperty;
                                  mel:propertyChainOf (${property} ${expression}).
                                ${this} a owl:DatatypeProperty;
                                  mel:distributiveSubjectOver ${this['propchain']}.
                              """
        else:
            if left_plural is not None:
                if left_plural.__class__.__name__ == "PluralCumulative":
                    clauses = """
                                ${this} a owl:DatatypeProperty;
                                  mel:cumulativeSubjectOver ${expression}.
                              """
                if left_plural.__class__.__name__ == "PluralDistributive":
                    clauses = """
                                ${this} a owl:DatatypeProperty;
                                  mel:distributiveSubjectOver ${expression}.
                              """
        return clauses


class AttributeExpressionDisjunction(Clause):

    def clause(self):
        return """
        ${this} a owl:DatatypeProperty;
            mel:propertyUnionOf (
                % for d in disjuncts:
                ${d}
                % endfor
            ).
        """


class AttributeExpressionConjunction(Clause):

    def clause(self):
        return """
        ${this} a owl:DatatypeProperty;
            mel:propertyIntersectionOf (
                % for c in conjuncts:
                ${c}
                % endfor
            ).
        """


class AttributeExpressionComplement(Clause):

    def clause(self):
        return """
        ${this} a owl:DatatypeProperty;
            mel:propertyComplementOf ${expression}.
        """


class AttributeExpressionProduct(Clause):

    def clause(self):
        return [
            "${this} a owl:DatatypeProperty.",
            "${this} rdfs:domain ${domain}.",
            "${this} rdfs:range ${range}.",
        ]


class AttributeExpressionTop(Resource):

    def resource_reference(self, **kwargs):
        return "http://www.w3.org/2002/07/owl#topDataProperty"


class AttributeExpressionBottom(Resource):

    def resource_reference(self, **kwargs):
        return "http://www.w3.org/2002/07/owl#bottomDataProperty"


MODELS = [
    AttributeExpression,
    AttributeExpressionDisjunction,
    AttributeExpressionConjunction,
    AttributeExpressionComplement,
    AttributeExpressionTop,
    AttributeExpressionBottom,
    AttributeExpressionProduct,
]
