from . import Client
import logging

class Atlas:
    def __init__(self):
        self._log = logging.getLogger('atlas:core')
        self._client = Client(on_intent_register=self._on_intent_registering)

    def _on_intent_registering(self, data):
        self._log.debug('Registering request for %s' % data)

    def run(self, host, port=1883):
        self._client.run(host, port)