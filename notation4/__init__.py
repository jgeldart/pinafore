from os.path import dirname, join
from textx import language, metamodel_from_file
from .resolver import OntologyResolver, TermResolver
from .checks import temporal_recursion_checker, variable_scope_check
from .util import iri_rewriter


def metamodel(classes=None):
    if classes is None:
        mm = metamodel_from_file(
            join(dirname(__file__),
                 "notation4.tx"),
            autokwd=True,
            memoization=True,
            use_regexp_group=True)
    else:
        mm = metamodel_from_file(
            join(dirname(__file__),
                 "notation4.tx"),
            classes=classes,
            autokwd=True,
            memoization=True,
            use_regexp_group=True)

    mm.register_scope_providers({
        'OntologyRef.ref': OntologyResolver(),
        'ClassRef.ref': TermResolver("Class"),
        'PropertyRef.ref': TermResolver("Property"),
        'AttributeRef.ref': TermResolver("Attribute"),
        'DatatypeRef.ref': TermResolver("Datatype"),
        'IndividualRef.ref': TermResolver("Individual"),
        'ConstantRef.ref': TermResolver("Constant"),
        'BNodeRef.ref': TermResolver("BNode"),
        'GraphRef.ref': TermResolver("Graph"),
        'PredicateRef.ref': TermResolver(["Property", "Attribute"]),
        'ObjectRef.ref': TermResolver(["Class", "Property", "Attribute", "Datatype", "Individual", "Constant", "BNode", "Graph"])
    })
    mm.register_model_processor(variable_scope_check)
    mm.register_model_processor(temporal_recursion_checker)
    mm.register_obj_processors({
        'ClassDecl': iri_rewriter,
        'PropertyDecl': iri_rewriter,
        'AttributeDecl': iri_rewriter,
        'DatatypeDecl': iri_rewriter,
        'IndividualDecl': iri_rewriter,
        'ConstantDecl': iri_rewriter,
        'BNodeDecl': iri_rewriter,
        'GraphDecl': iri_rewriter,
    })

    return mm


@language("Notation4", "*.n4")
def notation4(classes=None):
    "A high-level ontology language."
    mm = metamodel(classes=classes)
    return mm
