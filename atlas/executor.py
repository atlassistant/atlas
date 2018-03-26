from .skill import Skill
import os, logging, glob, yaml, subprocess, threading

class ExecutorConfig:
    """Configuration for an Executor.
    """

    def __init__(self, path):
        """Constructs a new ExecutorConfig.
        
        :param path: Path of the skills directory
        :type path: str

        """

        self.path = os.path.abspath(path)

class Executor:
    """Executor launch atlas skills.

    With an executor, we can keep track of which skill backend are actually running.

    """

    def __init__(self, config):
        """Constructs a new executor for the given skills folder.
        
        :param config: Executor configuration
        :type config: ExecutorConfig

        """

        self._log = logging.getLogger('atlas.executor')
        self._config = config

    def run(self):
        self._log.info('Running executor in: %s' % self._config.path)

        for skill_config_path in glob.glob(self._config.path + '/**/atlas.yml'):
            with open(skill_config_path) as f:
                skill_info = Skill(**yaml.safe_load(f))

            self._log.info('Loaded %s %s by %s' % (skill_info.name, skill_info.version, skill_info.author))

            # t = threading.Thread(target=lambda: subprocess.run(skill_info.cmd.split(' '), cwd=os.path.dirname(skill_config_path)), daemon=True)
            # t.start()
