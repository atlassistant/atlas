from ..atlas import AtlasConfig, __version__
from ..web import Server
import argparse, sys, os

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Atlas Web %s' % __version__)

  parser.add_argument('-c', '--config', help='Path to the configuration yaml file')

  args = parser.parse_args(sys.argv[1:])

  config_path = os.path.abspath(args.config or 'atlas.yml')

  server = Server(AtlasConfig(config_path).server)

  try:
    server.run()
  except Exception as e:
    print (e)