from os.path import dirname, join
from textx import language, metamodel_from_file, get_children, get_parent_of_type
from .resolver import OntologyResolver, TermResolver
from .resolver.util import cache_ontology, resolve_ontology
from .checks import temporal_recursion_checker, variable_scope_check


def iri_rewriter(element):
    ontology = get_parent_of_type("OntologyDecl", element)
    if hasattr(element, "name") and element.name.startswith("<") and element.name.endswith(">"):
        setattr(element, "full_iri", element.name[1:-1])
    elif hasattr(element, "name"):
        setattr(element, "full_iri", ontology.name[1:-1] + element.name)


@language("Notation4", "*.n4")
def notation4():
    "A high-level ontology language."
    mm = metamodel_from_file(
        join(dirname(__file__),
             "notation4.tx"),
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
    })

    return mm
