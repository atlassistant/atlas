from .. import Atlas, AtlasConfig, __version__
from ..agent import AgentConfig
import os, sys, argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Atlas CLI %s' % __version__)

    parser.add_argument('-c', '--config')

    args = parser.parse_args(sys.argv[1:])

    config_path = os.path.abspath(args.config or 'atlas.yml')

    atlas = Atlas(AtlasConfig(config_path))

    try:
        atlas.run()
    except Exception as e:
        print (e)
        atlas.cleanup()