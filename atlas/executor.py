from atlas_sdk.broker import BrokerConfig
import os, logging, glob, subprocess

class ExecutorConfig:
  """Configuration for an Executor.
  """

  def __init__(self, path, broker_config):
    """Constructs a new ExecutorConfig.
    
    :param path: Path of the skills directory
    :type path: str
    :param broker_config: Broker configuration used to start the skills on the specific message broker
    :type broker_config: BrokerConfig

    """

    self.path = os.path.abspath(path)
    self.broker = broker_config

class Executor:
  """Executor is a handy utility used to launch skill placed in a specific directory.

  It looks for directories with an "atlas" file containing the command to run and executes it with the configurated
  broker configuration.

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

    for p in glob.glob(self._config.path + '/**/atlas'):

      with open(p) as f:
        # Constructs the command line to run
        cmd = "%s -H %s -p %d" % (f.read(), self._config.broker.host, self._config.broker.port)

        if self._config.broker.is_secured():
          cmd += " -u %s:%s" % (self._config.broker.username, self._config.broker.password)

        process = subprocess.Popen(cmd, cwd=os.path.dirname(p), shell=True)
        self._processes.append(process)
        self._log.info('🚀 Started %s' % cmd)

  def cleanup(self):
    """Stops spawned processes.
    """

    self._log.info('Stopping processes')

    for process in self._processes:
      process.terminate()
      self._log.info('Stopped %s' % process.args)
