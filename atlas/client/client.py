from ..broker import BrokerConfig
import paho.mqtt.client as mqtt
import logging, json

TERMINATE_TOPIC = 'atlas/%s/dialog/terminate'
PARSE_TOPIC = 'atlas/%s/dialog/parse'
ASK_TOPIC = 'atlas/%s/dialog/ask'
SHOW_TOPIC = 'atlas/%s/dialog/show'

INTENT_TOPIC = 'atlas/intents/%s'

CHANNEL_ASK_TOPIC = 'atlas/%s/channel/ask'
CHANNEL_SHOW_TOPIC = 'atlas/%s/channel/show'
CHANNEL_CREATE_TOPIC = 'atlas/%s/channel/create'
CHANNEL_DESTROY_TOPIC = 'atlas/%s/channel/destroy'

class Client:
    """Client is an helper class to handler messages management.
    """

    def __init__(self, client_id=None):
        self.log = logging.getLogger('atlas.client.%s' % client_id)

        self._client = mqtt.Client(client_id)
        self._client.on_message = self.on_message
        self._client.on_connect = self.on_connect

        # Represents subscribed handlers for each type of subscriptions
        self._handlers = {
            'void': {},
            'raw': {},
            'json': {},
        }

    def handler_not_set(self, data=None, raw=None):
        self.log.warn('Handler not set correctly')

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

    def publish(self, topic, payload):
        """Publish a message to the given topic.

        You must transform the payload before calling this method.

        :param topic: Where to publish the message
        :type topic: str
        :param payload: Payload to publish
        :type payload: str

        """

        self._client.publish(topic, payload)

    def _subscribe(self, topic, ret, handler):
        """Inner subscribe which append the handler and subscribe to the topic.
        """

        self._handlers[ret][topic] = handler
        self._client.subscribe(topic)

    def subscribe_json(self, topic, handler):
        """Subscribe to a topic with the given handler.

        Using this subscription type, the payload will be loaded via json and gave to the handler.

        For convenience, the handler should also take a second parameter which is the raw payload.

        :param topic: Topic to subscribe to
        :type topic: str
        :param handler: Handler to call
        :type handler: callable

        """

        self._subscribe(topic, 'json', handler)

    def subscribe_void(self, topic, handler):
        """Subscribe to a topic with the given handler.

        Using this subscription type, the payload will be empty.

        :param topic: Topic to subscribe to
        :type topic: str
        :param handler: Handler to call
        :type handler: callable

        """

        self._subscribe(topic, 'void', handler)

    def subscribe_raw(self, topic, handler):
        """Subscribe to a topic with the given handler.

        Using this subscription type, the payload will be send as it.

        :param topic: Topic to subscribe to
        :type topic: str
        :param handler: Handler to call
        :type handler: callable

        """

        self._subscribe(topic, 'raw', handler)

    def on_connect(self, client, userdata, flags, rc):
        self.log.info('Connected to broker')

    def on_message(self, client, userdata, msg):
        self.log.debug('Received message %s - %s' % (msg.topic, msg.payload))

        handler = self._handlers['raw'].get(msg.topic)

        if handler:
            handler(msg.payload.decode('utf-8'))
        else:
            handler = self._handlers['void'].get(msg.topic)

            if handler:
                handler()
            else:
                handler = self._handlers['json'].get(msg.topic)

                if handler:
                    try:
                        data = json.loads(msg.payload)
                    except json.decoder.JSONDecodeError:
                        data = {}
                        self.log.warn('Could not decode payload %s' % msg.payload)

                    handler(data, msg.payload)
                else:
                    self.log.warn('No handler found for %s' % msg.topic)
