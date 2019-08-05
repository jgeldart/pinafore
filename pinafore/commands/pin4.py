import argparse
import sys
from pathlib import Path
from rdflib import Graph
from pinafore.parser import Parser

ARGPARSER = argparse.ArgumentParser(description='parse a Notation4 file to RDF')

ARGPARSER.add_argument('input',
                        type=argparse.FileType('r'),
                        help='The Notation4 file to parse')

ARGPARSER.add_argument('-o', '--output',
                       dest='output',
                       type=argparse.FileType('wb'),
                       default=sys.stdout,
                       help='The location to write the output. Defaults to STDOUT')

ARGPARSER.add_argument('--format',
                       dest='output_format',
                       choices=['dot', 'xml', 'n3', 'turtle', 'nt', 'pretty-xml', 'trix', 'trig', 'nquads'],
                       default='turtle',
                       help='The serialization format to output.')

def main():
  args = ARGPARSER.parse_args()

  parser = Parser(args.input)

  if 'dot' == args.output_format:
    parser.export(args.output)
  else:
    path = Path(args.input.name).absolute()
    base = path.as_uri()
    
    document = parser.document
    document.set_base(base)
    
    g = Graph()
    
    for prefix, iri in document.namespaces.items():
      g.bind(prefix, iri)

    for t in document.triples:
      g.add(t)

    output_serialization = g.serialize(format=args.output_format)
    args.output.write(output_serialization)
