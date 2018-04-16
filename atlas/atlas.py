from .agent import Agent
from .utils import find
from atlas_sdk.broker import BrokerConfig
from .discovery import Discovery, DiscoveryConfig
from .version import __version__
from .web import Server, ServerConfig
from .interpreters import Interpreter, InterpreterConfig
from .client import AtlasClient
from .executor import Executor, ExecutorConfig
from .env import EnvConfig
import logging, yaml, os, configparser

class AtlasConfig:
  """Represents the global Atlas configuration.
  """

  def __init__(self, path):
    """Constructs a new AtlasConfig for the given yml filepath.

    :param path: Path to the YAML configuration file
    :type path: str

    """

    with open(path) as f:
      data = yaml.safe_load(f)

    # Broker configuration

    self.broker = BrokerConfig(**data.get('broker', {}))

    # Interpreter configuration

    self.interpreter =  InterpreterConfig(**data.get('interpreter', {
      'type': 'atlas.interpreter.Interpreter'
    }))

    # Env configuration

    self.env = EnvConfig(**data.get('env', {}))

    # Discovery configuration

    self.discovery = DiscoveryConfig(**data.get('discovery', {}))

    # Logging level

    logs = data.get('logs', {})
    log_level = logs.get('level', 'INFO')
    logging.basicConfig(level=getattr(logging, log_level))

    # Disable transitions logging
    transitions_logger = logging.getLogger('transitions')
    transitions_logger.setLevel(logging.WARNING)

    # Executor config

    self.executor = ExecutorConfig(broker_config=self.broker, **data.get('executor', {}))

    # Server config

    self.server = ServerConfig(broker_config=self.broker, **data.get('server', {}))

class Atlas:
  """Entry point for this assistant system.

  Atlas manages agents (representing multiple users and devices) and dialog states.

  """

  def __init__(self, config):
    """Constructs a new Atlas engine.
    
    :param config: Atlas configuration
    :type config: AtlasConfig

    """

    self._log = logging.getLogger('atlas.core')
    self._config = config
    self._agents = []
    
    self._envs = {}
    self._interpreters = {}

    self._load_envs(self._config.env)
    self._load_interpreters(self._config.interpreter)

    self._executor = Executor(self._config.executor)
    self._discovery = Discovery(self._config.discovery)
    self._server = Server(self._config.server)
    self._client = AtlasClient(
      on_create=lambda d: self.create_agent(d.get('id'), d.get('uid')),
      on_destroy=self.delete_agent
    )

  def _load_envs(self, config):
    """Load user environments variables. Filenames should match the user ID.
    
    :param config: Configuration to use
    :type config: EnvConfig
    
    """

    self._log.info('Loading user envs from %s' % config.path)

    for env_file_path in os.listdir(config.path):
      with open(os.path.join(config.path, env_file_path)) as f:
        config_string = '[DEFAULT]\n' + f.read() # Add a default section since the file is a plain empty one
        config = configparser.ConfigParser()
        config.optionxform = str
        config.read_string(config_string)

        uid, _ = os.path.splitext(env_file_path)

        self._envs[uid] = dict(config['DEFAULT'])

  def _load_interpreters(self, config):
    """Load user interpreters. Filenames should match the user ID.

    :param config: Configuration to use
    :type config: InterpreterConfig

    """

    self._log.info('Loading user interpreters from training files %s' % config.path)

    for training_file_path in os.listdir(config.path):
      uid, _ = os.path.splitext(training_file_path)

      interpreter = config.construct()
      interpreter.fit(os.path.join(config.path, training_file_path))

      self._interpreters[uid] = interpreter

  def find_agent(self, id):
    """Try to find an agent in this engine.

    :param id: Id of the agent
    :type id: str
    :rtype: Agent
    """

    return find(self._agents, lambda a: a.id == id)

  def create_agent(self, id, uid):
    """Creates a new agent attached to this engine.

    :param id: Channel id for the agent
    :type id: str
    :param uid: User ID for the agent, it determines which interpreter and envs would be loaded in the Agent
    :type uid: str

    """

    if id:
      if self.find_agent(id):
        self._log.info('Reusing existing agent %s for user %s' % (id, uid))
      else:
        self._log.info('🙌 Creating agent %s for user %s' % (id, uid))
              
        agt = Agent(
          id,
          uid,
          self._interpreters.get(uid, self._interpreters.get('default')),
          self._envs.get(uid, self._envs.get('default'))
        )

        self._agents.append(agt)

        agt.client.start(self._config.broker)
    else:
      self._log.error('No id defined, could not create the agent')

  def delete_agent(self, id):
    """Deletes an agent from this engine.

    :param id: Id of the agent to remove
    :type id: str

    """

    agt = self.find_agent(id)

    if agt:
      self._log.info('🗑️ Deleting agent %s' % id)
      agt.cleanup()
      self._agents.remove(agt)
    else:
      self._log.info('No agent found for %s' % id)

  def cleanup(self):
    """Cleanups this engine instance.
    """

    self._log.info('Exiting ATLAS %s gracefuly' % __version__)

    self._discovery.cleanup()

    for agt in self._agents:
      agt.cleanup()

    self._client.stop()
    self._executor.cleanup()

  def run(self):
    """Runs this instance!
    """

    self._log.info('ATLAS %s is running!' % __version__)
    self._client.start(self._config.broker)
    self._discovery.start(self._config.broker)
    self._executor.run()
    self._server.run()

    self.cleanup()