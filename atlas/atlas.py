from .agent import Agent
import logging

class Atlas:
    def __init__(self, host, interpreter):
        self._log = logging.getLogger('atlas:core')
        self._host = host
        self._interpreter = interpreter
        self._agents = []

    def create_agent(self, config):
        self._log.info('Creating agent')
        
        agt = Agent(self._interpreter, config)

        self._agents.append(agt)

        agt.client.start(self._host)

    def cleanup(self):
        self._log.info('Exiting gracefuly')

        for agt in self._agents:
            agt.client.stop()

    def run(self):
        self._log.info('Atlas is running, press any key to exit')

        input()

        self.cleanup()