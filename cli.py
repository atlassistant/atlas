from atlas import Atlas
from atlas.agent import AgentConfig
from atlas.client import Client
from atlas.interpreters.snips_interpreter import SnipsInterpreter
import logging

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    atlas = Atlas(SnipsInterpreter())

    atlas.create_agent(AgentConfig('joe'))

    atlas.run()
