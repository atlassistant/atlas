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

class ExecutorProcess:
    
    def __init__(self, skill):
        """Represents a single executing process for a skill backend.

        :param skill: Skill related to this process
        :type skill: Skill
        """

        self.skill = skill
        self._popen = None

    def run(self):
        """Runs this process.
        """

        self._popen = subprocess.Popen(self.skill.cmd, cwd=os.path.dirname(self.skill.path))

    def terminate(self):
        """Terminates this process.
        """

        if self._popen:
            self._popen.terminate()
            self._popen = None

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
        self._processes = []
        self._config = config

    def run(self):
        """Run discover skills and run them.
        """

        self._log.info('Running executor in: %s' % self._config.path)

        for skill_config_path in glob.glob(self._config.path + '/**/atlas.yml'):

            with open(skill_config_path) as f:
                skill_info = Skill(path=skill_config_path, **yaml.safe_load(f))

            self._log.info('Loaded %s' % skill_info)

            p = ExecutorProcess(skill_info)

            self._processes.append(p)

            p.run()

    def cleanup(self):
        """Stops spawned processes.
        """

        self._log.info('Stopping processes')

        for process in self._processes:
            process.terminate()
            self._log.info('Stopped %s' % process.skill)
