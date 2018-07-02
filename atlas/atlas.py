from atlas_sdk.runnable import Runnable
from atlas_sdk.pubsubs import PubSub
from .adapters import AtlasAdapter
from .executor import Executor
import logging

class Atlas(Runnable):
  
  def __init__(self, adapter=None):
    self._logger = logging.getLogger(self.__class__.__name__.lower())
    self._pubsub = PubSub.from_config()
    self._executor = Executor.from_config()

    self._adapter = adapter or AtlasAdapter(self._pubsub)

  def run(self):
    self._logger.info('atlas is going up')
    self._adapter.activate()
    self._adapter.loading()

    self._executor.run()

    self._adapter.loaded()

    input()

  def cleanup(self):
    self._logger.info('atlas is going down')
    self._adapter.unloading()
    
    self._executor.cleanup()

    self._adapter.unloaded()
    self._adapter.deactivate()