
from tests.utils import n4_parse, nt_parse

def test_single_statement():
  n4_graph = n4_parse('examples/model_statements_subject/single_statement.n4')
  expected_graph = nt_parse('examples/model_statements_subject/single_statement.nt')
  assert n4_graph == expected_graph 

def test_multi_object_statement():
  n4_graph = n4_parse('examples/model_statements_subject/multi_object.n4')
  expected_graph = nt_parse('examples/model_statements_subject/multi_object.nt')
  assert n4_graph == expected_graph

def test_multi_predicate_statement():
  n4_graph = n4_parse('examples/model_statements_subject/multi_predicate.n4')
  expected_graph = nt_parse('examples/model_statements_subject/multi_predicate.nt')
  assert n4_graph == expected_graph

def test_multi_subject():
  n4_graph = n4_parse('examples/model_statements_subject/multi_subject.n4')
  expected_graph = nt_parse('examples/model_statements_subject/multi_subject.nt')
  assert n4_graph == expected_graph

def test_multi_subject_no_full_stop():
  n4_graph = n4_parse('examples/model_statements_subject/multi_subject-no-full-stop.n4')
  expected_graph = nt_parse('examples/model_statements_subject/multi_subject.nt')
  assert n4_graph == expected_graph