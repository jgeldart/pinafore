from tests.utils import n4_parse, nt_parse

def test_base_iri():
  n4_graph = n4_parse('examples/model_prolog/base.n4')
  expected_graph = nt_parse('examples/model_prolog/base.nt')
  assert n4_graph == expected_graph

def test_prefix_simple():
  n4_graph = n4_parse('examples/model_prolog/prefix-simple.n4')
  expected_graph = nt_parse('examples/model_prolog/prefix.nt')
  assert n4_graph == expected_graph

def test_prefix_default():
  n4_graph = n4_parse('examples/model_prolog/prefix-default.n4')
  expected_graph = nt_parse('examples/model_prolog/prefix.nt')
  assert n4_graph == expected_graph

def test_keyword():
  n4_graph = n4_parse('examples/model_prolog/keyword.n4')
  expected_graph = nt_parse('examples/model_prolog/keyword.nt')
  assert n4_graph == expected_graph

def test_import():
  n4_graph = n4_parse('examples/model_prolog/import.n4')
  expected_graph = nt_parse('examples/model_prolog/import.nt')
  assert n4_graph == expected_graph