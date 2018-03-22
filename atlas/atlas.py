from .agent import Agent, AgentConfig
from .interpreters import Interpreter
import logging

class Atlas:
    """Entry point for this assistant system.

    Atlas manages agents (representing multiple users and devices) and dialog states.

    """

    def __init__(self, host, interpreter):
        """Constructs a new Atlas engine.
        
        :param host: Host of the message broker
        :type host: str
        :param interpreter: Interpreter implementation to use
        :type interpreter: Interpreter

        """

        self._log = logging.getLogger('atlas.core')
        self._host = host
        self._interpreter = interpreter
        self._agents = []

    def create_agent(self, config):
        """Creates a new agent attached to this engine.

        :param config: Configuration of the agent
        :type config: AgentConfig

        """

        self._log.info('Creating agent')
        
        agt = Agent(self._interpreter, config)

        self._agents.append(agt)

        agt.client.start(self._host)

    def cleanup(self):
        """Cleanups this engine instance.
        """

        self._log.info('Exiting gracefuly')

        for agt in self._agents:
            agt.client.stop()

    def run(self):
        """Runs this instance!
        """

        self._log.info('Atlas is running, press any key to exit')

        input()

        self.cleanup()