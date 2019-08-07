
from tests.utils import notation4_parse, nt_parse

def test_single_statement():
  assert notation4_parse('examples/model_statements_subject/single_statement.n4') == nt_parse('examples/model_statements_subject/single_statement.nt')

def test_multi_object_statement():
  assert notation4_parse('examples/model_statements_subject/multi_object.n4') == nt_parse('examples/model_statements_subject/multi_object.nt')

def test_multi_predicate_statement():
  assert notation4_parse('examples/model_statements_subject/multi_predicate.n4') == nt_parse('examples/model_statements_subject/multi_predicate.nt')