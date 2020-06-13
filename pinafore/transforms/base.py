from lxml import etree


class XMLSerializer(object):

    def __init__(self, metamodel):
        self._metamodel = metamodel

    def to_xml(self, model):
        root = etree.Element("model")
        root_attributes = root.attrib
        root_attributes["filename"] = model._tx_filename
        root_attributes["metamodel"] = "notation4"
        self._convert_to_xml_element(root, model)

    def from_xml(self, xml_doc):
        pass

    def _convert_to_xml_element(self, parent_xml, model_elm):
        child_xml = etree.Element(model_elm.__class__.__name__)
        for key, value in self._to_xml_attributes(model_elm):
            child_xml.attrib[key] = value
        for child_elm in self._to_xml_children(model_elm):
            self._convert_to_xml_element(child_xml, child_elm)
        parent_xml.append(child_xml)
        return parent_xml
