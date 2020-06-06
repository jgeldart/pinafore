from .base import Clause


class Predicate(Clause):

    def clause(self):
        return """
            % for o in objects:
            ${parent} ${property} ${o}.
            % endfor
        """


MODELS = [
    Predicate
]
