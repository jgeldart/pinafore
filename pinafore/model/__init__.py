'''
pinafore/model/__init__.py
'''

import itertools

import pinafore.model.document as document
import pinafore.model.prolog as prolog
import pinafore.model.statements as statements
import pinafore.model.bnodes as bnodes
import pinafore.model.collections as collections
import pinafore.model.identifiers as identifiers
import pinafore.model.literals as literals

MODEL_CLASSES = list(itertools.chain(
  document.MODEL_CLASSES,
  prolog.MODEL_CLASSES,
  statements.MODEL_CLASSES,
  bnodes.MODEL_CLASSES,
  collections.MODEL_CLASSES,
  identifiers.MODEL_CLASSES,
  literals.MODEL_CLASSES
  ))