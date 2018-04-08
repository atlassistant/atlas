import logging
from .version import __version__
from .client import AgentClient
from .interpreters import Interpreter
from transitions import Machine, EventData, MachineError
from transitions.extensions.states import add_state_features, Timeout

@add_state_features(Timeout)
class AgentMachine(Machine):
    """Custom transitions Machine to add state features.
    """
    
    pass

class AgentConfig:
    def __init__(self, id, lang, ask_timeout=30):
        """Constructs a new configuration for the given parameters.

        :param id: Client ID used to represents the agent
        :type id: str
        :param lang: Language of the client
        :type lang: str
        :param ask_timeout: Timeout in seconds where the agent should go back to its asleep state when requiring user inputs
        :type ask_timeout: int

        """

        self.id = id
        self.lang = lang
        self.ask_timeout = ask_timeout

    def wrap(self, data):
        """Merge data with specific keys for this configuration.

        :param data: Data to merge
        :type data: dict

        """

        data.update({
            '__id': self.id,
            '__lang': self.lang,
            '__version': __version__,
        })

        return data

class Agent:
    """Agents are the core of the dialog engine of atlas.

    They maintain the state of a conversation and act as a relay between skills and channels. They are
    tied to a particular user or device and open a MQTT client themselve.

    """

    STATE_ASLEEP = 'asleep'
    PREFIX_ASK = 'ask__'

    def __init__(self, interpreter, config):
        """Creates a new agent.

        :param interpreter: Interpreter to be used
        :type interpreter: Interpreter
        :param config: Configuration to use
        :type config: AgentConfig

        """
        
        self.config = config

        self._log = logging.getLogger('atlas.agent.%s' % self.config.id)
        self._intent_queue = []

        self.interpreter = interpreter

        # Configure the client facade

        self.client = AgentClient(self.config.id,
            on_parse=self.parse,
            on_ask=self.ask,
            on_terminate=self.terminate,
            on_show=self.show)

        self.reset()

        # Constructs every possible transitions from interpreter metadata

        metadata = self.interpreter.get_metadata()

        ask_states = list(set([self._to_ask_state(slot) for meta in metadata.values() for slot in meta]))
        states = [Agent.STATE_ASLEEP] + list(metadata.keys()) + [{ 
            'name': o, 
            'timeout': self.config.ask_timeout, 
            'on_timeout': self._on_timeout 
        } for o in ask_states]

        self._log.info('Registering with states %s' % states)

        self._machine = AgentMachine(self, 
            states=states, 
            initial=Agent.STATE_ASLEEP, 
            send_event=True, 
            before_state_change=lambda e: self._log.info('⚡ %s: %s -> %s' % (e.event.name, e.transition.source, e.transition.dest) ))

        self._machine.add_transition(Agent.STATE_ASLEEP, '*', Agent.STATE_ASLEEP, after=self.reset)

        ask_transitions_source = { k: [] for k in ask_states }

        for intent, slots in metadata.items():
            converted_slots = [self._to_ask_state(s) for s in slots]
            self._machine.add_transition(intent, [Agent.STATE_ASLEEP] + converted_slots, intent, after=self._call_intent)

            for slot in converted_slots:
                ask_transitions_source[slot].append(intent)

        for k, v in ask_transitions_source.items():
            self._machine.add_transition(k, v, k, after=self._on_asked)

    def _to_ask_state(self, slot):
        """Converts to an ask state.

        :param slot: Slot to convert
        :type slot: str

        """

        return Agent.PREFIX_ASK + slot

    def reset(self, event=None):
        """Resets the current agent states.

        :param event: Optional event parameters
        :type event: EventData

        """

        self._cur_asked_param = None
        self._cur_intent = None
        self._cur_slots = {}

        self.client.terminate()

        self._process_next_intent()

    def go(self, trigger_name, **kwargs):
        """Safely call a trigger and catch errors

        :param trigger_name: Name of the trigger
        :type trigger_name: str

        """

        try:
            self.trigger(trigger_name, **kwargs) # pylint: disable=E1101
        except MachineError as err:
            self._log.error('Could not trigger "%s": %s' % (trigger_name, err))

    def _call_intent(self, event):
        """Call the intent with current slot values.

        :param event: Machine event
        :type event: EventData

        """

        # TODO when the discovery will be done, agents should know if an intent
        # could not be reached because no skill can answered to it so let the user
        # know!

        self._cur_intent = event.transition.dest
        
        data = self.config.wrap(self._cur_slots)

        self._log.debug('Calling intent "%s" with params %s' % (self._cur_intent, data))

        self.client.intent(self._cur_intent, data)

    def _on_asked(self, event):
        """Entered in ask state, save current asked param.

        :param event: Machine event
        :type event: EventData

        """

        self._cur_asked_param = event.transition.dest[len(Agent.PREFIX_ASK):]

        payload = event.kwargs.get('payload')

        self._log.debug('Asking request with payload %s' % payload)

        self.client.ask(payload)

    def _on_timeout(self, event):
        """Called when a state timeout has been reached.

        :param event: Machine event
        :type event: EventData

        """

        self.go(Agent.STATE_ASLEEP)

    def parse(self, msg):
        """Parse a raw message.

        :param msg: Message to parse
        :type msg: str

        """

        self._log.debug('Parsing "%s"' % msg)

        # TODO if intent is "cancel", returns to asleep
        # In the future we want every message coming after the cancellation and with a conversation_start_date to be dismissed

        # Start by checking if we are in a ask* state
        if self.state.startswith(Agent.PREFIX_ASK) and self._cur_asked_param: # pylint: disable=E1101
            self._cur_slots[self._cur_asked_param] = self.interpreter.parse_entity(msg, self._cur_intent, self._cur_asked_param)

            self.go(self._cur_intent)
        else:
            data = self.interpreter.parse(msg)

            # TODO if no intent was found, let it know

            self._intent_queue.extend(data)

            if self.state == Agent.STATE_ASLEEP: # pylint: disable=E1101
                self._process_next_intent()

            # TODO another intent is running, ask for confirmation? maybe?

    def _process_next_intent(self):
        """Process the intent queue if any left.
        """

        if len(self._intent_queue) > 0:
            intent = self._intent_queue.pop(0)
            self._cur_slots = intent['slots']
            self.go(intent['intent'])

    def ask(self, data, raw_msg):
        """Ask required by the skill intent.

        :param data: Data sent by the intent, it should at least contains the key "slot"
        :type data: dict
        :param raw_msg: Raw payload received
        :type raw_msg: str

        """

        self.go(self._to_ask_state(data['slot']), payload=raw_msg)

    def show(self, data, raw_msg):
        """Show simply pass message to the client channel.

        :param data: Data sent by the intent
        :type data: dict
        :param raw_msg: Raw payload received
        :type raw_msg: str

        """

        self.client.show(raw_msg)

    def terminate(self):
        """Terminates a dialog and returns to the asleep state.
        """

        self.go(Agent.STATE_ASLEEP)

    def cleanup(self):
        """Cleanup the agent.
        """

        # TODO Find a way to remove it cleanly
        # self._machine.remove_model(self)
        
        self.client.stop()

    def __str__(self):
        return 'Agent %s - %s' % (self.config.id, self.config.lang)
