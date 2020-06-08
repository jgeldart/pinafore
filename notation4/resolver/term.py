from os.path import join, dirname
from textx import get_model, get_metamodel, get_children, metamodel_from_file, get_parent_of_type
from .util import prefixes, resolve_prefix, defrag, cache_ontology
from .ontology import OntologyResolver
from ..util import iri_rewriter


PRELUDE = None


class TermResolver:
    """
      Resolve references to terms (classes, properties, etc.)
      based on the scoping rules of Notation4.

      If the term has a prefix, look up that prefix on the current
      ontology and search for the term there. If the prefix is empty,
      treat as a keyword and apply the keyword scoping rules:

      1. Search the current ontology for the term. If the term is found,
          return the last mentioned declaration for the term.

      2. Load the imported ontologies and, searching from last to first
          import, try to match the term there.

      3. If a custom prelude is defined, search it for the term.

      4. If no custom prelude is defined and a prelude is enabled, load
          the standard prelude and search for the term there.

      5. If the term is still not found, return None.
    """

    def __init__(self, kinds=[]):
        if not isinstance(kinds, list):
            kinds = [kinds]

        self._keyword_classes = [
            "KeywordPragma{}".format(ref_type)
            for ref_type
            in kinds]
        self._decl_classes = [
            "{}Decl".format(ref_type)
            for ref_type
            in kinds]

        # Set up default prelude

    def _prelude(self):
        global PRELUDE
        if PRELUDE is None:
            metamodel = self._metamodel()
            filename = join(dirname(__file__), "../prelude.n4")
            model = metamodel.model_from_file(filename)
            PRELUDE = model
        return PRELUDE

    def _metamodel(self):
        mm = metamodel_from_file(join(dirname(__file__),
                                 "../notation4.tx"),
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

    def _scopes(self, obj):
        def _follow(scope):
            for ontology in prefixes(scope, as_reversed=True):
                if hasattr(ontology, "is_exported") and ontology.is_exported:
                    yield ontology
                    for o in _follow(ontology):
                        yield o
        # 1st scope: the current ontology
        current_ontology = get_model(obj)
        yield current_ontology
        # 2nd scopes: the imports in reverse order
        for ontology in prefixes(current_ontology, as_reversed=True):
            yield ontology
            for o in _follow(ontology):  # Follow the export chain
                yield o
        # 3rd scope: the prelude if defined
        if current_ontology.prelude is not None:
            prelude = current_ontology.prelude.ref
        elif current_ontology.no_prelude is None:
            prelude = self._prelude()
            yield prelude
            for o in _follow(prelude):
                yield o
        else:
            pass

    def _match(self, scope, ref_name, classes, search_all=True):

        def _decider(elm):
            base_condition = (
                hasattr(elm, "name")
                and elm.name == ref_name
                and elm.__class__.__name__ in classes
            )
            if search_all:
                return base_condition
            else:
                return (base_condition
                        and hasattr(elm, "is_exported")
                        and elm.is_exported)

        if scope is None:
            return iter([])

        for m in get_children(_decider, scope):
            yield m

    def _match_qname(self, scope, local_name, search_all=True):
        return self._match(scope,
                           local_name,
                           self._decl_classes,
                           search_all=search_all)

    def _match_keyword(self, scope, ref_name, search_all=True):
        return self._match(scope,
                           ref_name,
                           self._keyword_classes,
                           search_all=search_all)

    def __call__(self, obj, attr, obj_ref):
        current_ontology = get_model(obj)
        ref_name = obj_ref.obj_name
        prefix, local_name = defrag(ref_name)
        matches = []
        if prefix is None:
            referenced_ontology = current_ontology
        else:
            referenced_ontology = resolve_prefix(current_ontology, prefix)
        matches += [
            m
            for m
            in self._match_qname(
                referenced_ontology,
                local_name,
                search_all=(referenced_ontology == current_ontology)
                )
            ]
        matches += [
                   m.entity.ref
                   for o in self._scopes(obj)
                   for m in self._match_keyword(
                       o,
                       local_name,
                       search_all=(o == current_ontology)
                       )
                  ]
        if len(matches) > 0:
            # if hasattr(matches[0], "full_iri"):
            #     print(ref_name, matches[0].full_iri)
            # else:
            #     print(ref_name, "__")
            return matches[0]
        else:
            print(referenced_ontology, prefix, local_name)
            return None