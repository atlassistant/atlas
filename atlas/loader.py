from .interpreters import InterpreterConfig
import logging, os, configparser

DEFAULT_SECTION = 'DEFAULT'
DEFAULT_KEY = 'default'

class LoaderConfig():
  """Loads interpreters and env configurations from the file system.
  """

  def __init__(self, interpreter_config, training_path, trained_path, env_path):
    """Constructs a new LoaderConfig object.
    """

    self.interpreter_config = interpreter_config
    self.trained_path = trained_path
    self.training_path = training_path
    self.env_path = env_path

class Loader():
  """Loads interpreters and env configurations from the file system.
  """

  def __init__(self, config):
    """Instantiates a new Loader.

    :param config: Loader configuration
    :type config: LoaderConfig

    """

    self._log = logging.getLogger('atlas.loader')
    self._config = config
    self._envs = {}
    self._interpreters = {}

  def load(self):
    """Starts the loader!
    """

    self._load_envs()
    self._load_interpreters()

  def env_for(self, uid):
    """Retrieve environment variables for the given user id.

    :param uid: User id
    :type uid: str
    :rtype: dict

    """

    self._log.debug('Retrieving environment for %s' % uid)

    return self._envs.get(uid, self._envs.get(DEFAULT_KEY))

  def interpreter_for(self, uid):
    """Retrieve interpreter for the given user id.

    :param uid: User id
    :type uid: str
    :rtype: Interpreter

    """

    self._log.debug('Retrieving interpreter for %s' % uid)

    return self._interpreters.get(uid, self._interpreters.get(DEFAULT_KEY))

  def _load_envs(self):
    """Load user environments variables. Filenames should match the user ID.    
    """

    self._log.info('📝 Loading user envs from %s' % self._config.env_path)

    for env_file_path in os.listdir(self._config.env_path):
      with open(os.path.join(self._config.env_path, env_file_path)) as f:
        config_string = ('[%s]\n' % DEFAULT_SECTION) + f.read() # Add a default section since the file is a plain empty one
        config = configparser.ConfigParser()
        config.optionxform = str
        config.read_string(config_string)

        uid, _ = os.path.splitext(env_file_path)

        self._envs[uid] = dict(config[DEFAULT_SECTION])

    self._log.debug('Loaded %d env(s) files' % len(self._envs))

  def _load_interpreters(self,):
    """Load user interpreters. Filenames should match the user ID.
    """

    self._log.info('📝 Loading user interpreters from training files %s' % self._config.training_path)

    for training_file_path in os.listdir(self._config.training_path):
      uid, _ = os.path.splitext(training_file_path)

      interpreter = self._config.interpreter_config.construct()
      interpreter.fit(os.path.join(self._config.training_path, training_file_path), self._config.trained_path)

      self._interpreters[uid] = interpreter

    self._log.debug('Loaded %d interpreter(s)' % len(self._interpreters))