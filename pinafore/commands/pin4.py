import argparse
import sys
from pinafore.parser import Parser

ARGPARSER = argparse.ArgumentParser(description='parse a Notation4 file to RDF')

ARGPARSER.add_argument('input',
                        type=argparse.FileType('r'),
                        help='The Notation4 file to parse')

ARGPARSER.add_argument('-o', '--output',
                       dest='output',
                       type=argparse.FileType('w'),
                       default=sys.stdout,
                       help='The location to write the output. Defaults to STDOUT')

def main():
  args = ARGPARSER.parse_args()

  parser = Parser(args.input)

  parser.export(args.output)