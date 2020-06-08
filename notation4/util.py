from textx import get_parent_of_type


def iri_rewriter(element):
    ontology = get_parent_of_type("OntologyDecl", element)
    if hasattr(element, "name") and element.name is not None:
        if element.name.startswith("<") and element.name.endswith(">"):
            setattr(element, "full_iri", element.name[1:-1])
        else:
            setattr(element, "full_iri", ontology.name[1:-1] + element.name)
