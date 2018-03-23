from .broker import BrokerConfig
import paho.mqtt.client as mqtt
import logging, json

class Client:
    """Client is a simple facade between an Agent and the MQTT broker.

    It defines handler for all supported operations and exposes available publications.

    """

    TERMINATE_TOPIC = 'atlas/%s/dialog/terminate'
    PARSE_TOPIC = 'atlas/%s/dialog/parse'
    ASK_TOPIC = 'atlas/%s/dialog/ask'
    SHOW_TOPIC = 'atlas/%s/dialog/show'
    
    INTENT_TOPIC = 'atlas/intents/%s'

    CHANNEL_ASK_TOPIC = 'atlas/%s/channel/ask'
    CHANNEL_SHOW_TOPIC = 'atlas/%s/channel/show'

    def __init__(self, client_id):
        self._log = logging.getLogger('atlas.client.%s' % client_id)

        self.PARSE_TOPIC = Client.PARSE_TOPIC % client_id
        self.ASK_TOPIC = Client.ASK_TOPIC % client_id
        self.SHOW_TOPIC = Client.SHOW_TOPIC % client_id
        self.TERMINATE_TOPIC = Client.TERMINATE_TOPIC % client_id
        self.CHANNEL_ASK_TOPIC = Client.CHANNEL_ASK_TOPIC % client_id
        self.CHANNEL_SHOW_TOPIC = Client.CHANNEL_SHOW_TOPIC % client_id

        self._client = mqtt.Client(client_id)
        self._client.on_message = self._on_message
        self._client.on_connect = self._on_connect

        self.on_ask = self._handler_not_set
        self.on_parse = self._handler_not_set
        self.on_terminate = self._handler_not_set
        self.on_show = self._handler_not_set

    def _handler_not_set(self, data=None, raw=None):
        self._log.warn('Handler not set correctly')

    def start(self, config):
        """Starts the broker client.

        :param config: Broker configuration
        :type config: BrokerConfig

        """

        self._client.connect(config.host, config.port)

        if config.username and config.password:
            self._client.username_pw_set(config.username, config.password)

        self._client.loop_start()

    def stop(self):
        """Stops the broker client.
        """
        
        self._client.loop_stop()

    def intent(self, intent, data):
        """Publish a message to call the intent handler.

        :param intent: Name of the intent to call
        :type intent: str
        :param data: Data to send to the intent handler
        :type data: dict

        """

        self._client.publish(Client.INTENT_TOPIC % intent, json.dumps(data))

    def ask(self, payload):
        """Ask a question to the channel.

        :param payload: message
        :type payload: str

        """

        self._client.publish(self.CHANNEL_ASK_TOPIC, payload)

    def show(self, payload):
        """Show a message to the channel.

        :param payload: message
        :type payload: str

        """

        self._client.publish(self.CHANNEL_SHOW_TOPIC, payload)

    def _on_connect(self, client, userdata, flags, rc):
        self._log.info('Connected to broker')
        self._client.subscribe(self.PARSE_TOPIC)
        self._client.subscribe(self.ASK_TOPIC)
        self._client.subscribe(self.SHOW_TOPIC)
        self._client.subscribe(self.TERMINATE_TOPIC)

    def _on_message(self, client, userdata, msg):
        self._log.debug('Received message %s - %s' % (msg.topic, msg.payload))

        # Some specific messages do not need the JSON load
        if msg.topic == self.PARSE_TOPIC:
            self.on_parse(msg.payload.decode('utf-8'))
        elif msg.topic == self.TERMINATE_TOPIC:
            self.on_terminate()
        else:
            # Else, it should be a JSON object
            try:
                data = json.loads(msg.payload)
            except json.decoder.JSONDecodeError:
                data = {}
                self._log.warn('Could not decode payload %s' % msg.payload)

            if msg.topic == self.ASK_TOPIC:
                self.on_ask(data, msg.payload)
            elif msg.topic == self.SHOW_TOPIC:
                self.on_show(data, msg.payload)
            else:
                self._log.warn('No handler found for %s' % msg.topic)