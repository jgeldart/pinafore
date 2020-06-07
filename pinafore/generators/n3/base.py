from collections import defaultdict
import uuid
from mako.template import Template
from rdflib import ConjunctiveGraph, URIRef, Literal, BNode
from textx import get_parent_of_type


class keydefaultdict(defaultdict):
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError( key )
        else:
            ret = self[key] = self.default_factory(key)
            return ret


class ResourceReference(object):

    def __init__(self, name, is_anonymous=False):
        if name is None:
            name = uuid.uuid4().urn
        name = name.strip()
        if is_anonymous:
            name = uuid.uuid5(uuid.NAMESPACE_URL, name).urn
        self._primary_ref = URIRef(name)
        self._secondary_refs = keydefaultdict(lambda x: BNode(name + "#" + x).skolemize())

    def __getitem__(self, name):
        return self._secondary_refs[name].n3()

    def __repr__(self):
        return self._primary_ref.n3()

    def __str__(self):
        return self._primary_ref.n3()


class BNodeReference(object):

    def __init__(self, name=None):
        if name is None:
            name = "N" + uuid.uuid4().hex
        self._primary_ref = BNode(name).skolemize()
        self._secondary_refs = keydefaultdict(lambda x: BNode(name + "#" + x).skolemize())

    def __getitem__(self, name):
        return self._secondary_refs[name].n3()

    def __repr__(self):
        return self._primary_ref.n3()

    def __str__(self):
        return self._primary_ref.n3()


class LiteralReference(object):

    def __init__(self, literal):
        self._primary_ref = literal

    def __repr__(self):
        return self._primary_ref.n3()

    def __str__(self):
        return self._primary_ref.n3()


class Resource(object):

    def __init__(self, **kwargs):
        super().__init__()
        self._primary_resource_ref = None
        for name, value in kwargs.items():
            setattr(self, name, value)

    def resource(self):
        if self._primary_resource_ref is None:
            ref = self.resource_reference()
            if ref is None:
                self._primary_resource_ref = BNodeReference()
            elif isinstance(ref, Resource):
                self._primary_resource_ref = ref.resource()
            elif isinstance(ref, Literal):
                self._primary_resource_ref = LiteralReference(ref)
            elif isinstance(ref, str):
                self._primary_resource_ref = ResourceReference(ref)
            else:
                self._primary_resource_ref = None
        return self._primary_resource_ref

    def resource_reference(self):
        if hasattr(self, "name") and self.name is not None:
            n = self.name
            if hasattr(self, "full_iri"):
                n = self.full_iri
            if n.startswith("<") and n.endswith(">"):
                return n[1:-1]
            else:
                return n
        elif hasattr(self, "expression") and isinstance(self.expression, Resource):
            return self.expression
        elif hasattr(self, "subject") and isinstance(self.subject, Resource):
            return self.subject
        elif hasattr(self, "value"):
            return Literal(self.value)
        else:
            return None

    def is_triple_source(self):
        return False

    def is_context(self):
        return False


DEFAULT_NAMESPACES = """
@prefix owl: <http://www.w3.org/2002/07/owl#>.
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.
@prefix xsd: <http://www.w3.org/2001/XMLSchema#>.
@prefix skos: <http://www.w3.org/2004/02/skos/core#>.
@prefix dct: <http://purl.org/dc/terms/>.
@prefix bibo: <http://purl.org/ontology/bibo/>.
@prefix vaem: <http://www.linkedmodel.org/schema/vaem#>.
@prefix log: <http://www.w3.org/2000/10/swap/log#>.
@prefix math: <http://www.w3.org/2000/10/swap/math#>.
@prefix list: <http://www.w3.org/2000/10/swap/list#>.
@prefix shacl: <http://www.w3.org/ns/shacl#>.
@prefix void: <http://rdfs.org/ns/void#>.
@prefix grddl: <http://www.w3.org/2003/g/data-view#>.
"""


WK_SKOLEM = "http://rdlib.net/.well-known/genid/rdflib/"


class Clause(Resource):

    def to_graph(self):
        return self._deskolem(self.convert(ConjunctiveGraph()))

    def _deskolem(self, graph):
        for s, p, o, c in graph.quads((None, None, None, None)):
            graph.remove((s, p, o, c))
            if isinstance(s, URIRef) and str(s).startswith(WK_SKOLEM):
                s = BNode(str(s).replace(WK_SKOLEM, ""))
            if isinstance(p, URIRef) and str(p).startswith(WK_SKOLEM):
                p = BNode(str(p).replace(WK_SKOLEM, ""))
            if isinstance(o, URIRef) and str(o).startswith(WK_SKOLEM):
                o = BNode(str(o).replace(WK_SKOLEM, ""))
            if isinstance(c, URIRef) and str(c).startswith(WK_SKOLEM):
                c = BNode(str(c).replace(WK_SKOLEM, ""))
            graph.add((s, p, o, c))
        return graph

    def convert(self, graph):
        template_clauses = self.clause()
        if not isinstance(template_clauses, list):
            template_clauses = [template_clauses]
        template_strs = [DEFAULT_NAMESPACES
                         + self.extra_namespaces()
                         + c for c in template_clauses]
        params = self._template_params()
        g = ConjunctiveGraph()
        for template_str in template_strs:
            graph_fragment = None
            try:
                graph_fragment = Template(template_str).render(**params)
                g.parse(data=graph_fragment, format="n3")
            except Exception:
                pass  # print(graph_fragment, params)
        merged_graph = self._merge_graphs(graph, g)
        final_graph = self._visit_children(merged_graph)
        return final_graph

    def is_triple_source(self):
        return True

    def clause(self):
        raise NotImplementedError("Clause definition not provided")

    def extra_namespaces(self):
        return ""

    def do_not_traverse(self):
        return []

    def _parent_resource(self, element=None):
        if element is None:
            element = self
        if hasattr(element, "parent"):
            if isinstance(element.parent, Resource):
                return element.parent
            else:
                return self._parent_resource(element=element.parent)
        else:
            return None

    def _template_params(self):
        params = {}
        params["this"] = self.resource()
        params["this_raw"] = self
        parent = self._parent_resource()
        if parent is not None:
            params["parent"] = self.parent.resource()
            params["parent_raw"] = self.parent
        ontology = get_parent_of_type("OntologyDecl", self)
        if ontology is not None:
            params["ontology"] = ontology.resource()
            params["ontology_raw"] = ontology
        for attr_name in self.__class__._tx_attrs:
            if hasattr(self, attr_name) and getattr(self, attr_name) is not None:
                attr_val = getattr(self, attr_name)
                res_val = self._resourcify_attribute(attr_val)
                if res_val is not None:
                    params[attr_name] = res_val
                params["{}_raw".format(attr_name)] = attr_val
        # print(params)
        return params

    def _resourcify_attribute(self, res):
        if hasattr(res, "ref") and isinstance(res.ref, Resource):
            res = res.ref.resource()
            return res
        if isinstance(res, Resource):
            return res.resource()
        elif isinstance(res, list):
            return [self._resourcify_attribute(a) for a in res]
        elif hasattr(res, "full_iri"):
            return ResourceReference(res.full_iri)
        elif hasattr(res, "ref") and hasattr(res.ref, "full_iri"):
            return ResourceReference(res.ref.full_iri)
        else:
            return None

    def _merge_graphs(self, graph, new_graph):
        final_graph = ConjunctiveGraph()
        for s, p, o, c in graph.quads():
            final_graph.add((s, p, o, c))
        for s, p, o, c in new_graph.quads():
            final_graph.add((s, p, o, c))
        for prefix, ns in graph.namespaces():
            final_graph.bind(prefix, ns)
        for prefix, ns in new_graph.namespaces():
            final_graph.bind(prefix, ns)

        return final_graph

    def _visit_children(self, graph):
        if self.is_context():
            g = ConjunctiveGraph(identifier=self.resource())
        else:
            g = graph

        for child in self._child_clauses():
            g = child.convert(g)

        return self._merge_graphs(graph, g)

    def _child_clauses(self, element=None, visited=set()):
        if element is None:
            element = self
        if not isinstance(element, list):
            visited.add(self)
        klass = element.__class__
        if hasattr(klass, "_tx_attrs"):
            for attr_name in klass._tx_attrs:
                if attr_name not in self.do_not_traverse():
                    attr = getattr(element, attr_name)
                    if (not isinstance(attr, list)) and (attr not in visited) and hasattr(attr.__class__, "_tx_attrs"):
                        if isinstance(attr, Clause):
                            yield attr
                        else:
                            for child in self._child_clauses(element=attr, visited=visited):
                                yield child
                    elif isinstance(attr, list):
                        for i in attr:
                            if isinstance(i, Clause):
                                yield i
                            else:
                                for child in self._child_clauses(element=i, visited=visited):
                                    yield child
