from .base import Clause, BNodeReference


class DataExpressionDisjunction(Clause):

    def clause(self):
        return """
        ${this} a rdfs:Datatype;
            owl:unionOf (
                % for d in disjuncts:
                ${d}
                % endfor
            ).
        """


class DataExpressionConjunction(Clause):

    def clause(self):
        return """
        ${this} a rdfs:Datatype;
            owl:intersectionOf (
                % for c in conjuncts:
                ${c}
                % endfor
            ).
        """


class DataExpressionComplement(Clause):

    def clause(self):
        return """
        ${this} a rdfs:Datatype;
            owl:datatypeComplementOf ${expression}.
        """


class DataFacetGTE(Clause):

    def resource_reference(self, **kwargs):
        return None

    def clause(self):
        return """
        ${this} a rdfs:Datatype;
            owl:withRestrictions ([
                xsd:minInclusive ${value}
                ]).
        """


class DataFacetGT(Clause):

    def resource_reference(self, **kwargs):
        return None

    def clause(self):
        return """
        ${this} a rdfs:Datatype;
            owl:withRestrictions ([
                xsd:minExclusive ${value}
                ]).
        """


class DataFacetLTE(Clause):

    def resource_reference(self, **kwargs):
        return None

    def clause(self):
        return """
        ${this} a rdfs:Datatype;
            owl:withRestrictions ([
                xsd:maxInclusive ${value}
                ]).
        """


class DataFacetLT(Clause):

    def resource_reference(self, **kwargs):
        return None

    def clause(self):
        return """
        ${this} a rdfs:Datatype;
            owl:withRestrictions ([
                xsd:maxExclusive ${value}
                ]).
        """


class DataFacetMinLength(Clause):

    def resource_reference(self, **kwargs):
        return None

    def clause(self):
        return """
        ${this} a rdfs:Datatype;
            owl:withRestrictions ([
                xsd:minLength "${value_raw}"^^xsd:integer
                ]).
        """


class DataFacetMaxLength(Clause):

    def resource_reference(self, **kwargs):
        return None

    def clause(self):
        return """
        ${this} a rdfs:Datatype;
            owl:withRestrictions ([
                xsd:maxLength "${value_raw}"^^xsd:integer
                ]).
        """


class DataFacetLength(Clause):

    def resource_reference(self, **kwargs):
        return None

    def clause(self):
        return """
        ${this} a rdfs:Datatype;
            owl:withRestrictions ([
                xsd:length "${value_raw}"^^xsd:integer
                ]).
        """


class DataFacetMatches(Clause):

    def resource_reference(self, **kwargs):
        return None

    def clause(self):
        return """
        ${this} a rdfs:Datatype;
            owl:withRestrictions ([
                xsd:pattern "${value_raw.value[1:-1]}"
                ]).
        """


MODELS = [
    DataExpressionDisjunction,
    DataExpressionConjunction,
    DataExpressionComplement,
    DataFacetGTE,
    DataFacetGT,
    DataFacetLTE,
    DataFacetLT,
    DataFacetMinLength,
    DataFacetMaxLength,
    DataFacetLength,
    DataFacetMatches,
]
