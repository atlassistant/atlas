import logging
from .version import __version__
from .client import AgentClient
from atlas_sdk import BrokerConfig
from atlas_sdk.request import SID_KEY, UID_KEY, ENV_KEY, VERSION_KEY, LANG_KEY, CID_KEY
from .interpreters import Interpreter
from transitions import Machine, EventData, MachineError
from transitions.extensions.states import add_state_features, Timeout
import uuid

STATE_ASLEEP = 'asleep'
INTENT_CANCEL = 'cancel' # TODO handle it :)
PREFIX_ASK = 'ask__'

def to_ask_state(slot):
  """Converts to an ask state.

  :param slot: Slot to convert
  :type slot: str

  """

  return PREFIX_ASK + slot

def generate_hash():
  """Generates a random hash.

  :rtype: str
  """

  return uuid.uuid4().hex

@add_state_features(Timeout)
class AgentMachine(Machine):
  """Custom transitions Machine to add state features.
  """
  
  pass

class Agent:
  """Agents are the core of the dialog engine of atlas.

  They maintain the state of a conversation and act as a relay between skills and channels. They are
  tied to a particular user or device and open a MQTT client themselve.

  """

  def __init__(self, id, uid, interpreter, env, validate_intent=None, ask_timeout=30):
    """Creates a new agent.

    :param id: Channel id
    :type id: str
    :param uid: User ID
    :type uid: str
    :param interpreter: Interpreter to be used
    :type interpreter: Interpreter
    :param env: Configuration parameters for the user
    :type env: dict
    :param validate_intent: Handler to validate the user intent by checking if it's available, 
                            it will take the intent name and should returns a dict containing valid env 
                            variables if the skill exists or None if no skill could be found matching
                            that intent
    :type validate_intent: callable
    :param ask_timeout: Timeout when entering an ask state
    :type ask_timeout: int

    """

    self._log = logging.getLogger('atlas.agent.%s' % id)
    self._intent_queue = []

    self.validate_intent = validate_intent
    self.interpreter = interpreter
    self.env = env
    self.id = id
    self.uid = uid

    # Configure the client facade

    self._client = AgentClient(id,
      on_parse=self.parse,
      on_ask=self.ask,
      on_terminate=self._terminate_from_skill,
      on_show=self.show
    )

    self.reset()

    # Constructs every possible transitions from interpreter metadata

    metadata = self.interpreter.metadata()

    ask_states = list(set([to_ask_state(slot) for meta in metadata.values() for slot in meta]))
    states = [STATE_ASLEEP] + list(metadata.keys()) + [{ 
      'name': o, 
      'timeout': ask_timeout, 
      'on_timeout': self._on_timeout 
    } for o in ask_states]

    self._log.info('Registering with states %s' % states)

    self._machine = AgentMachine(self, 
      states=states, 
      initial=STATE_ASLEEP, 
      send_event=True, 
      before_state_change=lambda e: self._log.info('⚡ %s: %s -> %s' % (e.event.name, e.transition.source, e.transition.dest) )
    )

    self._machine.add_transition(STATE_ASLEEP, '*', STATE_ASLEEP, after=self.reset)

    ask_transitions_source = { k: [] for k in ask_states }

    for intent, slots in metadata.items():
      converted_slots = [to_ask_state(s) for s in slots]
      self._machine.add_transition(intent, [STATE_ASLEEP] + converted_slots, intent, after=self._call_intent)

      for slot in converted_slots:
        ask_transitions_source[slot].append(intent)

    for k, v in ask_transitions_source.items():
      self._machine.add_transition(k, v, k, after=self._on_asked)

  def reset(self, event=None):
    """Resets the current agent states.

    :param event: Optional event parameters
    :type event: EventData

    """

    self._cur_asked_param = None
    self._cur_intent = None
    self._cur_conversation_id = None
    self._cur_slots = {}

    self._client.terminate()

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

    self._cur_intent = event.transition.dest

    valid_keys = self.env.keys()

    # Try to validate if the intent could be reached

    if self.validate_intent:
      valid_keys = self.validate_intent(self._cur_intent)

      if valid_keys == None:
        self._log.warn('Intent %s could not be reached, skipping now' % self._cur_intent)
        return self.go(STATE_ASLEEP)

    self._cur_conversation_id = generate_hash()
    
    self._client.work()

    # Constructs the message payload
    
    data = {
      CID_KEY: self._cur_conversation_id,
      SID_KEY: self.id,
      UID_KEY: self.uid,
      LANG_KEY: self.interpreter.lang(),
      VERSION_KEY: __version__,
      ENV_KEY: { k: self.env[k] for k in valid_keys },
    }
    
    data.update(self._cur_slots)

    self._log.debug('Calling intent "%s" with params %s' % (self._cur_intent, data))

    self._client.intent(self._cur_intent, data)

  def _on_asked(self, event):
    """Entered in ask state, save current asked param.

    :param event: Machine event
    :type event: EventData

    """

    self._cur_asked_param = event.transition.dest[len(PREFIX_ASK):]

    payload = event.kwargs.get('payload')

    self._log.debug('Asking request with payload %s' % payload)

    self._client.ask(payload)

  def _on_timeout(self, event):
    """Called when a state timeout has been reached.

    :param event: Machine event
    :type event: EventData

    """

    self.go(STATE_ASLEEP)

  def parse(self, msg):
    """Parse a raw message.

    :param msg: Message to parse
    :type msg: str

    """

    self._log.debug('Parsing "%s"' % msg)

    # TODO if intent is "cancel", go to the cancel state immediately. This will generates a new
    # conversation id so old request will be dismissed if they tried to do something

    # Start by checking if we are in a ask* state
    if self.state.startswith(PREFIX_ASK) and self._cur_asked_param: # pylint: disable=E1101
      self._cur_slots[self._cur_asked_param] = self.interpreter.parse_entity(msg, self._cur_intent, self._cur_asked_param)

      self.go(self._cur_intent)
    else:
      data = self.interpreter.parse(msg)

      # TODO if no intent was found, let it know, maybe?

      self._intent_queue.extend(data)

      if self.state == STATE_ASLEEP: # pylint: disable=E1101
        self._process_next_intent()

      # TODO another intent is running, ask for confirmation? maybe?

  def _process_next_intent(self):
    """Process the intent queue if any left.
    """

    if len(self._intent_queue) > 0:
      intent = self._intent_queue.pop(0)
      self._cur_slots = intent['slots']
      self.go(intent['intent'])

  def _is_valid_request(self, data):
    """Checks if a request is valid in the current context.

    :param data: Request data
    :type data: dict

    """

    conversation_id = data.get(CID_KEY)

    if conversation_id == None:
      return False

    return conversation_id == self._cur_conversation_id

  def ask(self, data, raw_msg):
    """Ask required by the skill intent.

    :param data: Data sent by the intent, it should at least contains the key "slot"
    :type data: dict
    :param raw_msg: Raw payload received
    :type raw_msg: str

    """

    if self._is_valid_request(data):
      self.go(to_ask_state(data['slot']), payload=raw_msg)

  def show(self, data, raw_msg):
    """Show simply pass message to the client channel.

    :param data: Data sent by the intent
    :type data: dict
    :param raw_msg: Raw payload received
    :type raw_msg: str

    """

    if self._is_valid_request(data):
      self._client.show(raw_msg)

  def _terminate_from_skill(self, data, raw_msg):
    """Called by a skill when it has ended its work.

    :param data: Data sent by the intent
    :type data: dict
    :param raw_msg: Raw payload received
    :type raw_msg: str

    """

    if self._is_valid_request(data):
      self.terminate()

  def terminate(self):
    """Terminates a dialog and returns to the asleep state.
    """

    self.go(STATE_ASLEEP)

  def start(self, config):
    """Starts this agent.

    :param config: Broker configuration
    :type config: BrokerConfig

    """

    self._client.start(config)

  def cleanup(self):
    """Cleanup the agent.
    """

    # TODO Find a way to remove it cleanly
    # self._machine.remove_model(self)
    
    self._client.stop()

  def __str__(self):
    return 'Agent %s - %s' % (self.id, self.interpreter.lang)
