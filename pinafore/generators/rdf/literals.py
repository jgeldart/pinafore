from rdflib import Literal as L
from rdflib.namespace import XSD
from textx import get_parent_of_type
from .base import Resource, Clause


class LiteralBase(Resource):

    def resource_reference(self, **kwargs):
        dtype = self.datatype()
        if hasattr(self, "parent") and self.parent is not None:
            if hasattr(self.parent, "dtlang") and self.parent.dtlang is not None:
                if hasattr(self.parent.dtlang, "data_type") and self.parent.dtlang.data_type is not None:
                    dtype = self.parent.dtlang.data_type.resource()

        lang = self.lang()
        if dtype == XSD.string and lang is not None:
            return L(self.literal_value(), lang=lang)
        else:
            return L(self.literal_value(), datatype=dtype)

    def datatype(self):
        return XSD.string

    def literal_value(self):
        return self.value

    def lang(self):
        return None


class IntegerExpression(LiteralBase):

    def datatype(self):
        return XSD.integer


class DecimalExpression(LiteralBase):

    def datatype(self):
        return XSD.decimal


class RationalExpression(LiteralBase):

    def datatype(self):
        return XSD.decimal

    def value(self):
        return 1.0 * self.numerator / self.denominator


class DateTimeExpression(LiteralBase):

    def datatype(self):
        return XSD.dateTime


class DurationExpression(LiteralBase):

    def datatype(self):
        return XSD.duration


class BooleanExpression(LiteralBase):

    def datatype(self):
        return XSD.boolean


class RegexExpression(LiteralBase):

    def datatype(self):
        return XSD.string

    def lang(self):
        return None


class StringExpression(LiteralBase):

    def datatype(self):
        return XSD.string

    def lang(self):
        language = None
        ontology = get_parent_of_type("OntologyDecl", self)
        if ontology.default_language != "":
            language = ontology.default_language
        if hasattr(self, "parent") and self.parent is not None:
            if hasattr(self.parent, "dtlang") and self.parent.dtlang is not None:
                if hasattr(self.parent.dtlang, "language") and self.parent.dtlang.language != "":
                    language = self.parent.dtlang.language
        return language


class RangeExpressionBase(Clause):

    def resource_reference(self, **kwargs):
        return None

    def clause(self):
        clauses = ["""${this} a mel:LiteralRange."""]
        if self.lowerOpen != "":
            clauses.append("""
                           ${this} mel:minExclusiveValue ${lower}.
                           """)
        elif self.lowerClosed != "":
            clauses.append("""
                           ${this} mel:minInclusiveValue ${lower}.
                           """)
        if self.higherOpen != "":
            clauses.append("""
                           ${this} mel:maxExclusiveValue ${higher}.
                           """)
        elif self.higherClosed != "":
            clauses.append("""
                           ${this} mel:maxInclusiveValue ${higher}.
                           """)
        return clauses


class RangeExpressionInteger(RangeExpressionBase):
    pass


class RangeExpressionDecimal(RangeExpressionBase):
    pass


class RangeExpressionRational(RangeExpressionBase):
    pass


class RangeExpressionDateTime(RangeExpressionBase):
    pass


MODELS = [
    DecimalExpression,
    IntegerExpression,
    RationalExpression,
    DateTimeExpression,
    DurationExpression,
    BooleanExpression,
    StringExpression,
    RegexExpression,
    RangeExpressionInteger,
    RangeExpressionDecimal,
    RangeExpressionRational,
    RangeExpressionDateTime,
]
