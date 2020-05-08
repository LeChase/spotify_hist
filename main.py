"""
main script

"""

import uniques

from scraper import Scraper

from lyrics import Lyrics
from spotify import Spotify


# __json_path__ = "output/unique.json"
__json_path__ = "output/unique_spotify.json"


def main():

    # Scraper.main('lyrics', Lyrics.find_lyrics)

    Scraper.main('spotify', Spotify.get_features)




if __name__ == '__main__':

    main()