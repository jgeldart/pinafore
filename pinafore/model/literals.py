'''
pinafore/model/literals.py

Model classes for literals and literal expressions.
'''
from rdflib.namespace import XSD
import rdflib

from pinafore.model.base import Resource

class Literal(Resource):

  @property
  def reference(self):
    literal_datatype = None
    literal_lang = None
    literal_value = None
    if self.dtlang is not None:
      if self.dtlang.dtype is not None:
        literal_datatype = self.dtlang.dtype.reference
        literal_value = self.literal.value
      elif self.dtlang.language is not None:
        literal_datatype = XSD.string
        literal_lang = self.dtlang.language
        literal_value = self.literal.value
    else:
      if isinstance(self.literal, DecimalExpression):
        literal_datatype = XSD.decimal
        literal_value = self.literal.value
      elif isinstance(self.literal, IntegerExpression):
        literal_datatype = XSD.integer
        literal_value = self.literal.value
      elif isinstance(self.literal, RationalExpression):
        literal_datatype = XSD.rational
        literal_value = '{0}/{1}'.format(self.literal.numerator, self.literal.denominator)
      elif isinstance(self.literal, DateExpression):
        literal_datatype = XSD.date
        literal_value = self.literal.value
      elif isinstance(self.literal, TimeExpression):
        literal_datatype = XSD.time
        literal_value = self.literal.value
      elif isinstance(self.literal, DateTimeExpression):
        literal_datatype = XSD.dateTime
        literal_value = self.literal.value
      elif isinstance(self.literal, DurationExpression):
        literal_datatype = XSD.duration
        literal_value = self.literal.value
      elif isinstance(self.literal, BooleanExpression):
        literal_datatype = XSD.boolean
        literal_value = self.literal.value
      else:
        literal_datatype = XSD.string
        literal_value = self.literal.value

    if literal_lang is not None:
      return rdflib.Literal(literal_value, lang=literal_lang)
    else:
      return rdflib.Literal(literal_value, datatype=literal_datatype)

class DTLang(Resource):
  pass

class DecimalExpression(Resource):
  pass

class RationalExpression(Resource):
  pass

class IntegerExpression(Resource):
  pass

class DateExpression(Resource):
  pass

class TimeExpression(Resource):
  pass

class DateTimeExpression(Resource):
  pass

class DurationExpression(Resource):
  pass

class BooleanExpression(Resource):
  pass

class StringExpression(Resource):
  pass

MODEL_CLASSES = [
  Literal,
  DTLang,
  DecimalExpression,
  RationalExpression,
  IntegerExpression,
  DateExpression,
  TimeExpression,
  DateTimeExpression,
  DurationExpression,
  BooleanExpression,
  StringExpression
]
