from tests.utils import n4_parse, nt_parse, ttl_parse

def test_empty_list():
  n4_graph = n4_parse('examples/model_collections/empty_list.n4')
  expected_graph = ttl_parse('examples/model_collections/empty_list.ttl')
  assert n4_graph == expected_graph

def test_literal_list():
  n4_graph = n4_parse('examples/model_collections/literal_list.n4')
  expected_graph = ttl_parse('examples/model_collections/literal_list.ttl')
  assert n4_graph == expected_graph

def test_uri_list():
  assert False

def test_curie_list():
  assert False

def test_bnode_list():
  assert False

def test_nested_list():
  assert False

def test_mixed_list():
  assert False

def test_set():
  assert False

def test_seq():
  assert False

def test_bag():
  assert False

def test_alt():
  assert False