import os

class EnvConfig():
  """Represents configuration for the env data.
  """

  def __init__(self, path):
    """Constructs a new environment config.

    :param path: Path where env files are stored
    :type path: str

    """

    self.path = os.path.abspath(path)