import unittest
from unittest.mock import MagicMock, patch
from atlas.executor import Executor

class ExecutorTests(unittest.TestCase):
  
  @patch('glob.glob')
  def test_discover(self, glob_mock):
    glob_mock.return_value = ['a_directory/a_skill/atlas.yml']

    executor = Executor('a_directory')
    executor.discover()