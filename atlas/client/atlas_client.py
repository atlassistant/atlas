from atlas_sdk.client import Client, \
  CHANNEL_CREATE_TOPIC, CHANNEL_DESTROY_TOPIC
import re

class AtlasClient(Client):
  """MQTT client used to create and destroy Agent upon channel creation / destruction.

  This one is special.

  """

  def __init__(self, on_create=None, on_destroy=None):
    """Constructs a new AtlasClient.

    :param on_create: Handler when a channel has been created
    :type on_create: callable
    :param on_destroy: Handler when a channel has been destroyed
    :type on_destroy: callable

    """

    super(AtlasClient, self).__init__(name='atlas')

    self.on_create = on_create or self.handler_not_set
    self.on_destroy = on_destroy or self.handler_not_set

    def _get_client_id_and_operation(self, topic):
      """Split the topic to get the client_id and the operation name.

      :param topic: Message topic
      :type topic: str
      :rtype: str
      
      """

      r = re.search('atlas/(.*?)/channel/(.*)', topic)

      return (r.group(1), r.group(2))

    def on_connect(self, client, userdata, flags, rc):
      super(AtlasClient, self).on_connect(client, userdata, flags, rc)

      client.subscribe(CHANNEL_CREATE_TOPIC % '+')
      client.subscribe(CHANNEL_DESTROY_TOPIC % '+')

    def on_message(self, client, userdata, msg):
      id, op = self._get_client_id_and_operation(msg.topic)

      if op == 'create':
        self.on_create(id)
      elif op == 'destroy':
        self.on_destroy(id)