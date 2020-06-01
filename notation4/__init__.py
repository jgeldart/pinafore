from os.path import dirname, join
from pathlib import Path
from io import StringIO
from urllib.parse import urldefrag, urlparse
from rdflib import Graph
from rdflib.util import guess_format
import requests
from textx import language, metamodel_from_file, get_model, get_metamodel, get_children, get_children_of_type, get_parent_of_type, textx_isinstance, TextXSemanticError

from textx.const import RULE_COMMON, RULE_ABSTRACT
from textx.model import ObjCrossRef
from textx.scoping.tools import get_parser


def relative_url(base, url):
    if not str(url).startswith(base):
        return str(url)

    first, frag = urldefrag(url)
    if frag != "":
        return str(frag)
    else:
        return str(url).replace(base, "")


class OntologyResolver:

    def __init__(self):
        pass

    def _parse_rdf(self, contents, file_name):
        reader = StringIO(contents)
        g = Graph()
        try:
            g.parse(reader, format=guess_format(file_name))
            return g
        except Exception:
            pass

        try:
            g.parse(reader, format='xml')
            return g
        except Exception:
            pass

        try:
            g.parse(reader, format='turtle')
            return g
        except Exception:
            pass

        try:
            g.parse(reader, format='n3')
            return g
        except Exception:
            pass

        try:
            g.parse(reader, format='nt')
            return g
        except Exception:
            pass

        try:
            g.parse(reader, format='nquads')
            return g
        except Exception:
            pass

        try:
            g.parse(reader, format='rdfa')
            return g
        except Exception:
            pass

        return None

    def _extract_rdf_ontology(self, metamodel, graph, ontology_iri):

        def _apply_attrs(cstr, **kwargs):
            c = cstr()
            for name, value in kwargs.items():
                setattr(c, name, value)
            return c

        base = str(ontology_iri)
        ontology = _apply_attrs(metamodel['OntologyDecl'], name="<{}>".format(base), prefix=None, no_prelude=None, prelude=None, default_language=None, axioms=[], pragmas=[], assertions=[])

        classes = graph.query("""
                        SELECT DISTINCT ?cls WHERE {
                            { ?cls a <http://www.w3.org/2002/07/owl#Class>. }
                            UNION
                            { ?cls a <http://www.w3.org/2000/01/rdf-schema#Class>. }
                            UNION
                            { ?cls a <http://www.w3.org/2004/02/skos/core#Concept>.}
                        }
                        """)
        f = metamodel['ClassDecl']
        class_decls = [_apply_attrs(f, parent=ontology, is_exported=True, name=relative_url(base, result[0]), axioms=[]) for result in classes]

        properties = graph.query("""
                                 SELECT DISTINCT ?prop WHERE {
                                    { ?prop a <http://www.w3.org/2002/07/owl#ObjectProperty>. }
                                    UNION
                                    { ?prop a <http://www.w3.org/2000/01/rdf-schema#Property>. }
                                 }
                                 """)
        f = metamodel['PropertyDecl']
        property_decls = [_apply_attrs(f, parent=ontology, is_exported=True, name=relative_url(base, result[0]), axioms=[]) for result in properties]

        attributes = graph.query("""
                                 SELECT DISTINCT ?attr WHERE {
                                    ?attr a <http://www.w3.org/2002/07/owl#DatatypeProperty>.
                                 }
                                 """)
        f = metamodel['AttributeDecl']
        attribute_decls = [_apply_attrs(f, parent=ontology, is_exported=True, name=relative_url(base, result[0]), axioms=[]) for result in attributes]

        datatypes = graph.query("""
                                 SELECT DISTINCT ?attr WHERE {
                                    ?attr a <http://www.w3.org/2000/01/rdf-schema#Datatype>.
                                 }
                                 """)
        f = metamodel['DatatypeDecl']
        datatype_decls = [_apply_attrs(f, parent=ontology, is_exported=True, name=relative_url(base, result[0]), axioms=[]) for result in datatypes]

        individuals = graph.query("""
                                 SELECT DISTINCT ?indiv WHERE {
                                     ?indiv a <http://www.w3.org/2002/07/owl#NamedIndividual>.
                                 }
                                 """)
        f = metamodel['IndividualDecl']
        individual_decls = [_apply_attrs(f, parent=ontology, is_exported=True, name=relative_url(base, result[0]), axioms=[]) for result in individuals]

        ontology.assertions = class_decls + property_decls + attribute_decls + datatype_decls + individual_decls

        if not hasattr(metamodel, "_ontologies"):
            setattr(metamodel, "_ontologies", {})

        metamodel._ontologies[base] = ontology

        return ontology

    def __call__(self, obj, attr, obj_ref):
        model = get_model(obj)
        the_metamodel = get_metamodel(model)
        ontology_iri = obj_ref.obj_name[1:-1]

        if hasattr(the_metamodel, "_ontologies") and ontology_iri in the_metamodel._ontologies.keys():
            return the_metamodel._ontologies[ontology_iri]

        root = Path(get_model(obj)._tx_filename).parent
        ontology_file_contents = ""
        file_name = ""
        if hasattr(obj, "local_file") and obj.local_file is not None and obj.local_file != "":
            # Use a local file to resolve the import
            file_name = Path(join(root, obj.local_file))
            ontology_file_contents = file_name.read_text()
        else:
            # Pull the ontology from the provided IRI
            file_name = ontology_iri
            response = requests.get(ontology_iri, headers={'accept': 'application/rdf+xml, text/rdf+n3, application/rdf+turtle, application/x-turtle, application/turtle, application/xml, */*'})
            if response.status_code in [200, 300, 301, 302]:
                ontology_file_contents = response.text

        imported_model = None

        # Parse the ontology using a progression of parsers
        # First, Notation4
        try:
            imported_model = the_metamodel.internal_model_from_file(file_name, is_main_model=True, model_str=ontology_file_contents)
        except Exception:
            pass

        # Then generic RDF
        if imported_model is None:
            g = self._parse_rdf(ontology_file_contents, file_name)

            if g is not None:
                imported_model = self._extract_rdf_ontology(the_metamodel, g, ontology_iri)

        if not hasattr(the_metamodel, "_ontologies"):
            setattr(the_metamodel, "_ontologies", {})
        the_metamodel._ontologies[ontology_iri] = imported_model

        # Finally, just return what we've gotten
        return imported_model


class FYNResolver:

    def __init__(self, ref_types):
        if not isinstance(ref_types, list):
            ref_types = [ref_types]

        self._keyword_classes = ["KeywordPragma{}".format(ref_type) for ref_type in ref_types]
        self._declaration_classes = ["{}Decl".format(ref_type) for ref_type in ref_types]

    def _resolve_prefix(self, scope, prefix):
        ontologies = [o.ontology.ref for o in get_children(lambda x: hasattr(x, "name") and x.name == prefix and x.__class__.__name__ == "ImportPragma", scope)]
        if len(ontologies) > 0:
            return ontologies[0]
        else:
            return scope

    def _possible_keyword_matches(self, scope, ref_name):

        def _decide_match(is_local=True):
            def f(x):
                return (
                    hasattr(x, "name")
                    and x.name == ref_name
                    and x.__class__.__name__ in self._keyword_classes
                    and hasattr(x, "is_exported")
                    and (is_local or x.is_exported)
                )
            return f

        potential_matches = get_children(_decide_match(), scope)
        potential_matches += [k for o in [get_children(_decide_match(False), o.ontology.ref) for o in get_children_of_type("ImportPragma", scope)] for k in o]
        return potential_matches

    def _possible_qname_matches(self, scope, ref_name):
        if ":" in ref_name:
            prefix, ref_name = ref_name.split(":")
            new_scope = self._resolve_prefix(scope, prefix)
        else:
            new_scope = scope

        return get_children(
            lambda x:
                hasattr(x, "name")
                and x.name == ref_name
                and (
                    x.__class__.__name__ in self._keyword_classes
                    or x.__class__.__name__ in self._declaration_classes
                )
                and (
                    new_scope == scope or (hasattr(x, "is_exported") and x.is_exported)
                ),
            new_scope
        )

    def _possible_iri_matches(self, scope, ref_name):

        def _decide_match(x):
            return (hasattr(x, "name")
                    and hasattr(x, "parent") and x.parent is not None
                    and x.parent.__class__.__name__ == "OntologyDecl"
                    and (x.parent.name[1:-1] + x.name == ref_name)
                    and (
                        x.__class__.__name__ in self._keyword_classes
                        or x.__class__.__name__ in self._declaration_classes
                    ))
        potential_matches = [get_children(_decide_match, o.ontology.ref) for o in get_children_of_type("ImportPragma", scope)]
        return [m for o in potential_matches for m in o]

    def _possible_matches(self, obj, ref_name):
        model = get_model(obj)
        if ref_name.startswith("<") and ref_name.endswith(">"):
            return self._possible_iri_matches(model, ref_name[1:-1])
        else:
            return self._possible_qname_matches(model, ref_name) + self._possible_keyword_matches(model, ref_name)

    def _resolve_ref(self, obj, ref_name):
        matches = self._possible_matches(obj, ref_name)
        if len(matches) > 0:
            match = matches[0]
            if match.__class__.__name__ in self._keyword_classes:
                return match.entity.ref
            else:
                return matches[0]

    def __call__(self, obj, attr, obj_ref):
        if obj_ref is None:
            return None  # Oops

        assert type(obj_ref) is ObjCrossRef, type(obj_ref)

        if get_parser(obj).debug:
            get_parser(obj).dprint("Resolving obj crossref: {}:{}"
                                   .format(obj_ref.cls, obj_ref.obj_name))

        return self._resolve_ref(obj, obj_ref.obj_name)


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
        'ClassRef.ref': FYNResolver("Class"),
        'PropertyRef.ref': FYNResolver("Property"),
        'AttributeRef.ref': FYNResolver("Attribute"),
        'DatatypeRef.ref': FYNResolver("Datatype"),
        'IndividualRef.ref': FYNResolver("Individual"),
        'ConstantRef.ref': FYNResolver("Constant"),
        'BNodeRef.ref': FYNResolver("BNode"),
        'GraphRef.ref': FYNResolver("Graph"),
        'PredicateRef.ref': FYNResolver(["Property", "Attribute"]),
        'ObjectRef.ref': FYNResolver(["Class", "Property", "Attribute", "Datatype", "Individual", "Constant", "BNode", "Graph"])
    })
    mm.register_model_processor(variable_scope_check)
    mm.register_model_processor(temporal_recursion_checker)

    return mm
