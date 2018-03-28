from cmd import Cmd
import time, sys, json
from threading import Thread
import paho.mqtt.client as mqtt

class Prompt(Cmd):
    def __init__(self, client_id):
        super(Prompt, self).__init__()

        self.prompt = '> '
        self._client_id = client_id
        self._client = mqtt.Client()
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        self._client.connect('localhost')
        self._client.loop_start()

    def _on_connect(self, client, userdata, flags, rc):
        print ('Connected!')
        client.publish('atlas/%s/channel/create' % self._client_id)
        client.subscribe('atlas/%s/channel/ask' % self._client_id)
        client.subscribe('atlas/%s/channel/show' % self._client_id)

    def _on_message(self, client, userdata, msg):
        data = json.loads(msg.payload)

        print (data['text'])

    def do_destroy(self, arg):
        self._client.publish('atlas/%s/channel/destroy' % self._client_id)

    def default(self, arg):
        self._client.publish('atlas/%s/dialog/parse' % self._client_id, arg)

    def do_terminate(self, arg):
        self._client.publish('atlas/%s/dialog/terminate' % self._client_id)

    def do_exit(self, args):
        self._client.publish('atlas/%s/channel/destroy' % self._client_id)

        self._client.disconnect()
        self._client.loop_stop()

        raise SystemExit

if __name__ == '__main__':
    prompt = Prompt(sys.argv[1])
    prompt.cmdloop('Welcome %s!' % prompt._client_id)