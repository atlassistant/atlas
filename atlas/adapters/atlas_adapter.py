from atlas_sdk.adapters import PubSubAdapter
from atlas_sdk.topics import CHANNEL_CREATE_TOPIC, CHANNEL_DESTROY_TOPIC, \
  ATLAS_STATUS_LOADING, ATLAS_STATUS_LOADED, ATLAS_STATUS_UNLOADING, ATLAS_STATUS_UNLOADED, \
  CHANNEL_CREATED_TOPIC, CHANNEL_DESTROYED_TOPIC
from atlas_sdk.constants import SESSION_ID_KEY, VERSION_KEY, USER_ID_KEY
from atlas_sdk.pubsubs.handlers import notset
from ..version import __version__
from json import loads, dumps
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

    # TODO may need some polish
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

  def _send_load_event_with_version(self, topic):
    self._pubsub.publish(topic, dumps({
      VERSION_KEY: __version__,
    }))

  def _send_channel_event(self, topic, id, uid):
    self._pubsub.publish(topic, dumps({
      SESSION_ID_KEY: id,
      USER_ID_KEY: uid,
    }))

  def loading(self):
    """Inform that atlas is loading.
    """

    self._send_load_event_with_version(ATLAS_STATUS_LOADING)

  def loaded(self):
    """Inform that atlas has loaded.
    """

    self._send_load_event_with_version(ATLAS_STATUS_LOADED)

  def unloading(self):
    """Inform that atlas is unloading.
    """

    self._pubsub.publish(ATLAS_STATUS_UNLOADING)

  def unloaded(self):
    """Inform that atlas has unloaded.
    """

    self._pubsub.publish(ATLAS_STATUS_UNLOADED)

  def channel_created(self, id, uid):
    """Inform the channel that an agent is ready for it.

    Args:
      id (str): Id of the channel
      uid (str): User Id of the channel

    """

    self._send_channel_event(CHANNEL_CREATED_TOPIC, id, uid)

  def channel_destroyed(self, id, uid):
    """Inform the channel that its agent has been destroyed.

    Args:
      id (str): Id of the channel
      uid (str): User Id of the channel
      
    """

    self._send_channel_event(CHANNEL_DESTROYED_TOPIC, id, uid)

  def activate(self):
    self._pubsub.subscribe(CHANNEL_CREATE_TOPIC % '+', self._on_channel_create)
    self._pubsub.subscribe(CHANNEL_DESTROY_TOPIC % '+', self._on_channel_destroy)

    super(AtlasAdapter, self).activate()

  def deactivate(self):
    self._pubsub.unsubscribe(CHANNEL_CREATE_TOPIC % '+', self._on_channel_create)
    self._pubsub.unsubscribe(CHANNEL_DESTROY_TOPIC % '+', self._on_channel_destroy)

    super(AtlasAdapter, self).deactivate()