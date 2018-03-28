from .client import Client, \
    PARSE_TOPIC, ASK_TOPIC, SHOW_TOPIC, TERMINATE_TOPIC, CHANNEL_ASK_TOPIC, CHANNEL_SHOW_TOPIC, INTENT_TOPIC
import json

class AgentClient(Client):
    """AgentClient is a simple facade between an Agent and the MQTT broker.

    It defines handler for all supported operations and exposes available publications.

    """

    def __init__(self, client_id):
        super(AgentClient, self).__init__(client_id)

        self.PARSE_TOPIC = PARSE_TOPIC % client_id
        self.ASK_TOPIC = ASK_TOPIC % client_id
        self.SHOW_TOPIC = SHOW_TOPIC % client_id
        self.TERMINATE_TOPIC = TERMINATE_TOPIC % client_id
        self.CHANNEL_ASK_TOPIC = CHANNEL_ASK_TOPIC % client_id
        self.CHANNEL_SHOW_TOPIC = CHANNEL_SHOW_TOPIC % client_id

        self.on_ask = self.handler_not_set
        self.on_parse = self.handler_not_set
        self.on_terminate = self.handler_not_set
        self.on_show = self.handler_not_set

    def on_connect(self, client, userdata, flags, rc):
        super(AgentClient, self).on_connect(client, userdata, flags, rc)

        self.subscribe_void(self.TERMINATE_TOPIC, self.on_terminate)
        self.subscribe_json(self.ASK_TOPIC, self.on_ask)
        self.subscribe_json(self.SHOW_TOPIC, self.on_show)
        self.subscribe_raw(self.PARSE_TOPIC, self.on_parse)

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

    def show(self, payload):
        """Show a message to the channel.

        :param payload: message
        :type payload: str

        """

        self.publish(self.CHANNEL_SHOW_TOPIC, payload)