from os.path import dirname, join
from textx import language, metamodel_from_file


@language("Notation4", "*.n4")
def notation4():
    "A high-level ontology language."
    return metamodel_from_file(join(dirname(__file__), "notation4.tx"), use_regexp_group=True)
