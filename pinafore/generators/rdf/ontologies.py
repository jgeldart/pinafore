from .base import Clause


class OntologyDecl(Clause):

    def extra_namespaces(self):
        nss = "@prefix vann: <http://purl.org/vocab/vann/>."
        if self.prefix is not None:
            nss += " @prefix {}: {}.".format(self.prefix, self.resource())
        return nss

    def resource_reference(self, is_anonymous=False, file_hash=None):
        if is_anonymous and hasattr(self, "parent") and self.parent is None and file_hash is not None:
            return file_hash
        else:
            return super().resource_reference(is_anonymous=is_anonymous, file_hash=file_hash)

    def clause(self):
        return ["${this} a owl:Ontology.",
                "${this} vann:preferredNamespacePrefix \"${prefix_raw}\"."]

    def is_context(self):
        return True


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
