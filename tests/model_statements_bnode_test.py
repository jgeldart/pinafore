from tests.utils import n4_parse, nt_parse, ttl_parse

def test_empty_bnode():
  n4_graph = n4_parse('examples/model_statements_bnode/empty_bnode.n4')
  expected_graph = ttl_parse('examples/model_statements_bnode/empty_bnode.ttl')
  assert n4_graph == expected_graph

def test_bnode_statement():
  n4_graph = n4_parse('examples/model_statements_bnode/bnode_statement.n4')
  expected_graph = ttl_parse('examples/model_statements_bnode/bnode_statement.ttl')
  assert n4_graph == expected_graph

def test_bnode_with_identifier():
  assert False

def test_nested_bnode():
  assert False
