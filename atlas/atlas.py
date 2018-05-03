from .agent import Agent
from .utils import find
from atlas_sdk.broker import BrokerConfig
from .discovery import Discovery, DiscoveryConfig
from .version import __version__
from .web import Server, ServerConfig
from .interpreters import Interpreter, InterpreterConfig
from .client import AtlasClient
from .executor import Executor, ExecutorConfig
from .loader import Loader, LoaderConfig
import logging, yaml, os, configparser

BROKER_CONFIG_KEY = 'broker'
INTERPRETER_CONFIG_KEY = 'interpreter'
LOADER_CONFIG_KEY = 'loader'
DISCOVERY_CONFIG_KEY = 'discovery'
EXECUTOR_CONFIG_KEY = 'executor'
SERVER_CONFIG_KEY = 'server'
LOGS_CONFIG_KEY = 'logs'

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

    os.chdir(os.path.dirname(path))

    # Broker configuration

    self.broker = BrokerConfig(**data.get(BROKER_CONFIG_KEY, {}))

    # Interpreter configuration

    self.interpreter =  InterpreterConfig(**data.get(INTERPRETER_CONFIG_KEY, {}))

    # Loader configuration

    self.loader = LoaderConfig(interpreter_config=self.interpreter, **data.get(LOADER_CONFIG_KEY, {}))

    # Discovery configuration

    self.discovery = DiscoveryConfig(**data.get(DISCOVERY_CONFIG_KEY, {}))

    # Logging level

    logs = data.get(LOGS_CONFIG_KEY, {})
    log_level = logs.get('level', 'INFO')
    logging.basicConfig(level=getattr(logging, log_level))

    # Executor config

    self.executor = ExecutorConfig(broker_config=self.broker, **data.get(EXECUTOR_CONFIG_KEY, {}))

    # Server config

    self.server = ServerConfig(broker_config=self.broker, **data.get(SERVER_CONFIG_KEY, {}))

    # Disable transitions and werkzeug logging
    logging.getLogger('transitions').setLevel(logging.WARNING)

    if not self.server.debug:
      logging.getLogger('werkzeug').setLevel(logging.WARNING)

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
    
    self._loader = Loader(self._config.loader)
    self._executor = Executor(self._config.executor)
    self._discovery = Discovery(self._config.discovery)
    self._server = Server(self._config.server)
    self._client = AtlasClient(
      on_create=lambda d: self.create_agent(d.get('id'), d.get('uid')),
      on_destroy=self.delete_agent
    )

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
          self._loader.interpreter_for(uid),
          self._loader.env_for(uid),
          validate_intent=lambda intent_name: self._discovery.skill_env_for_intent(intent_name)
        )

        self._agents.append(agt)

        agt.start(self._config.broker)
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

    self._log.info('Exiting atlas %s gracefuly' % __version__)

    self._discovery.cleanup()

    for agt in self._agents:
      agt.cleanup()

    self._client.stop()
    self._executor.cleanup()

  def run(self):
    """Runs this instance!
    """

    self._log.info("""

      `.-:::::::-.`      
   `-::-..`````..-::-`   
  -::.```         `.::-  
 ::- `::-`           -::    
-::   .`              ::-   atlas v%s  Copyright (C) 2018  Julien LEICHER
::.           -:`     .::   This program comes with ABSOLUTELY NO WARRANTY.
::.    ``   `-:::.    .::   This is free software, and you are welcome to redistribute it
-::   .::-`.:::::::.`.::-   under certain conditions.
 :::-:::::::::::::--:::: 
  -:::::::::::::-:.-::-  
   `-:::::::::::::::-`   
      `.-:::::::-.`      
""" % __version__)

    self._loader.load()
    self._client.start(self._config.broker)
    self._discovery.start(self._config.broker)
    self._executor.run()
    self._server.run()

    self.cleanup()