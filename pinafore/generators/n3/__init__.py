import click
from os.path import join, dirname, basename, splitext, abspath, exists
from itertools import chain
from textx import generator
from notation4 import metamodel as n4_metamodel
from .attributes import MODELS as attribute_models
from .bnodes import MODELS as bnode_models
from .classes import MODELS as class_models
from .class_expressions import MODELS as class_expression_models
from .datatypes import MODELS as datatype_models
from .datatype_expressions import MODELS as datatype_expression_models
from .graphs import MODELS as graph_models
from .individuals import MODELS as individual_models
from .literals import MODELS as literal_models
from .ontologies import MODELS as ontology_models
from .predicates import MODELS as predicate_models
from .properties import MODELS as property_models
from .property_expressions import MODELS as property_expression_models


MODELS = chain(attribute_models,
               bnode_models,
               class_models,
               class_expression_models,
               datatype_models,
               datatype_expression_models,
               graph_models,
               individual_models,
               literal_models,
               ontology_models,
               predicate_models,
               property_models,
               property_expression_models)


@generator("notation4", "n3")
def n3_generator(metamodel, model, output_path, overwrite, debug, **custom_args):
    metamodel = n4_metamodel(classes=MODELS)

    # Determine file path parts
    input_file = model._tx_filename
    base_dir = output_path if output_path else dirname(input_file)
    base_name, _ = splitext(basename(input_file))
    output_file = abspath(join(base_dir, "{}.{}".format(base_name, 'n3')))

    # Reparse model
    model = metamodel.model_from_file(input_file)

    # Convert to a graph
    g = model.to_graph()

    # Output
    if overwrite or not exists(output_file):
        click.echo('-> {}'.format(output_file))
        g.serialize(output_file, format="n3")
    else:
        click.echo('-- Skipping: {}'.format(output_file))
