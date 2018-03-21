from transitions import Machine
from atlas import Client
import json
import logging
import threading
import paho.mqtt.client as mqtt

class Interpreter:
    def parse(self, msg):
        return IntentData(msg, 'weather_forecast')

class Intent:
    def __init__(self, data):
        self.name = data['intent']
        self.slots = data['slots']

class IntentData:
    def __init__(self, text, name=None, slots={}):
        self.text = text
        self.name = name
        self.slots = slots

    def __str__(self):
        return 'IntentData %s - %s' % (self.name, self.slots)

class Agent:
    asleep = 'asleep'
    ask_prefix = 'ask__'

    def __init__(self, interpreter, intents, do=None):
        self._log = logging.getLogger('agent')
        self._interpreter = interpreter
        self._do = do
        self.reset()

        ask_states = list(set([slot for intent in intents for slot in intent.slots]))
        states = [Agent.asleep] + [i.name for i in intents] + [self._to_ask_transition(s) for s in ask_states]

        self._log.info('Registering states %s' % states)

        self._machine = Machine(self, states=states, send_event=True, initial=Agent.asleep)

        # Let's constructs transitions!
        ask_transitions_source = { k: [] for k in ask_states }

        for intent in intents:
            self._machine.add_transition(intent.name, ['asleep'] + [self._to_ask_transition(s) for s in intent.slots], intent.name, after='_call_intent')
            for slot in intent.slots:
                ask_transitions_source[slot].append(intent.name)

        for k, v in ask_transitions_source.items():
            ask_name = self._to_ask_transition(k)
            self._machine.add_transition(ask_name, v, ask_name)

    def _call_intent(self, event):
        self._log.debug('Calling intent handler "%s"' % event.transition.dest)
        if self._do:
            self._do(self._cur)

    def _to_ask_transition(self, param):
        return Agent.ask_prefix + param

    def _is_asking(self):
        return self.state.startswith(Agent.ask_prefix)

    def ask_sent_for(self, param):
        self._cur_param = param
        self.trigger(self._to_ask_transition(param))

    def process(self, msg):
        if self._is_asking():
            self._log.info('Setting %s to %s' % (self._cur_param, msg))
            self._cur.slots[self._cur_param] = msg
            self._cur_param = None
        else:
            self._cur = self._interpreter.parse(msg)

        if self._cur and self._cur.name:
            self.trigger(self._cur.name)

    def reset(self):
        self._cur = None
        self._cur_param = None

class Atlas:
    register_topic = '/atlas/intents/register'
    parse_topic = '/atlas/dialog/parse'
    ask_topic = '/atlas/dialog/ask'
    say_topic = '/atlas/dialog/say'

    def __init__(self, host, port=1883):
        self._log = logging.getLogger('atlas')
        self._client = mqtt.Client()
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        self._client.connect(host)

        self._new_intents = []
        self._intents = []
        self._agent = None
        self._check_agent_recompiling()

    def _check_agent_recompiling(self):
        self._log.debug('Checking if agent should recompiles')
        
        if len(self._new_intents) > 0:
            intents_to_register = list(self._new_intents)
            self._new_intents = []

            for intent in intents_to_register:
                self._log.info('Registering intent "%s" with %d slot(s)' % (intent.name, len(intent.slots)))
                self._intents.append(intent)

            self._agent = Agent(Interpreter(), self._intents, do=lambda x: self._client.publish('/atlas/intents/%s' % x.name, json.dumps({ k: v.decode('utf-8') for k, v in x.slots.items() })))

        t = threading.Timer(5, self._check_agent_recompiling)
        t.daemon = True
        t.start()

    def _on_connect(self, client, userdata, flags, rc):
        self._log.info('Connected to broker!')
        self._client.subscribe(Atlas.register_topic)
        self._client.subscribe(Atlas.ask_topic)
        self._client.subscribe(Atlas.parse_topic)
        self._client.subscribe(Atlas.say_topic)

    def _on_intent_register(self, data):
        self._new_intents.append(Intent(data))

    def _on_ask_topic(self, data):
        self._log.info('Requiring user inputs')
        if self._agent:
            self._agent.ask_sent_for(data['param'])

    def _on_parse_topic(self, msg):
        self._log.info('Parsing sentence %s' % msg)
        if self._agent:
            self._agent.process(msg)

    def run(self):
        self._client.loop_forever()

    def _on_message(self, client, userdata, msg):
        self._log.debug('Message received %s' % msg.topic)
        
        if msg.topic == Atlas.parse_topic:
            self._on_parse_topic(msg.payload)
        else:
            data = json.loads(msg.payload)

            if msg.topic == Atlas.register_topic:
                self._on_intent_register(data)
            elif msg.topic == Atlas.ask_topic:
                self._on_ask_topic(data)
            else:
                self._log.warn('No handler found for %s' % msg.topic)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    cli = Client()
    cli.subscribe('joe', '/atlas/dialog/parse', lambda x: print (x))

    cli.run('localhost')

    # atlas = Atlas('localhost')
    # atlas.run()

    # intents = [
    #     Intent({ 'intent': 'weather_forecast', 'slots': ['location', 'date'] }),
    #     Intent({ 'intent': 'reminder', 'slots': ['date', 'content'] }),
    # ]

    # agt = Agent(Interpreter(), intents, do=lambda x: print(x))
    # agt.process('donne moi la météo')
    # agt.ask_sent_for('location')
    # agt.process('Paris')
    # agt.ask_sent_for('date')
