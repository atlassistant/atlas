from .client import DiscoveryClient
from atlas_sdk import BrokerConfig
from .utils import find
from datetime import datetime, timedelta
import logging, threading

class Skill():
  """Represents a skill discovered by atlas.
  """

  def __init__(self, name, version, author=None, description=None, intents={}, env={}):
    """Constructs a new skill.
    
    :param name: Name of the skill
    :type name: str
    :param version: Version of the skill
    :type version: str
    :param author: Author of the skill
    :type author: str
    :param description: Optional description of the skill
    :type description: str
    :param intents: Intents supported by this skill with associated slots
    :type intents: dict
    :param env: Configuration variables with their types
    :type env: dict

    """

    self.name = name
    self.author = author
    self.version = version
    self.description = description
    self.intents = intents
    self.env = env
    
    self.heard_of()

  def heard_of(self):
    """Inform that this skill has just responded to the discovery challenge.
    """

    self.last_heard_of = datetime.utcnow()

  def has_timedout(self, date, timeout):
    return self.last_heard_of < date + timedelta(seconds = -timeout)

  def __str__(self):
    return 'Skill "%s"' % self.name

class DiscoveryConfig():
  """Represents the discovery configuration;
  """

  def __init__(self, interval=10, timeout=30):
    """Constructs a new configuration for the discovery service.

    :param interval: Polling interval in seconds
    :type interval: int
    :param timeout: Timeout in seconds, when a skill should be removed
    :type timeout: int

    """

    self.interval = interval
    self.timeout = timeout

class Discovery():
  """Represents the discovery service used to keep track of registered skills.
  """

  def __init__(self, config):
    """Constructs a new Discovery handler.

    :param config: Service configuration
    :type config: DiscoveryConfig
    """

    self._config = config
    self._skills = {}
    self._log = logging.getLogger('atlas.discovery')
    self._client = DiscoveryClient(on_discovery=self.process)

  def _ping(self):
    self._log.debug('Sending discovery request!')

    try:
      self._client.ping()
    except Exception as e:
      # May be because the client is not connected yet
      self._log.warn('Could not send a ping discovery: %s' % e)

    # Check for timeout skills

    now = datetime.utcnow()

    for k in list(self._skills.keys()):
      v = self._skills.get(k)

      if v.has_timedout(now, self._config.timeout):
        del self._skills[k]
        self._log.info('⏳ SKill %s has timed out, removed it' % k)

    self._thread = threading.Timer(self._config.interval, self._ping)
    self._thread.daemon = True
    self._thread.start()

  def process(self, skill_data, raw=None):
    """Process an incoming ping response for skill data.

    :param skill_data: Skill data received
    :type skill_data: dict
    :param raw: Raw message data
    :type raw: str

    """

    self._log.debug('Processing response from %s' % skill_data)

    name = skill_data.get('name')

    if name:
      skill = self._skills.get(name)

      if skill:
        self._log.debug('Skill %s already exists, updating' % name)
        skill.heard_of()
      else:
        self._skills[name] = Skill(**skill_data)
        self._log.info('🛠️ Added skill %s' % name)
    else:
      self._log.warn('No name defined, skipping the skill')

  def skill_env_for_intent(self, intent):
    """Try to retrieve a skill env associated with the intent name given.

    :param intent: Name of the intent
    :type intent: str
    :rtype: list

    """

    # TODO what if multiple skill can respond to the same intent with different env? :/

    skill = find(self._skills.values(), lambda s: s.intents.get(intent) != None)

    if skill:
      return skill.env.keys()

    return None

  def start(self, broker_config):
    """Starts the discovery service.

    :param broker_config: Broker configuration
    :type broker_config: BrokerConfig
    
    """

    self._client.start(broker_config)
    self._ping()

  def cleanup(self):
    """Cleanup discovery service stuff.
    """
    
    self._thread.cancel()
    self._client.stop()