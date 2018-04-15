import os

class InterpreterConfig():
  """Holds information about the interpreter configuration.
  """

  def __init__(self, type, path):
    """Constructs a new interpreter config.
    
    :param type: Type of the interpreter
    :type type: str
    :param path: Path where to look for training files
    :type path: str

    """

    interpreter_parts = type.split('.')
    interpreter_klass = interpreter_parts[-1:][0]
    mod = __import__('.'.join(interpreter_parts[:-1]), fromlist=[interpreter_klass])

    self.interpreter_class = getattr(mod, interpreter_klass)
    self.path = os.path.abspath(path)

class Interpreter():
  """Interpreters convert natural language sentences to parsed structures used by atlas.

  There multiple open-source NLU libraries out there so it should be fairly easy to write a tiny abstraction
  for atlas.

  Interpreters should expose metadata since this is used by the Agent (ie. the dialog engine).

  """

  def __init__(self, lang):
    """Constructs a new interpreter.

    :param lang: Language of the interpreter
    :type lang: str

    """

    self.lang = lang

  def get_metadata(self):
    """Gets interpreter metadata as a dict such as
    {
        'intent_name': ['slot_name', 'another_slot']
    }

    :rtype: dict

    """

    return {}

  def fit(self, trained_file_path):
    """Train this interpreter.

    :param trained_file_path: Path to the training file
    :type trained_file_path: str
    
    """

    pass

  def parse(self, msg):
    """Parses an incoming message and converts it to a list of dict that represents intents and slots.

    :param msg: Message to parse
    :type msg: str

    :rtype: list

    """

    return []

  def parse_entity(self, msg, intent, slot):
    """Parses a message as an entity. This is useful when the skill is asking for mandatory parameters.

    The interpreter should translate the given value into the appropriate entity type.

    :param msg: Raw message to parse
    :type msg: str
    :param intent: Intent requested
    :type intent: str
    :param slot: Slot requested
    :type slot: str

    :rtype: str

    """

    return msg
