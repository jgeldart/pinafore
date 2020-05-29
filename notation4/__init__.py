from os.path import dirname, join
from pathlib import Path
from io import StringIO
from urllib.parse import urldefrag, urlparse
from rdflib import Graph
from rdflib.util import guess_format
import requests
from textx import language, metamodel_from_file, get_model, get_metamodel, get_children, get_children_of_type, textx_isinstance, TextXSemanticError

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
        ontology = _apply_attrs(metamodel['OntologyDecl'], name=base, prefix=None, no_prelude=None, prelude=None, default_language=None, pragmas=[], assertions=[])

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
        ontology_iri = obj_ref.obj_name

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

    def __init__(self, ref_type):
        self._keyword_class = "KeywordPragma{}".format(ref_type)
        self._declaration_class = "{}Decl".format(ref_type)

    def _possible_matches(self, obj, ref_name):
        model = get_model(obj)
        if ":" in ref_name:
            prefix, ref_name = ref_name.split(":")
            ontologies = [o.ontology.ref for o in get_children(
                lambda x:
                    hasattr(x, "name")
                    and x.name == prefix
                    and x.__class__.__name__ == "ImportPragma",
                model
                )]
            if len(ontologies) > 0:
                model = ontologies[0]
        return get_children(
            lambda x:
                hasattr(x, "name")
                and x.name == ref_name
                and (
                    x.__class__.__name__ == self._keyword_class
                    or x.__class__.__name__ == self._declaration_class
                    ),
                model
                )

    def _resolve_ref(self, obj, ref_name):
        matches = self._possible_matches(obj, ref_name)
        if len(matches) > 0:
            match = matches[0]
            if match.__class__.__name__ == self._keyword_class:
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


@language("Notation4", "*.n4")
def notation4():
    "A high-level ontology language."
    mm = metamodel_from_file(
        join(dirname(__file__),
             "notation4.tx"),
        use_regexp_group=True)
    mm.register_scope_providers({
        'OntologyRef.ref': OntologyResolver(),
        'ClassRef.ref': FYNResolver("Class"),
        'PropertyRef.ref': FYNResolver("Property"),
        'AttributeRef.ref': FYNResolver("Attribute"),
        'DatatypeRef.ref': FYNResolver("Datatype"),
        'IndividualRef.ref': FYNResolver("Individual"),
    })

    return mm
