from .atlas import Atlas, AtlasConfig
from .version import __version__
from .checker import Checker
from .web import Server
from .utils import generate_hash
from atlas_sdk import ChannelClient
import os, sys, argparse
from cmd import Cmd

# Monkey patch with eventlet
try:
  import eventlet # pylint: disable=E0401
  eventlet.monkey_patch()
except:
  pass

class Prompt(Cmd):
  def __init__(self, broker_config):
    super(Prompt, self).__init__()

    self.prompt = '> '
    self.uid = 'client'
    self.client_id = generate_hash()
    self.client = ChannelClient(self.client_id, self.uid, 
      on_ask=self.show_message, 
      on_show=self.show_message, 
      on_terminate=self.has_terminated,
      on_work=self.on_work
    )
    self.client.start(broker_config)

  def show_message(self, data, raw):
    print (data.get('text'))

  def on_work(self):
    print('-- work has started')
  
  def has_terminated(self):
    print ('-- intent has terminated')

  def default(self, arg):
    self.client.parse(arg)

  def do_exit(self, args):
    self.client.stop()

    raise SystemExit

def get_config():
  parser = argparse.ArgumentParser(description='Atlas CLI %s - An open-source assistant built for people' % __version__)

  parser.add_argument('-c', '--config', help='Path to the configuration yaml file')

  args = parser.parse_args(sys.argv[1:])

  config_path = os.path.abspath(args.config or 'atlas.yml')

  return AtlasConfig(config_path)

def client():
  prompt = Prompt(get_config().broker)
  prompt.cmdloop('Welcome!')

def web():
  serv = Server(get_config().server)
  
  try:
    serv.run()
  except Exception as e:
    print (e)

def check():
  check = Checker(get_config())
  check.run()

def main():
  atlas = Atlas(get_config())

  try:
    atlas.run()
  except Exception as e:
    print (e)
    atlas.cleanup()

if __name__ == '__main__':
  main()