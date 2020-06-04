from os.path import join
from io import StringIO
from pathlib import Path
import requests
from urllib.parse import urldefrag
from rdflib import Graph
from rdflib.util import guess_format
from textx import TextXSemanticError, get_model, get_metamodel
from .util import resolve_ontology, cache_ontology, error_for_object


ACCEPTED_RDF_FILE_FORMATS = [
    "xml",
    "turtle",
    "n3",
    "nt",
    "nquads",
    "rdfa"
]


class Extractor:

    def __init__(self, metamodel, ontology_iri):
        self._meta = metamodel
        self._ontology_iri = ontology_iri[1:-1]

    def query(self):
        return ""

    def class_name(self):
        pass

    def matches(self, graph):
        return graph.query(self.query())

    def convert(self, match):
        cstr = self._meta[self.class_name()]
        return self._apply_attrs(cstr,
                                 name=match['name'],
                                 expression=None,
                                 is_exported=True,
                                 modifiers=[],
                                 axioms=[])

    def converted_matches(self, graph):
        for m in self.matches(graph):
            yield self.convert(m)

    def _apply_attrs(self, cstr, **kwargs):
        c = cstr()
        for key, value in kwargs.items():
            if key == "name":
                value = self._relative_url(self._ontology_iri, value)
            setattr(c, key, value)
        return c

    def _relative_url(self, base, url):
        if not str(url).startswith(base):
            return str(url)

        first, frag = urldefrag(url)
        if frag != "":
            return str(frag)
        else:
            return str(url).replace(base, "")


class ClassExtractor(Extractor):

    def query(self):
        return """
        SELECT DISTINCT ?name WHERE {
            { ?name a <http://www.w3.org/2002/07/owl#Class>. }
            UNION
            { ?name a <http://www.w3.org/2000/01/rdf-schema#Class>. }
            UNION
            { ?name a <http://www.w3.org/2004/02/skos/core#Concept>.}
        }
        """

    def class_name(self):
        return "ClassDecl"


class PropertyExtractor(Extractor):

    def query(self):
        return """
        SELECT DISTINCT ?name WHERE {
            { ?name a <http://www.w3.org/2002/07/owl#ObjectProperty>. }
            UNION
            { ?name a <http://www.w3.org/2000/01/rdf-schema#Property>. }
        }
        """

    def class_name(self):
        return "PropertyDecl"


class AttributeExtractor(Extractor):

    def query(self):
        return """
        SELECT DISTINCT ?name WHERE {
            ?name a <http://www.w3.org/2002/07/owl#DatatypeProperty>.
        }
        """

    def class_name(self):
        return "AttributeDecl"


class DatatypeExtractor(Extractor):

    def query(self):
        return """
        SELECT DISTINCT ?name WHERE {
            ?name a <http://www.w3.org/2000/01/rdf-schema#Datatype>.
        }
        """

    def class_name(self):
        return "DatatypeDecl"


class IndividualExtractor(Extractor):

    def query(self):
        return """
        SELECT DISTINCT ?indiv WHERE {
            ?indiv a <http://www.w3.org/2002/07/owl#NamedIndividual>.
        }
        """

    def class_name(self):
        return "IndividualDecl"


class PatternExtractor(Extractor):
    pass


class RuleExtractor(Extractor):
    pass


class LabelledBNodeExtractor(Extractor):
    pass


class OntologyResolver:

    def __init__(self):
        pass

    def _resolve_location(self, obj, ontology_iri):
        root = Path(get_model(obj)._tx_filename).parent
        if hasattr(obj, "local_file") and obj.local_file != "":
            # Use a local file to resolve the import
            filename = Path(join(root, obj.local_file))
            contents = filename.read_text()
            return filename, contents
        else:
            # Pull the ontology from the provided IRI
            filename = ontology_iri
            response = requests.get(ontology_iri, headers={'accept': 'application/rdf+xml, text/rdf+n3, application/rdf+turtle, application/x-turtle, application/turtle, application/xml, */*'})
            if response.status_code in [200, 300, 301, 302]:
                contents = response.text
            return filename, contents

    def _load_ontology(self,
                       metamodel,
                       ontology_iri,
                       filename,
                       contents):
        ontology = None
        n4_error = None
        try:
            ontology = self._load_notation4(metamodel,
                                            filename,
                                            contents)
        except Exception as e:
            n4_error = e

        if ontology is not None:
            return ontology

        try:
            graph = self._load_rdf(filename, contents, ontology_iri)
            if len(graph) > 0:
                ontology = self._extract_rdf(metamodel,
                                             graph,
                                             ontology_iri)
        except Exception:
            pass

        if ontology is not None:
            return ontology
        elif n4_error is not None:
            raise n4_error
        else:
            return None

    def _load_notation4(self, metamodel, filename, contents):
        return metamodel.internal_model_from_file(filename,
                                                  is_main_model=True,
                                                  model_str=contents)

    def _load_rdf(self, filename, contents, ontology_iri):
        graph = Graph()

        try:
            graph.parse(data=contents,
                        format=guess_format(filename))
            return graph
        except Exception:
            pass

        for t in ACCEPTED_RDF_FILE_FORMATS:
            try:
                graph.parse(data=contents,
                            format=t)
                return graph
            except Exception:
                pass

        return None

    def _extract_rdf(self, metamodel, graph, ontology_iri):
        extractors = [
            ClassExtractor(metamodel, ontology_iri),
            PropertyExtractor(metamodel, ontology_iri),
            AttributeExtractor(metamodel, ontology_iri),
            DatatypeExtractor(metamodel, ontology_iri),
            IndividualExtractor(metamodel, ontology_iri)
            ]
        ontology = self._create_ontology_decl(metamodel, ontology_iri)
        ontology.assertions = [m
                               for ex
                               in extractors
                               for m
                               in ex.converted_matches(graph)]
        return ontology

    def _create_ontology_decl(self, metamodel, ontology_iri):
        cstr = metamodel["OntologyDecl"]
        o = cstr()
        o.name = ontology_iri
        o.expression = None
        o.prefix = None
        o.no_prelude = None
        o.prelude = None
        o.default_language = None
        o.axioms = []
        o.pragmas = []
        o.assertions = []
        return o

    def __call__(self, obj, attr, obj_ref):
        ontology_iri = obj_ref.obj_name
        model = get_model(obj)
        metamodel = get_metamodel(model)

        if not (ontology_iri.startswith("<") and ontology_iri.endswith(">")):
            raise TextXSemanticError(
                **error_for_object("Not a valid ontology IRI", obj))
        ontology = resolve_ontology(metamodel, ontology_iri)
        if ontology is not None:
            return ontology

        location = ontology_iri[1:-1]

        filename, contents = self._resolve_location(obj, location)
        ontology = self._load_ontology(metamodel,
                                       ontology_iri,
                                       filename,
                                       contents)

        if ontology is not None:
            cache_ontology(metamodel, ontology)

        return ontology
