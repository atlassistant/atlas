from atlas_sdk.topics import ATLAS_REGISTRY_SKILL
from atlas_sdk.adapters import PubSubAdapter
from atlas_sdk.pubsubs.handlers import notset, json

class RegistryAdapter(PubSubAdapter):
  """Represents the adapter that should handle registry subscriptions.
  """

  def __init__(self, pubsub):
    super(RegistryAdapter, self).__init__(pubsub)

    self.on_register_skill = notset(self._logger)

    self._on_register_handler = None

  def activate(self):
    self._on_register_handler = json(self.on_register_skill)

    self._pubsub.subscribe(ATLAS_REGISTRY_SKILL, self._on_register_handler)

    super(RegistryAdapter, self).activate()

  def deactivate(self):
    self._pubsub.unsubscribe(ATLAS_REGISTRY_SKILL, self._on_register_handler)

    super(RegistryAdapter, self).deactivate()