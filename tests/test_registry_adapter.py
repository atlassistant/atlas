import unittest
from unittest.mock import MagicMock
from atlas_sdk.pubsubs import PubSub
from atlas_sdk.topics import ATLAS_REGISTRY_SKILL
from atlas.adapters.registry_adapter import RegistryAdapter

class RegistryAdapterTests(unittest.TestCase):

  def test_subscriptions(self):
    pb = PubSub()
    adapter = RegistryAdapter(pb)

    adapter.on_register_skill = MagicMock()

    adapter.activate()

    pb.on_received(ATLAS_REGISTRY_SKILL, '{ "name": "A skill" }')

    adapter.on_register_skill.assert_called_once_with({ 'name': 'A skill' })
