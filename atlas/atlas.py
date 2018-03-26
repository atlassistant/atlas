from .agent import Agent, AgentConfig
from .broker import BrokerConfig
from .version import __version__
from .interpreters import Interpreter
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

        broker = data.get('broker', {})

        self.broker = BrokerConfig(**broker)

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

    def create_agent(self, config):
        """Creates a new agent attached to this engine.

        :param config: Configuration of the agent
        :type config: AgentConfig

        """

        self._log.info('Creating agent')
        
        agt = Agent(self._config.interpreter, config)

        self._agents.append(agt)

        agt.client.start(self._config.broker)

    def cleanup(self):
        """Cleanups this engine instance.
        """

        self._log.info('Exiting Atlas %s gracefuly' % __version__)

        for agt in self._agents:
            agt.client.stop()

    def run(self):
        """Runs this instance!
        """

        self._log.info('Atlas %s is running, press any key to exit' % __version__)

        input()

        self.cleanup()