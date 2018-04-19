from .. import Atlas, AtlasConfig, __version__
import os, sys, argparse

# Monkey patch with eventlet
try:
  import eventlet
  eventlet.monkey_patch()
except:
  pass

def main():
  parser = argparse.ArgumentParser(description='Atlas CLI %s - An open-source assistant built for people' % __version__)

  parser.add_argument('-c', '--config', help='Path to the configuration yaml file')

  args = parser.parse_args(sys.argv[1:])

  config_path = os.path.abspath(args.config or 'atlas.yml')

  atlas = Atlas(AtlasConfig(config_path))

  try:
    atlas.run()
  except Exception as e:
    print (e)
    atlas.cleanup()

if __name__ == '__main__':
  main()