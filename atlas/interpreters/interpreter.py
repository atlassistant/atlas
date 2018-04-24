from ..utils import generate_checksum
import os, logging

class InterpreterConfig():
  """Holds information about the interpreter configuration.
  """

  def __init__(self, type='atlas.interpreter.Interpreter', **kwargs):
    """Constructs a new interpreter config.
    
    :param type: Type of the interpreter
    :type type: str
    :param path: Path where to look for training files
    :type path: str
    :param trained_path: Path where are stored trained interpreter files
    :type trained_path: str

    """

    interpreter_parts = type.split('.')
    interpreter_klass = interpreter_parts[-1:][0]
    mod = __import__('.'.join(interpreter_parts[:-1]), fromlist=[interpreter_klass])

    self.interpreter_class = getattr(mod, interpreter_klass)
    self.kwargs = kwargs

  def construct(self):
    """Constructs a new interpreter related to this configuration instance.
    """

    return self.interpreter_class(**self.kwargs)

class Interpreter():
  """Interpreters convert natural language sentences to parsed structures used by atlas.

  There multiple open-source NLU libraries out there so it should be fairly easy to write a tiny abstraction
  for atlas.

  Interpreters should expose metadata since this is used by the Agent (ie. the dialog engine).

  """

  def __init__(self, name):
    """Constructs a new interpreter.

    :param name: Name of the interpreter
    :type name: str

    """

    self._log = logging.getLogger('atlas.interpreter.%s' % name)

  def checksum_match(self, data, checksum_file_path):
    """Checks if the checksum is the same between raw data and a checksum file.

    :param data: Raw data for which we want to compute the checksum
    :type data: str
    :param checksum_file_path: Path of the checksum file
    :type checksum_file_path: str
    :rtype: tuple

    """

    data_checksum = generate_checksum(data)

    self._log.debug('Checksum of raw data is %s' % data_checksum)

    try:
      with open(checksum_file_path) as f:
        file_checksum = f.read()

      self._log.debug('File checksum is %s' % file_checksum)

      return (data_checksum == file_checksum, data_checksum)
    except FileNotFoundError:
      self._log.debug('Checksum file not found at %s' % checksum_file_path)
      return (False, data_checksum)

  def lang(self):
    """Returns the interpreter language.

    :rtype: str

    """

    return 'en' # Default to en

  def metadata(self):
    """Gets interpreter metadata as a dict such as
    {
        'intent_name': ['slot_name', 'another_slot']
    }

    :rtype: dict

    """

    return {}

  def fit(self, training_file_path, trained_directory_path):
    """Train this interpreter.

    :param training_file_path: Path to the training file
    :type training_file_path: str
    :param trained_directory_path: Path to the trained folder where stuff should be put
    :type trained_directory_path: str
    
    """

    pass

  def parse(self, msg):
    """Parses an incoming message and converts it to a list of dict that represents intents and slots.

    If multiple values are found for the same slot, the interpreter should returns an array of values
    instead of a single one.

    Why a list of dict? Because you can return multiple intents for the same sentence if this is what
    the user asked for.

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
