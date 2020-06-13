from uuid import uuid4
from textx import get_parent_of_type
from .base import Desugaring, is_a, has_a, replace, resolve


class GlobalNominalPropertyValueTransform(Desugaring):

    def match(self, element):
        return (is_a(element, "NominalPropertyRestriction")
                and has_a(element, "is_local", value=False)
                and is_a(element.parent, "ClassExpressionPropertyValue"))

    def bind(self, element):
        return resolve(element, {
            'role': 'parent.role',
            'nominal_path': 'expression',
        })

    def apply(self, element, bindings):
        nom_var = uuid4().hex
        nominal_variable = self.construct("NominalVariable",
                                          nominal_var="the '{}'".format(nom_var))
        axiom = get_parent_of_type("ClassAxiomSpecializes", element)
        if axiom is None:
            axiom = get_parent_of_type("ClassAxiomEquivalence", element)
            if axiom is None:
                return
        local_value = self.construct("ClassExpressionPropertySome",
                                     role=bindings["role"],
                                     restriction=nominal_variable)
        replace(element.parent, local_value)
        top_value = self.construct("ClassExpressionConjunction",
                                   conjuncts=[
                                       axiom.expression,
                                       self.construct("ClassExpressionPropertySome",
                                                      role=bindings["nominal_path"],
                                                      restriction=nominal_variable)
                                   ])
        replace(axiom.expression, top_value)


class LocalNominalPropertyValueTransform(Desugaring):
    """
    Desugar local nominal property expressions to standard nominal variables.
    """

    def match(self, element):
        return (is_a(element, "NominalPropertyRestriction")
                and has_a(element, "is_local", value=True)
                and is_a(element.parent, "ClassExpressionPropertyValue"))

    def bind(self, element):
        return resolve(element, {
            'role': 'parent.role',
            'nominal_path': 'expression',
        })

    def apply(self, element, bindings):
        nom_var = uuid4().hex
        nominal_variable = self.construct("NominalVariable",
                                          nominal_var="the '{}'".format(nom_var))
        value = self.construct("ClassExpressionConjunction",
                               conjuncts=[
                                   self.construct("ClassExpressionPropertySome",
                                                  role=bindings["role"],
                                                  restriction=nominal_variable),
                                   self.construct("ClassExpressionPropertySome",
                                                  role=bindings["nominal_path"],
                                                  restriction=nominal_variable)
                               ])
        replace(element.parent, value)
