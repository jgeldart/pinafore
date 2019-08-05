from textx import metamodel_from_file

from pinafore.model import MODEL_CLASSES

NOTATION4_META = metamodel_from_file('pinafore/notation4/grammar/notation4.tx', debug=False, classes=MODEL_CLASSES, use_regexp_group=True, autokwd=True, memoization=True)

# TODO: Register processors to check for semantic correctness