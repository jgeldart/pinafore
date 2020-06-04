from os.path import dirname, join
from urllib.parse import urldefrag
from textx import language, metamodel_from_file, get_model, get_metamodel, get_children, get_children_of_type, get_parent_of_type, textx_isinstance, TextXSemanticError
from .resolver import OntologyResolver, TermResolver

def relative_url(base, url):
    if not str(url).startswith(base):
        return str(url)

    first, frag = urldefrag(url)
    if frag != "":
        return str(frag)
    else:
        return str(url).replace(base, "")


def variable_scope_check(model, metamodel):
    def _decl_decider(x):
        return (
            hasattr(x, "name") and x.name is not None
            and (x.name.startswith("?") or x.name.startswith("!"))
            and (
                get_parent_of_type("Formula", x) is None
                and get_parent_of_type("ClassPatternDecl", x) is None
                and get_parent_of_type("PropertyPatternDecl", x) is None
                and get_parent_of_type("AttributePatternDecl", x) is None
                and get_parent_of_type("DatatypePatternDecl", x) is None
                and get_parent_of_type("IndividualPatternDecl", x) is None
                and get_parent_of_type("PropertyRestrictionPatternDecl", x) is None
                and get_parent_of_type("AttributeRestrictionPatternDecl", x) is None
                and get_parent_of_type("ModalPatternDecl", x) is None
                and get_parent_of_type("LiteralPatternDecl", x) is None
            )
        )

    def _ref_decider(x):
        return (
            ((hasattr(x, "universal_var") and x.universal_var is not None) or (hasattr(x, "existential_var") and x.existential_var is not None))
            and (
                get_parent_of_type("Formula", x) is None
                and get_parent_of_type("ClassPatternDecl", x) is None
                and get_parent_of_type("PropertyPatternDecl", x) is None
                and get_parent_of_type("AttributePatternDecl", x) is None
                and get_parent_of_type("DatatypePatternDecl", x) is None
                and get_parent_of_type("IndividualPatternDecl", x) is None
                and get_parent_of_type("PropertyRestrictionPatternDecl", x) is None
                and get_parent_of_type("AttributeRestrictionPatternDecl", x) is None
                and get_parent_of_type("ModalPatternDecl", x) is None
                and get_parent_of_type("LiteralPatternDecl", x) is None
            )
        )

    def _headed_list_decider(x):
        return (
            (x.__class__.__name__ == "HeadedList" or x.__class__.__name__.startswith("Infix"))
            and (
                get_parent_of_type("Formula", x) is None
                and get_parent_of_type("ClassPatternDecl", x) is None
                and get_parent_of_type("PropertyPatternDecl", x) is None
                and get_parent_of_type("AttributePatternDecl", x) is None
                and get_parent_of_type("DatatypePatternDecl", x) is None
                and get_parent_of_type("IndividualPatternDecl", x) is None
                and get_parent_of_type("PropertyRestrictionPatternDecl", x) is None
                and get_parent_of_type("AttributeRestrictionPatternDecl", x) is None
                and get_parent_of_type("ModalPatternDecl", x) is None
                and get_parent_of_type("LiteralPatternDecl", x) is None
            )
        )

    issues = get_children(_decl_decider, model)
    issues += get_children(_ref_decider, model)
    issues += get_children(_headed_list_decider, model)
    if len(issues) > 0:
        first_error = issues[0]
        if hasattr(first_error, "name"):
            var = "Variable '{}'".format(first_error.name)
        elif hasattr(first_error, "universal_var"):
            var = "Variable '{}'".format(first_error.universal_var)
        elif hasattr(first_error, "existential_var"):
            var = "Variable '{}'".format(first_error.existential_var)
        elif hasattr(first_error, "head"):
            var = "Headed list '{}'".format(first_error.head.ref.name)
        else:
            var = "Infix expression '{}'".format(first_error)
        parser = model._tx_parser
        line, col = parser.pos_to_linecol(
            first_error._tx_position
            )
        message = "{} used outside a formula or pattern in '{}'".format(
            var,
            str(first_error)
            )
        raise TextXSemanticError(
            message,
            line=line,
            col=col,
            filename=model._tx_filename
            )


def temporal_recursion_checker(model, metamodel):
    def _decider(x):
        return (x.__class__.__name__ == "ClassExpressionRecursion"
                and get_parent_of_type("ClassExpressionModalRepeat", x)
                is None)
    issues = get_children(_decider, model)
    if len(issues) > 0:
        first_error = issues[0]
        parser = model._tx_parser
        line, col = parser.pos_to_linecol(
            first_error._tx_position
            )
        message = "'again' used outside a recursion '{}'".format(
            str(first_error)
            )
        raise TextXSemanticError(
            message,
            line=line,
            col=col,
            filename=model._tx_filename
            )


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

    return mm
