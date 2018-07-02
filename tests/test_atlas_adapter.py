import unittest
from unittest.mock import MagicMock
from atlas_sdk.pubsubs import PubSub
from atlas_sdk.topics import CHANNEL_CREATE_TOPIC, CHANNEL_DESTROY_TOPIC, \
  ATLAS_STATUS_LOADING, ATLAS_STATUS_LOADED, ATLAS_STATUS_UNLOADING, ATLAS_STATUS_UNLOADED, \
  CHANNEL_CREATED_TOPIC, CHANNEL_DESTROYED_TOPIC
from atlas.adapters.atlas_adapter import AtlasAdapter
from atlas.version import __version__

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

  def test_publications(self):
    pb = PubSub()
    pb.publish = MagicMock()
    payload = '{"version": "%s"}' % __version__

    adapter = AtlasAdapter(pb)

    adapter.loading()
    pb.publish.assert_called_once_with(ATLAS_STATUS_LOADING, payload, ensure_delivery=True)
    pb.publish.reset_mock()

    adapter.unloading()
    pb.publish.assert_called_once_with(ATLAS_STATUS_UNLOADING, ensure_delivery=True)
    pb.publish.reset_mock()

    adapter.loaded()
    pb.publish.assert_called_once_with(ATLAS_STATUS_LOADED, payload, ensure_delivery=True)
    pb.publish.reset_mock()

    adapter.unloaded()
    pb.publish.assert_called_once_with(ATLAS_STATUS_UNLOADED, ensure_delivery=True)
    pb.publish.reset_mock()

    adapter.channel_created('test', '1337')
    pb.publish.assert_called_once_with(CHANNEL_CREATED_TOPIC, '{"sid": "test", "uid": "1337"}')
    pb.publish.reset_mock()

    adapter.channel_destroyed('test', '1337')
    pb.publish.assert_called_once_with(CHANNEL_DESTROYED_TOPIC, '{"sid": "test", "uid": "1337"}')
    pb.publish.reset_mock()