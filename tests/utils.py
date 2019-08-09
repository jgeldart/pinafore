from pathlib import Path
from rdflib import Graph
from rdflib.compare import to_isomorphic, to_canonical_graph

from pinafore.parser import Parser

def n4_parse(rel_file):
  n4_file = Path('tests/{0}'.format(rel_file)).absolute()
  with open(n4_file, 'r') as f:
    parser = Parser(f)
    doc = parser.document
    doc.set_base(n4_file.as_uri())

    g = Graph()
    for prefix, iri in doc.namespaces.items():
      g.bind(prefix, iri)

    for t in doc.triples:
      g.add(t)

    return to_isomorphic(g)


def rdf_parse(rel_file, fmt):
  rdf_file = Path('tests/{0}'.format(rel_file)).absolute()
  return to_isomorphic(Graph().parse(format=fmt, file=rdf_file.open('rb')))

def nt_parse(rel_file):
  return rdf_parse(rel_file, 'nt')

def ttl_parse(rel_file):
  return rdf_parse(rel_file, 'ttl')