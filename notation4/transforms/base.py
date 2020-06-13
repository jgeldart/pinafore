from textx import get_children, get_model


def is_a(element, class_name):
    return element.__class__.__name__ == class_name


def has_a(element, attr, **kwargs):
    attr_check = (
        hasattr(element, attr)
        and getattr(element, attr) is not None
        and getattr(element, attr) != ""
        )
    if "value" in kwargs.keys():
        return (attr_check and getattr(element, attr) == kwargs["value"])
    else:
        return attr_check


def resolve(element, pattern):
    result = {}
    for key, pattern_string in pattern.items():
        current = element
        components = pattern_string.split('.')
        for component in components:
            if hasattr(current, component):
                current = getattr(current, component)
        result[key] = current
    return result


def replace(old_element, new_element, replace_refs=True):
    # Replace parent-child
    if hasattr(old_element, "parent"):
        p = old_element.parent
        for attr in p.__class__._tx_attrs:
            if id(getattr(p, attr)) == id(old_element):
                setattr(p, attr, new_element)
        setattr(old_element, "parent", None)
        setattr(new_element, "parent", p)
    # Replace references
    if replace_refs:
        m = get_model(old_element)
        children = get_children(lambda x: True, m)
        for c in children:
            for attr in c.__class__._tx_attrs:
                if id(getattr(c, attr)) == id(old_element):
                    setattr(c, attr, new_element)


class Desugaring(object):

    def __init__(self):
        super().__init__()
        self._metamodel = None

    def __call__(self, model, metamodel):
        self._metamodel = metamodel
        try:
            for elm in get_children(lambda x: self.match(x), model):
                try:
                    bindings = self.bind(elm)
                    self.apply(elm, bindings)
                except Exception:
                    pass
        except Exception:
            pass

    def match(self, element):
        """
        Returns `True` if the element should be transformed.
        """
        raise NotImplementedError

    def bind(self, element):
        """
        Constructs bindings (a dictionary) for a matching element.
        """
        raise NotImplementedError

    def apply(self, element, bindings):
        """
        Perform a replacement of the given element using the provided
        bindings.
        """
        raise NotImplementedError

    def construct(self, class_name, **kwargs):
        cstr = self._metamodel[class_name]
        elm = cstr()
        for key, value in kwargs.items():
            setattr(elm, key, value)
        for attr_name in cstr._tx_attrs.keys():
            if attr_name not in kwargs.keys():
                setattr(elm, attr_name, None)
        return elm

    def position(self, element):
        starts = [e._tx_position
                  for e
                  in element._tx_attrs.values()
                  if hasattr(e, "_tx_position")]
        ends = [e._tx_position_end
                for e
                in element._tx_attrs.values()
                if hasattr(e, "_tx_position_end")]
        return min(starts), max(ends)

    def set_position(self, element, positions):
        start, end = positions
        element._tx_position = start
        element._tx_position_end = end
