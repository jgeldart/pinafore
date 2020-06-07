from .base import Clause


class ClassExpressionDisjunction(Clause):

    def clause(self):
        return """
        ${this} a owl:Class;
            owl:unionOf (
                % for d in disjuncts:
                ${d}
                % endfor
                )
        .
        """


class ClassExpressionConjunction(Clause):

    def clause(self):
        return """
        ${this} a owl:Class;
            owl:intersectionOf (
                % for c in conjuncts:
                ${c}
                % endfor
                )
        .
        """


class ClassExpressionBase(Clause):

    def clause(self):
        return """
        ${this} a owl:Class;
            owl:intersectionOf (
                ${base_class}
                ${restriction}
                )
        .
        """


class ClassExpressionComplement(Clause):

    def clause(self):
        return """
        ${this} owl:complementOf ${expression}.
        """


class ClassExpressionEnumeration(Clause):

    def clause(self):
        return """
        ${this} a owl:Class;
            owl:oneOf (
                % for e in elements:
                ${e}
                % endfor
            ).
        """


class ClassExpressionAttributeMaxCard(Clause):

    def clause(self):
        return """
        ${this} a owl:Restriction;
            owl:maxQualifiedCardinality "${cardinality_raw}"^^xsd:integer;
            owl:onDataRange ${restriction};
            owl:onProperty ${role}.
        """


class ClassExpressionAttributeMinCard(Clause):

    def clause(self):
        return """
        ${this} a owl:Restriction;
            owl:minQualifiedCardinality "${cardinality_raw}"^^xsd:integer;
            owl:onDataRange ${restriction};
            owl:onProperty ${role}.
        """


class ClassExpressionAttributeExactCard(Clause):

    def clause(self):
        return """
        ${this} a owl:Restriction;
            owl:qualifiedCardinality "${cardinality_raw}"^^xsd:integer;
            owl:onDataRange ${restriction};
            owl:onProperty ${role}.
        """


class ClassExpressionPropertyMaxCard(Clause):

    def clause(self):
        return """
        ${this} a owl:Restriction;
            owl:maxQualifiedCardinality "${cardinality_raw}"^^xsd:integer;
            owl:onClass ${restriction};
            owl:onProperty ${role}.
        """


class ClassExpressionPropertyMinCard(Clause):

    def clause(self):
        return """
        ${this} a owl:Restriction;
            owl:minQualifiedCardinality "${cardinality_raw}"^^xsd:integer;
            owl:onClass ${restriction};
            owl:onProperty ${role}.
        """


class ClassExpressionPropertyExactCard(Clause):

    def clause(self):
        return """
        ${this} a owl:Restriction;
            owl:qualifiedCardinality "${cardinality_raw}"^^xsd:integer;
            owl:onClass ${restriction};
            owl:onProperty ${role}.
        """


class ClassExpressionAttributeOnlySome(Clause):

    def clause(self):
        return """
        ${this} a owl:Class;
            owl:intersectionOf (${this['only']} ${this['some']}).

        ${this['only']} a owl:Restriction;
            owl:allValuesFrom ${restriction};
            owl:onProperty ${role}.

        ${this['some']} a owl:Restriction;
            owl:someValuesFrom ${restriction};
            owl:onProperty ${role}.
        """


class ClassExpressionAttributeOnly(Clause):

    def clause(self):
        return """
        ${this} a owl:Restriction;
            owl:allValuesFrom ${restriction};
            owl:onProperty ${role}.
        """


class ClassExpressionAttributeSome(Clause):

    def clause(self):
        return """
        ${this} a owl:Restriction;
            owl:someValuesFrom ${restriction};
            owl:onProperty ${role}.
        """


class ClassExpressionPropertyOnlySome(Clause):

    def clause(self):
        return """
        ${this} a owl:Class;
            owl:intersectionOf (${this['only']} ${this['some']}).

        ${this['only']} a owl:Restriction;
            owl:allValuesFrom ${restriction};
            owl:onProperty ${role}.

        ${this['some']} a owl:Restriction;
            owl:someValuesFrom ${restriction};
            owl:onProperty ${role}.
        """


class ClassExpressionPropertyOnly(Clause):

    def clause(self):
        return """
        ${this} a owl:Restriction;
            owl:allValuesFrom ${restriction};
            owl:onProperty ${role}.
        """


class ClassExpressionPropertySome(Clause):

    def clause(self):
        return """
        ${this} a owl:Restriction;
            owl:someValuesFrom ${restriction};
            owl:onProperty ${role}.
        """


class ClassExpressionAttributeValue(Clause):

    def clause(self):
        return """
        ${this} a owl:Restriction;
            owl:hasValue ${restriction};
            owl:onProperty ${role}.
        """


class ClassExpressionPropertyValue(Clause):

    def clause(self):
        return """
        ${this} a owl:Restriction;
            owl:hasValue ${restriction};
            owl:onProperty ${role}.
        """


class ClassExpressionSelf(Clause):

    def clause(self):
        return """
        ${this} a owl:Restriction;
            owl:hasSelf "true"^^xsd:boolean;
            owl:onProperty ${role}.
        """


MODELS = [
    ClassExpressionDisjunction,
    ClassExpressionConjunction,
    ClassExpressionBase,
    ClassExpressionComplement,
    ClassExpressionEnumeration,
    ClassExpressionAttributeMaxCard,
    ClassExpressionAttributeMinCard,
    ClassExpressionAttributeExactCard,
    ClassExpressionAttributeOnlySome,
    ClassExpressionAttributeOnly,
    ClassExpressionAttributeSome,
    ClassExpressionAttributeValue,
    ClassExpressionPropertyMaxCard,
    ClassExpressionPropertyMinCard,
    ClassExpressionPropertyExactCard,
    ClassExpressionPropertyOnlySome,
    ClassExpressionPropertyOnly,
    ClassExpressionPropertySome,
    ClassExpressionPropertyValue,
    ClassExpressionSelf,
]
