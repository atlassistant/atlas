from .version import __version__
from .atlas import Atlas
import argparse, sys

def add_common_arguments(parser):
  """Add common arguments to the given parser.

  Args:
    parser (ArgumentParser): Parser to complete

  """

  parser.add_argument('-c', '--config', help='Path to the configuration yaml file')
  parser.set_defaults(config='atlas.yml')

class AtlasCLI:
  
  def __init__(self):
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

  def run(self):
    parser = argparse.ArgumentParser(
      description='Run the atlas server'
    )

    add_common_arguments(parser)
    
    args = parser.parse_args(sys.argv[2:])

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
    parser = argparse.ArgumentParser(
      description='Computes interpreter accuracy'
    )

    add_common_arguments(parser)

    args = parser.parse_args(sys.argv[2:])

    print ('checking accuracy...')

def main():
  AtlasCLI()

if __name__ == '__main__':
  main()
