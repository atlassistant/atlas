from .version import __version__
from .atlas import Atlas
from atlas_sdk.config import load_from_yaml
import argparse, sys, os, logging

def add_common_arguments(parser):
  """Add common arguments to the given parser.

  Args:
    parser (ArgumentParser): Parser to complete

  """

  parser.add_argument('-c', '--config', help='Path to the configuration yaml file')
  parser.set_defaults(config='atlas.yml')

class AtlasCLI:
  
  def __init__(self):
    self._logger = logging.getLogger(self.__class__.__name__.lower())

    parser = argparse.ArgumentParser(
      description='atlas command line utility v%s' % __version__,
      usage='''atlas <command> [<args>]

Available commands:
  run         Run the atlas server
  accuracy    Check interpreter accuracy
'''
    )
    
    parser.add_argument('command', help='Subcommand to run')

    args = parser.parse_args(sys.argv[1:2])

    if not hasattr(self, args.command):
      print ('Command not found: %s' % args.command)
      parser.print_help()
      exit(1)

    getattr(self, args.command)()

  def _load_configuration(self, path):
    fullpath = os.path.abspath(path)

    try:
      load_from_yaml(fullpath)
      
      self._logger.info('Using configuration file: "%s"' % fullpath)
    except FileNotFoundError:
      self._logger.error('Could not load the configuration file: "%s"!' % fullpath)
      sys.exit(-1)

  def run(self):
    """Runs the atlas instance by reading the configuration file.
    """

    parser = argparse.ArgumentParser(
      description='Run the atlas server'
    )

    add_common_arguments(parser)
    
    args = parser.parse_args(sys.argv[2:])

    self._load_configuration(args.config)

    print ("""
      `.-:::::::-.`      
   `-::-..`````..-::-`   
  -::.```         `.::-  
 ::- `::-`           -::    
-::   .`              ::-   atlas v%s  Copyright (C) 2018  Julien LEICHER
::.           -:`     .::   This program comes with ABSOLUTELY NO WARRANTY.
::.    ``   `-:::.    .::   This is free software, and you are welcome to redistribute it
-::   .::-`.:::::::.`.::-   under certain conditions.
 :::-:::::::::::::--:::: 
  -:::::::::::::-:.-::-  
   `-:::::::::::::::-`   
      `.-:::::::-.`      
""" % __version__)

    with Atlas():
      pass

  def accuracy(self):
    """Computes engine accuracy and reports it.
    """

    parser = argparse.ArgumentParser(
      description='Computes interpreter accuracy'
    )

    add_common_arguments(parser)

    args = parser.parse_args(sys.argv[2:])
    self._load_configuration(args.config)

    print ('checking accuracy...')

def main():
  AtlasCLI()

if __name__ == '__main__':
  main()
