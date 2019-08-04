from textx import metamodel_from_file

notation4_meta = metamodel_from_file("notation4.tx")

def parse(file_name):
  return notation4_meta.model_from_file(file_name)