from collections import OrderedDict, defaultdict

from textx import get_children, get_model


PREFIX_MAP_ATTR = "_n4_prefix_map"


def prefix_mapping(ontology):
    if hasattr(ontology, PREFIX_MAP_ATTR) and getattr(ontology, PREFIX_MAP_ATTR) is not None:
        prefix_map = getattr(ontology, PREFIX_MAP_ATTR)
    else:
        prefix_map = OrderedDict()
        imports = get_children(
            lambda x:
                x.__class__.__name__ == "ImportPragma",
            ontology
        )
        for i in imports:
            o = i.ontology.ref
            if o is not None:
                if hasattr(i, "is_exported") and i.is_exported:
                    setattr(o, "is_exported", True)
                if i.name is not None:
                    prefix_map[i.name] = o
                else:
                    prefix_map[i.ontology.ref.prefix] = o
        setattr(ontology, PREFIX_MAP_ATTR, prefix_map)
    return prefix_map


def resolve_prefix(ontology, prefix):
    """
    Resolve a prefix using a memorized prefix map.
    """
    prefix_map = prefix_mapping(ontology)
    if prefix in prefix_map.keys():
        return prefix_map[prefix]
    else:
        return None


def prefixes(ontology, as_reversed=False):
    """
    Returns an iterator over the ontology's defined prefixes.
    """
    prefix_map = prefix_mapping(ontology)
    if as_reversed:
        return reversed(prefix_map.values())
    else:
        return iter(prefix_map.values())


def defrag(ref_name):
    if ref_name.startswith("<") and ref_name.endswith(">"):
        return None, ref_name
    else:
        if ":" in ref_name:
            return ref_name.split(":")
        else:
            return None, ref_name


def _new_ontology_cache(metamodel):

    def _apply_attrs(cstr, **kwargs):
        c = cstr()
        for key, value in kwargs.items():
            setattr(c, key, value)
        return c

    return defaultdict(lambda iri: _apply_attrs(metamodel['OntologyDecl'], name=iri, prefix=None, no_prelude=None, prelude=None, default_language=None, axioms=[], pragmas=[], assertions=[]))


ONTOLOGY_CACHE_ATTR = '_n4_ontology_cache'


def resolve_ontology(metamodel, ontology_iri):
    if not hasattr(metamodel, ONTOLOGY_CACHE_ATTR):
        setattr(metamodel, ONTOLOGY_CACHE_ATTR, {})
    cache = getattr(metamodel, ONTOLOGY_CACHE_ATTR)

    if ontology_iri in cache.keys():
        return cache[ontology_iri]
    else:
        return None


def cache_ontology(metamodel, ontology):
    if not hasattr(metamodel, ONTOLOGY_CACHE_ATTR):
        setattr(metamodel, ONTOLOGY_CACHE_ATTR, {})
    cache = getattr(metamodel, ONTOLOGY_CACHE_ATTR)
    cache[ontology.name] = ontology
    return ontology


IRI_CACHE_ATTR = '_n4_iri_cache'


def resolve_iri(metamodel, iri):
    if not hasattr(metamodel, IRI_CACHE_ATTR):
        setattr(metamodel, IRI_CACHE_ATTR, {})
    cache = getattr(metamodel, IRI_CACHE_ATTR)
    if iri in cache.keys():
        return cache[iri]
    else:
        return None


def cache_iri(metamodel, iri, val):
    if not hasattr(metamodel, IRI_CACHE_ATTR):
        setattr(metamodel, IRI_CACHE_ATTR, {})
    cache = getattr(metamodel, IRI_CACHE_ATTR)
    cache[iri] = val
    return val


def error_for_object(msg, obj):
    model = get_model(obj)
    parser = model._tx_parser
    line, col = parser.pos_to_linecol(
        obj._tx_position
        )
    filename = model._tx_filename
    return {
        'message': msg,
        'line': line,
        'col': col,
        'filename': filename
    }
