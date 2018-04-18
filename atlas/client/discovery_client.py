from atlas_sdk.client import Client, DISCOVERY_PING_TOPIC, DISCOVERY_PONG_TOPIC
from ..version import __version__
import json
from datetime import datetime

class DiscoveryClient(Client):

  def __init__(self, on_discovery=None):
    """Constructs a new DiscoveryClient.

    :param on_discovery: Handler when a discovery response has been retrieved
    :type on_discovery: callable

    """

    super(DiscoveryClient, self).__init__(name='discovery')

    self.on_discovery = on_discovery or self.handler_not_set
    self._started_at = datetime.utcnow()

  def on_connect(self, client, userdata, flags, rc):
    super(DiscoveryClient, self).on_connect(client, userdata, flags, rc)

    self.subscribe_json(DISCOVERY_PONG_TOPIC, self.on_discovery)

  def ping(self):
    """Launch a ping request for the discovery service.
    """

    self.publish(DISCOVERY_PING_TOPIC, json.dumps({
      'version': __version__,
      'started_at': self._started_at.isoformat(), # TODO format it like snips-nlu
    }))