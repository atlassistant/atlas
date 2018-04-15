from atlas_sdk.client import Client, \
  DIALOG_PARSE_TOPIC, DIALOG_ASK_TOPIC, DIALOG_SHOW_TOPIC, DIALOG_TERMINATE_TOPIC, \
  CHANNEL_ASK_TOPIC, CHANNEL_SHOW_TOPIC, INTENT_TOPIC, CHANNEL_TERMINATE_TOPIC
import json

class AgentClient(Client):
  """AgentClient is a simple facade between an Agent and the MQTT broker.

  It defines handler for all supported operations and exposes available publications.

  """

  def __init__(self, client_id, on_ask=None, on_parse=None, on_terminate=None, on_show=None):
    """Constructs a new AgentClient.

    :param client_id: ID of the client manages by this agent
    :type client_id: str
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

    self.DIALOG_PARSE_TOPIC = DIALOG_PARSE_TOPIC % client_id
    self.DIALOG_ASK_TOPIC = DIALOG_ASK_TOPIC % client_id
    self.DIALOG_SHOW_TOPIC = DIALOG_SHOW_TOPIC % client_id
    self.DIALOG_TERMINATE_TOPIC = DIALOG_TERMINATE_TOPIC % client_id
    self.CHANNEL_ASK_TOPIC = CHANNEL_ASK_TOPIC % client_id
    self.CHANNEL_SHOW_TOPIC = CHANNEL_SHOW_TOPIC % client_id
    self.CHANNEL_TERMINATE_TOPIC = CHANNEL_TERMINATE_TOPIC % client_id

    self.on_ask = on_ask or self.handler_not_set
    self.on_parse = on_parse or self.handler_not_set
    self.on_terminate = on_terminate or self.handler_not_set
    self.on_show = on_show or self.handler_not_set

  def on_connect(self, client, userdata, flags, rc):
    super(AgentClient, self).on_connect(client, userdata, flags, rc)

    self.subscribe_void(self.DIALOG_TERMINATE_TOPIC, self.on_terminate)
    self.subscribe_json(self.DIALOG_ASK_TOPIC, self.on_ask)
    self.subscribe_json(self.DIALOG_SHOW_TOPIC, self.on_show)
    self.subscribe_raw(self.DIALOG_PARSE_TOPIC, self.on_parse)

  def intent(self, intent, data):
    """Publish a message to call the intent handler.

    :param intent: Name of the intent to call
    :type intent: str
    :param data: Data to send to the intent handler
    :type data: dict

    """

    self.publish(INTENT_TOPIC % intent, json.dumps(data))

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

  def show(self, payload):
    """Show a message to the channel.

    :param payload: message
    :type payload: str

    """

    self.publish(self.CHANNEL_SHOW_TOPIC, payload)