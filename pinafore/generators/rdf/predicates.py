from .base import Clause, Resource


class Predicate(Clause):

    def clause(self):
        return """
            % for o in objects:
            ${parent} ${property} ${o}.
            % endfor
        """


class LogicalEqualsPredicate(Resource):

    def resource_reference(self, **kwargs):
        return "http://www.w3.org/2000/10/swap/log#equalTo"


class LogicalNotEqualsPredicate(Resource):

    def resource_reference(self, **kwargs):
        return "http://www.w3.org/2000/10/swap/log#notEqualTo"


class NumericEqualsPredicate(Resource):

    def resource_reference(self, **kwargs):
        return "http://www.w3.org/2000/10/swap/math#equalTo"


class NumericNotEqualsPredicate(Resource):

    def resource_reference(self, **kwargs):
        return "http://www.w3.org/2000/10/swap/math#notEqualTo"


class NumericLessThanEqualsPredicate(Resource):

    def resource_reference(self, **kwargs):
        return "http://www.w3.org/2000/10/swap/math#notGreaterThan"


class NumericLessThanPredicate(Resource):

    def resource_reference(self, **kwargs):
        return "http://www.w3.org/2000/10/swap/math#lessThan"


class NumericGreaterThanEqualsPredicate(Resource):

    def resource_reference(self, **kwargs):
        return "http://www.w3.org/2000/10/swap/math#notLessThan"


class NumericGreaterThanPredicate(Resource):

    def resource_reference(self, **kwargs):
        return "http://www.w3.org/2000/10/swap/math#greaterThan"


class LogicalSemanticsPredicate(Resource):

    def resource_reference(self, **kwargs):
        return "http://www.w3.org/2000/10/swap/log#semantics"


class LogicalConclusionsPredicate(Resource):

    def resource_reference(self, **kwargs):
        return "http://www.w3.org/2000/10/swap/log#conclusion"


class LogicalIdenticalPredicate(Resource):

    def resource_reference(self, **kwargs):
        return "http://www.w3.org/2002/07/owl#sameAs"


class LogicalDifferentPredicate(Resource):

    def resource_reference(self, **kwargs):
        return "http://www.w3.org/2002/07/owl#differentFrom"


class CollectionInclusionPredicate(Resource):

    def resource_reference(self, **kwargs):
        return "http://www.w3.org/2000/10/swap/list#in"


MODELS = [
    Predicate,
    LogicalEqualsPredicate,
    LogicalNotEqualsPredicate,
    NumericEqualsPredicate,
    NumericNotEqualsPredicate,
    NumericLessThanEqualsPredicate,
    NumericLessThanPredicate,
    NumericGreaterThanEqualsPredicate,
    NumericGreaterThanPredicate,
    LogicalSemanticsPredicate,
    LogicalConclusionsPredicate,
    LogicalIdenticalPredicate,
    LogicalDifferentPredicate,
    CollectionInclusionPredicate,
]
