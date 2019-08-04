from pinafore.metamodel import NOTATION4_META

from textx.export import model_export_to_file

class Parser(object):

  def __init__(self, file):
    if isinstance(file, str):
      with open(file, 'r') as f:
        self._file_content = f.read()
    else:
      self._file_content = file.read()

    self._model = None

  @property
  def raw_document(self):
    if self._model is not None:
      return self._model
    else:
      self._model = NOTATION4_META.model_from_str(self._file_content)
      return self._model

  def export(self, file):
    model_export_to_file(file, model=self.raw_document)
