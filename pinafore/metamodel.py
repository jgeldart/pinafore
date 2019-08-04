from textx import metamodel_from_file

NOTATION4_META = metamodel_from_file('pinafore/notation4/grammar/notation4.tx', use_regexp_group=True, autokwd=True, memoization=True)

# TODO: Register processors to check for semantic correctness