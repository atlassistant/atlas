from atlas_sdk.adapters import PubSubAdapter
from atlas_sdk.topics import CHANNEL_CREATE_TOPIC, CHANNEL_DESTROY_TOPIC
from atlas_sdk.constants import SESSION_ID_KEY
from atlas_sdk.pubsubs.handlers import notset
from json import loads
import re

class AtlasAdapter(PubSubAdapter):
  
  def __init__(self, pubsub):
    super(AtlasAdapter, self).__init__(pubsub)

    self.on_channel_create = notset(self._logger)
    self.on_channel_destroy = notset(self._logger)

  def _extract_channel_id_and_trigger(self, handler, topic, payload):
    """Extract the channel id from the topic name and append it to the
    received data before calling the handler.

    Args:
      handler (callable): Handler to call with json data
      topic (str): Topic name triggered
      payload (str): Raw data received

    """

    channel_id = re.search('atlas/(.*?)/channel/.*', topic).group(1)

    try:
      data = loads(payload)
    except:
      data = {}

    data[SESSION_ID_KEY] = channel_id

    handler(data)

  def _on_channel_create(self, topic, payload):
    self._extract_channel_id_and_trigger(self.on_channel_create, topic, payload)

  def _on_channel_destroy(self, topic, payload):
    self._extract_channel_id_and_trigger(self.on_channel_destroy, topic, payload)

  def activate(self):
    self._pubsub.subscribe(CHANNEL_CREATE_TOPIC % '+', self._on_channel_create)
    self._pubsub.subscribe(CHANNEL_DESTROY_TOPIC % '+', self._on_channel_destroy)

    super(AtlasAdapter, self).activate()

  def deactivate(self):
    self._pubsub.unsubscribe(CHANNEL_CREATE_TOPIC % '+', self._on_channel_create)
    self._pubsub.unsubscribe(CHANNEL_DESTROY_TOPIC % '+', self._on_channel_destroy)

    super(AtlasAdapter, self).deactivate()