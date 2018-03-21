from atlas import Atlas
import logging

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    
    atlas = Atlas()
    atlas.run('localhost')
