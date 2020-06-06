from .base import Clause


class OntologyDecl(Clause):

    def extra_namespaces(self):
        nss = "@prefix vann: <http://purl.org/vocab/vann/>."
        if self.prefix is not None:
            nss += " @prefix {}: {}.".format(self.prefix, self.resource())
        return nss

    def clause(self):
        return ["${this} a owl:Ontology.",
                "${this} vann:preferredNamespacePrefix \"${prefix_raw}\"."]


class ImportPragma(Clause):

    def extra_namespaces(self):
        return "@prefix {}: {}.".format(self.name, self.ontology.ref.resource())

    def do_not_traverse(self):
        return ["ontology"]

    def clause(self):
        return """
        ${parent} owl:imports ${ontology}.
        """


MODELS = [
    OntologyDecl,
    ImportPragma
]
