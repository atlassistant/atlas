from atlas import Atlas
from atlas.agent import AgentConfig
from atlas.client import Client
from atlas.interpreters.dummy_interpreter import DummyInterpreter
import logging

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    atlas = Atlas('localhost', DummyInterpreter())
    atlas.create_agent(AgentConfig('joe'))

    atlas.run()
