from .loader import Loader
from .interpreters import Interpreter
from .atlas import AtlasConfig
import unittest, logging

class CheckerTest(unittest.TestCase):
  def __init__(self, interpreter):
    """Constructs a new test case for one interpreter.

    :param interpreter: Interpreter to test
    :type interpreter: Interpreter

    """

    super(CheckerTest, self).__init__()
    
    self._interpreter = interpreter

  def runTest(self):
    for data in self._interpreter.training():
      text = data['text']
      
      with self.subTest(text=text):
        expectedIntent = data['intent']
        r = self._interpreter.parse(text)

        self.assertEqual(1, len(r))
        self.assertEqual(expectedIntent, r[0]['intent'])

        # TODO may be add slot check support

class Checker:
  """Tiny helper to check interpreter accuracy. This makes it easy to know
  which intent may not be correctly inferred and so which one needs more training
  data.
  """

  def __init__(self, atlas_config):
    """Constructs a new checker instance.

    :param atlas_config: Atlas configuration
    :type atlas_config: AtlasConfig

    """

    self._log = logging.getLogger('atlas.checker')
    self._loader = Loader(atlas_config.loader)

  def run(self):
    """Runs the checker.
    """

    self._loader.load()

    suite = unittest.TestSuite()

    for uid, interp in self._loader._interpreters.items():
      suite.addTest(CheckerTest(interp))
      self._log.info('Added interpreter %s tests for uid %s' % (interp.name, uid))

    unittest.TextTestRunner().run(suite)