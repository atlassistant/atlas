from atlas_sdk.config import config
from atlas_sdk.runnable import Runnable
import json, logging, glob, os, yaml

class SkillData:
  """Represents a skill loaded by the executor.
  """

  def __init__(self, name, version):
    """Constructs a new skill data.

    Args:
      name (str): Name of the skill
      version (str): Version of the skill
      
    """

    self.name = name
    self.version = version

  def __str__(self):
    return '%s v%s' % (self.name, self.version)

class Executor(Runnable):
  """Executor executes skills placed into a specific directory.

  It makes it easy to run atlas and all skills at once.

  """

  def __init__(self, path):
    self._logger = logging.getLogger(self.__class__.__name__.lower())
    self._path = os.path.abspath(path)
    self._loaded_skills = []

  def discover(self):
    """Discovery launch the discovery process of this executor.

    It will try to find every skill in the given path.
    """

    self._logger.info('Discovering skills in %s' % self._path)

    for match in glob.glob(self._path + '/**/atlas.yml'):
      with open(match, mode='r', encoding='utf-8') as f:
        skill = SkillData(**yaml.load(f))
        self._loaded_skills.append(skill)        
        self._logger.info('Discovered skill "%s" at "%s"' % (skill, match))

  def run(self):
    self.discover()

    # self._logger.info('🚀 Started %s' % cmd)

  @classmethod
  def from_config(cls):
    """Constructs a new executor from the global config object.

    Returns:
      Executor: Executor ready to be used

    """

    return Executor(**config.get('executor', {}))