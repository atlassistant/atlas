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
    
  def __init__(self, path, **kwargs):

    abspath = os.path.abspath(path)
    working_dir = os.path.dirname(abspath)
    filename, _ = os.path.splitext(os.path.basename(path))

    trained_path = os.path.join(working_dir, '%s.trained.json' % filename)

    # TODO use checksums to decide if a training is needed

    with open(abspath) as f:
      training_data = json.load(f)
      language_code = training_data['language']
      load_resources(language_code)
    
    try:
      with open(trained_path) as f:
        self._engine = SnipsNLUEngine.from_dict(json.load(f))
    except FileNotFoundError:
      self._engine = SnipsNLUEngine()
      self._engine.fit(training_data)

      with open(trained_path, mode='w') as f:
        json.dump(self._engine.to_dict(), f)

    super(SnipsInterpreter, self).__init__(language_code)

    self._entity_parser = BuiltinEntityParser(language_code)

  def get_metadata(self):
    meta = self._engine._dataset_metadata['slot_name_mappings']

    return { k: list(v.keys()) for k, v in meta.items() }

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