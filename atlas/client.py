import paho.mqtt.client as mqtt
import logging, json

class Client:
    register_topic = '/atlas/intents/register'
    parse_topic = '/atlas/dialog/parse'
    ask_topic = '/atlas/dialog/ask'
    say_topic = '/atlas/dialog/say'

    def __init__(self, on_intent_register=None):
        self._log = logging.getLogger('atlas:client')
        self._on_intent_register = on_intent_register
        self._client = mqtt.Client()
        self._client.on_message = self._on_message
        self._client.on_connect = self._on_connect
        self._subs = {}

    def run(self, host, port=1883):
        self._client.connect(host, port)
        self._client.loop_forever()

    def _on_connect(self, client, userdata, flags, rc):
        self._log.info('Connected to broker')
        self._client.subscribe(Client.register_topic)
        self._client.subscribe(Client.parse_topic)
        self._client.subscribe(Client.ask_topic)
        self._client.subscribe(Client.say_topic)

    def _on_message(self, client, userdata, msg):
        self._log.debug('Received message %s - %s' % (msg.topic, msg.payload))
        
        try:
            data = json.loads(msg.payload)
        except json.decoder.JSONDecodeError:
            data = {}
            self._log.warn('Could not decode payload %s' % msg.payload)

        # Special case for intent registering
        if msg.topic == Client.register_topic and self._on_intent_register:
            self._on_intent_register(data)

        sid = data.get('sid')

        if sid:
            subs = self._subs.get(msg.topic)
            handler = subs.get(sid)

            if handler:
                handler(data)
        else:
            self._log.warn('No sid found!')

    def subscribe(self, sid, topic, handler):
        self._log.info('Subscribing to "%s" for sid "%s"' % (topic, sid))
        top = self._subs.get(topic)

        if not top:
            self._subs[topic] = { sid: handler }
        else:
            self._subs[top][sid] = handler
    
    def unsubscribe(self, sid, topic):
        self._log.info('Unsubscribing from "%s" for sid "%s"' % (topic, sid))
        top = self._subs.get(topic)
        
        if top:
            top.pop(sid)