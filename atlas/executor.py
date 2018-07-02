from atlas_sdk.config import config
from atlas_sdk.runnable import Runnable
import json, logging, glob, os

class Executor(Runnable):
  """Executor executes skills placed into a specific directory.

  It makes it easy to run atlas and all skills at once.

  """

  def __init__(self, path):
    self._logger = logging.getLogger(self.__class__.__name__.lower())
    self._path = os.path.abspath(path)

  def run(self):
    self._logger.info('Discovering skills in %s' % self._path)

    for match in glob.glob(self._path + '/**/atlas.yml'):
      cmd = match

      self._logger.info('🚀 Started %s' % cmd)

  @classmethod
  def from_config(cls):
    """Constructs a new executor from the global config object.

    Returns:
      Executor: Executor ready to be used

    """

    return Executor(**config.get('executor', {}))