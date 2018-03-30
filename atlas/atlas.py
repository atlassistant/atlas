from .agent import Agent, AgentConfig
from .broker import BrokerConfig
from .version import __version__
from .web import Server, ServerConfig
from .interpreters import Interpreter
from .client import AtlasClient
from .executor import Executor, ExecutorConfig
import logging, yaml

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

        interp =  data.get('interpreter', {})
        interpreter_parts = interp.get('type', 'atlas.interpreter.Interpreter').split('.')
        interpreter_klass = interpreter_parts[-1:][0]
        mod = __import__('.'.join(interpreter_parts[:-1]), fromlist=[interpreter_klass])
        klass = getattr(mod, interpreter_klass)

        self.interpreter = klass(**interp)

        # Logging level

        logs = data.get('logs', {})
        log_level = logs.get('level', 'INFO')
        logging.basicConfig(level=getattr(logging, log_level))

        # Disable transitions logging
        transitions_logger = logging.getLogger('transitions')
        transitions_logger.setLevel(logging.WARNING)

        # Executor config

        self.executor = ExecutorConfig(**data.get('executor', {}))

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
        self._executor = Executor(self._config.executor)
        self._server = Server(self._config.server)
        self._client = AtlasClient(
            on_create=lambda id: self.create_agent(AgentConfig(id, self._config.interpreter.lang)),
            on_destroy=self.delete_agent)

    def find_agent(self, id):
        """Try to find an agent in this engine.

        :param id: Id of the agent
        :type id: str
        :rtype: Agent
        """

        agts = list(filter(lambda a: a.config.id == id, self._agents))[:1]

        if agts:
            return agts[0]
        else:
            return None

    def create_agent(self, config):
        """Creates a new agent attached to this engine.

        :param config: Configuration of the agent
        :type config: AgentConfig

        """

        if self.find_agent(config.id):
            self._log.info('Reusing existing agent %s' % config.id)
        else:
            self._log.info('🙌  Creating agent %s' % config.id)
            
            agt = Agent(self._config.interpreter, config)

            self._agents.append(agt)

            agt.client.start(self._config.broker)

    def delete_agent(self, id):
        """Deletes an agent from this engine.

        :param id: Id of the agent to remove
        :type id: str

        """

        agt = self.find_agent(id)

        if agt:
            self._log.info('🗑️  Deleting agent %s' % id)
            agt.cleanup()
            self._agents.remove(agt)
        else:
            self._log.info('No agent found %s' % id)

    def cleanup(self):
        """Cleanups this engine instance.
        """

        self._log.info('Exiting Atlas %s gracefuly' % __version__)

        for agt in self._agents:
            agt.cleanup()

        self._client.stop()
        self._executor.cleanup()

    def run(self):
        """Runs this instance!
        """

        self._log.info('Atlas %s is running, press any key to exit' % __version__)
        self._client.start(self._config.broker)
        self._executor.run()
        self._server.run()

        self.cleanup()