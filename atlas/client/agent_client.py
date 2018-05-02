from atlas_sdk.client import Client, \
  DIALOG_PARSE_TOPIC, DIALOG_ASK_TOPIC, DIALOG_SHOW_TOPIC, DIALOG_TERMINATE_TOPIC, \
  CHANNEL_ASK_TOPIC, CHANNEL_SHOW_TOPIC, INTENT_TOPIC, CHANNEL_TERMINATE_TOPIC, CHANNEL_WORK_TOPIC, \
  CHANNEL_CREATED_TOPIC, CHANNEL_DESTROYED_TOPIC
import json

class AgentClient(Client):
  """AgentClient is a simple facade between an Agent and the MQTT broker.

  It defines handler for all supported operations and exposes available publications.

  """

  def __init__(self, client_id, lang, on_ask=None, on_parse=None, on_terminate=None, on_show=None):
    """Constructs a new AgentClient.

    :param client_id: ID of the client manages by this agent
    :type client_id: str
    :param lang: Lang of the agent
    :type lang: str
    :param on_ask: Handler when a skill wants to ask something
    :type on_ask: callable
    :param on_parse: Handler when a channel wants to parse a message
    :type on_parse: callable
    :param on_terminate: Handler when a skill wants to terminate the dialog
    :type on_terminate: callable
    :param on_show: Handler when a skill wants to show something
    :type on_show: callable

    """

    super(AgentClient, self).__init__(name='agent.' + client_id) # Do not pass the client_id here!

    self._lang = lang

    self.DIALOG_PARSE_TOPIC = DIALOG_PARSE_TOPIC % client_id
    self.DIALOG_ASK_TOPIC = DIALOG_ASK_TOPIC % client_id
    self.DIALOG_SHOW_TOPIC = DIALOG_SHOW_TOPIC % client_id
    self.DIALOG_TERMINATE_TOPIC = DIALOG_TERMINATE_TOPIC % client_id
    self.CHANNEL_ASK_TOPIC = CHANNEL_ASK_TOPIC % client_id
    self.CHANNEL_SHOW_TOPIC = CHANNEL_SHOW_TOPIC % client_id
    self.CHANNEL_TERMINATE_TOPIC = CHANNEL_TERMINATE_TOPIC % client_id
    self.CHANNEL_WORK_TOPIC = CHANNEL_WORK_TOPIC % client_id
    self.CHANNEL_CREATED_TOPIC = CHANNEL_CREATED_TOPIC % client_id
    self.CHANNEL_DESTROYED_TOPIC = CHANNEL_DESTROYED_TOPIC % client_id

    self.on_ask = on_ask or self.handler_not_set
    self.on_parse = on_parse or self.handler_not_set
    self.on_terminate = on_terminate or self.handler_not_set
    self.on_show = on_show or self.handler_not_set

  def on_connect(self, client, userdata, flags, rc):
    super(AgentClient, self).on_connect(client, userdata, flags, rc)

    self.subscribe_json(self.DIALOG_TERMINATE_TOPIC, self.on_terminate)
    self.subscribe_json(self.DIALOG_ASK_TOPIC, self.on_ask)
    self.subscribe_json(self.DIALOG_SHOW_TOPIC, self.on_show)
    self.subscribe_raw(self.DIALOG_PARSE_TOPIC, self.on_parse)

    self.created()

  def intent(self, intent, data):
    """Publish a message to call the intent handler.

    :param intent: Name of the intent to call
    :type intent: str
    :param data: Data to send to the intent handler
    :type data: dict

    """

    self.publish(INTENT_TOPIC % intent, json.dumps(data))

  def created(self):
    """Inform the channel that an agent has been created for it.
    """

    self.publish(self.CHANNEL_CREATED_TOPIC, json.dumps({
      'lang': self._lang,
    }))

  def destroyed(self):
    """Inform the channel that the agent has been destroyed.
    """

    self.publish(self.CHANNEL_DESTROYED_TOPIC)

  def ask(self, payload):
    """Ask a question to the channel.

    :param payload: message
    :type payload: str

    """

    self.publish(self.CHANNEL_ASK_TOPIC, payload)

  def terminate(self):
    """Inform the channel that atlas has stopped its work.
    """

    self.publish(self.CHANNEL_TERMINATE_TOPIC)

  def work(self):
    """Inform the channel that a skill has been called so the work has started.

    It may be used to show an activity indicator.
    """

    self.publish(self.CHANNEL_WORK_TOPIC)

  def show(self, payload):
    """Show a message to the channel.

    :param payload: message
    :type payload: str

    """

    self.publish(self.CHANNEL_SHOW_TOPIC, payload)