import unittest
from unittest.mock import MagicMock
from atlas_sdk.pubsubs import PubSub
from atlas_sdk.topics import CHANNEL_CREATE_TOPIC, CHANNEL_DESTROY_TOPIC
from atlas.adapters.atlas_adapter import AtlasAdapter

class AtlasAdapterTests(unittest.TestCase):

  def test_subscriptions(self):
    pb = PubSub()
    adapter = AtlasAdapter(pb)

    adapter.on_channel_create = MagicMock()
    adapter.on_channel_destroy = MagicMock()

    adapter.activate()

    # Here I can only test with the + keyword since it's the MQTT broker which
    # interpret the + as a wildcard
    pb.on_received(CHANNEL_CREATE_TOPIC % '+', '{ "uid": 1337 }')

    adapter.on_channel_create.assert_called_once_with({
      'uid': 1337,
      'sid': '+',
    })
    adapter.on_channel_destroy.assert_not_called()

    pb.on_received(CHANNEL_DESTROY_TOPIC % '+')

    adapter.on_channel_destroy.assert_called_once_with({
      'sid': '+',
    })
