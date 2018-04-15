from atlas_sdk.client import Client, \
  CHANNEL_CREATE_TOPIC, CHANNEL_DESTROY_TOPIC, CHANNEL_ASK_TOPIC, CHANNEL_SHOW_TOPIC, CHANNEL_TERMINATE_TOPIC, DIALOG_PARSE_TOPIC

class ChannelClient(Client):
  """A channel client should be used by client only. It leverages messages used by a channel.
  """
    
  def __init__(self, client_id, on_ask=None, on_show=None, on_terminate=None):
    """Constructs a new ChannelClient.
    
    :param client_id: Client ID to use
    :type client_id: str
    :param on_ask: Handler when the dialog engine wants the channel to ask something
    :type on_ask: callable
    :param on_show: Handler when the dialog engine wants the channel to show something
    :type on_show: callable
    :param on_terminate: Handler when the dialog engine wants the channel to terminate the dialog
    :type on_terminate: callable

    """

    super(ChannelClient, self).__init__(client_id, 'channel.' + client_id)

    self.CHANNEL_CREATE_TOPIC = CHANNEL_CREATE_TOPIC % client_id
    self.CHANNEL_DESTROY_TOPIC = CHANNEL_DESTROY_TOPIC % client_id
    self.CHANNEL_ASK_TOPIC = CHANNEL_ASK_TOPIC % client_id
    self.CHANNEL_SHOW_TOPIC = CHANNEL_SHOW_TOPIC % client_id
    self.CHANNEL_TERMINATE_TOPIC = CHANNEL_TERMINATE_TOPIC % client_id
    self.DIALOG_PARSE_TOPIC = DIALOG_PARSE_TOPIC % client_id

    self.on_ask = on_ask or self.handler_not_set
    self.on_show = on_show or self.handler_not_set
    self.on_terminate = on_terminate or self.handler_not_set

  def on_connect(self, client, userdata, flags, rc):
    super(ChannelClient, self).on_connect(client, userdata, flags, rc)

    self.create()

    self.subscribe_json(self.CHANNEL_ASK_TOPIC, self.on_ask)
    self.subscribe_json(self.CHANNEL_SHOW_TOPIC, self.on_show)
    self.subscribe_void(self.CHANNEL_TERMINATE_TOPIC, self.on_terminate)

  def stop(self):
    self.destroy()

    super(ChannelClient, self).stop()

  def create(self):
    """Inform the atlas engine of the channel creation.
    """
        
    self.publish(self.CHANNEL_CREATE_TOPIC)

  def destroy(self):
    """Inform the atlas engine that this channel is going down.
    """

    self.publish(self.CHANNEL_DESTROY_TOPIC)

  def parse(self, msg):
    """Ask the dialog engine to parse the given message.

    :param msg: Message to parse
    :type msg: str

    """

    self.publish(self.DIALOG_PARSE_TOPIC, msg)