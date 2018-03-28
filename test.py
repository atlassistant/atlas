from atlas.agent import Agent, AgentConfig
from atlas.interpreters.dummy_interpreter import DummyInterpreter

agents = []

agents.append(Agent(DummyInterpreter(), AgentConfig('dummy', 'en')))
agents.append(Agent(DummyInterpreter(), AgentConfig('joe', 'en')))
agents.append(Agent(DummyInterpreter(), AgentConfig('doe', 'en')))

print (list(filter(lambda x: x.config.id == 'dummy', agents))[0])