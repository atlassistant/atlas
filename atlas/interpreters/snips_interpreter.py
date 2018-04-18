from . import Interpreter
from snips_nlu import load_resources, SnipsNLUEngine
from snips_nlu.builtin_entities import BuiltinEntityParser
import io, json, os

def get_entity_value(entity, default_value=None):
  """Retrieve an entity value.
  
  :param entity: Dictionary wich contains results
  :type entity: dict
  :param default_value: Default value if not found
  :type default_value: any

  """

  return entity.get('value', entity.get('from', default_value))

class SnipsInterpreter(Interpreter):

  def __init__(self):
    super(SnipsInterpreter, self).__init__()

    self._meta = None
    self._lang = None
    self._engine = None
    self._entity_parser = None

  def metadata(self):
    return self._meta

  def lang(self):
    return self._lang

  def fit(self, training_file_path, trained_directory_path):
    filename, _ = os.path.splitext(os.path.basename(training_file_path))

    trained_path = os.path.join(trained_directory_path, '%s.trained.json' % filename)

    # TODO use checksums to decide if a training is needed

    with open(training_file_path) as f:
      training_data = json.load(f)
      self._lang = training_data['language']
      load_resources(self._lang)
    
    try:
      with open(trained_path) as f:
        self._engine = SnipsNLUEngine.from_dict(json.load(f))
    except FileNotFoundError:
      self._engine = SnipsNLUEngine()
      self._engine.fit(training_data)

      with open(trained_path, mode='w') as f:
        json.dump(self._engine.to_dict(), f)

    self._entity_parser = BuiltinEntityParser(self._lang)
    self._meta = { k: list(v.keys()) for k, v in self._engine._dataset_metadata['slot_name_mappings'].items() }

  def parse_entity(self, msg, intent, slot):
    # TODO check if builtin entity type for performance
    parsed = self._entity_parser.parse(msg)

    if parsed:
      return get_entity_value(parsed[0]['entity'], msg)

    return msg

  def parse(self, msg):
    parsed = self._engine.parse(msg)

    if parsed['intent'] == None:
      return []

    return [{
      'text': msg,
      'intent': parsed['intent']['intentName'],
      'slots': { s['slotName']: get_entity_value(s['value']) for s in parsed['slots'] }
    }]