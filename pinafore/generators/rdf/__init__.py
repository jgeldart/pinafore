import click
from os.path import join, dirname, basename, splitext, abspath, exists
from hashlib import sha512
from itertools import chain
from textx import generator
from notation4 import metamodel as n4_metamodel
from .attributes import MODELS as attribute_models
from .attribute_expressions import MODELS as attribute_expression_models
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
from .value_restrictions import MODELS as value_restriction_models


MODELS = chain(attribute_models,
               attribute_expression_models,
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
               property_expression_models,
               value_restriction_models)


def file_components(model, output_path, output_ext):
    input_file = model._tx_filename
    base_dir = output_path if output_path else dirname(input_file)
    base_name, _ = splitext(basename(input_file))
    output_file = abspath(join(base_dir, "{}.{}".format(base_name, output_ext)))
    return input_file, output_file


def write_file(g, output_file, format, overwrite=False):
    if overwrite or not exists(output_file):
        click.echo('-> {}'.format(output_file))
        g.serialize(output_file, format=format)
    else:
        click.echo('-- Skipping: {}'.format(output_file))


def convert_to_graph(input_file, anonymize=False):
    metamodel = n4_metamodel(classes=MODELS)
    # Determine file hash
    file_hash = None
    if anonymize:
        with open(input_file, 'r') as f:
            file_contents = f.read()
            file_hash = sha512(file_contents.encode()).hexdigest()

    # Reparse model
    model = metamodel.model_from_file(input_file)

    # Convert to a graph
    g = model.to_graph(anonymize=anonymize, file_hash=file_hash)

    return g


@generator("notation4", "rdfxml")
def rdfxml_generator(metamodel, model, output_path, overwrite, debug, anonymize=False, **custom_args):

    # Determine file path parts
    input_file, output_file = file_components(model, output_path, 'rdf')

    # Convert to a graph
    g = convert_to_graph(input_file, anonymize=anonymize)

    # Output
    write_file(g, output_file, 'pretty-xml', overwrite=overwrite)


@generator("notation4", "nquads")
def nquads_generator(metamodel, model, output_path, overwrite, debug, anonymize=False, **custom_args):

    # Determine file path parts
    input_file, output_file = file_components(model, output_path, 'nq')

    # Convert to a graph
    g = convert_to_graph(input_file, anonymize=anonymize)

    # Output
    write_file(g, output_file, 'nquads', overwrite=overwrite)


@generator("notation4", "n3")
def n3_generator(metamodel, model, output_path, overwrite, debug, anonymize=False, **custom_args):

    # Determine file path parts
    input_file, output_file = file_components(model, output_path, 'n3')

    # Convert to a graph
    g = convert_to_graph(input_file, anonymize=anonymize)

    # Output
    write_file(g, output_file, 'n3', overwrite=overwrite)
