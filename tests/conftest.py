from rdflib.graph import Graph
from rdflib.compare import graph_diff


def serialize_nt(g):
  return [ l.decode('utf8') for l in sorted(g.serialize(format='nt').splitlines()) if l ]

def pytest_assertrepr_compare(op, left, right):
  if isinstance(left, Graph) and isinstance(right, Graph):
    in_both, in_first, in_second = graph_diff(left, right)
    return ['ONLY IN FIRST:', ''] + serialize_nt(in_first) + ['', 'ONLY IN SECOND:', ''] + serialize_nt(in_second)
    #return ['In both:\n\n{0}'.format(serialize_nt(in_both)), 'In first:\n\n{0}'.format(serialize_nt(in_first)), 'In second:\n\n{0}'.format(serialize_nt(in_second))]