"""
main script

"""

from scraper import Scraper

from lyrics import Lyrics
from spotify import Spotify



def main():

    # Scraper.main('lyrics', Lyrics.find_lyrics)

    Scraper.main('spotify', Spotify.get_features)




if __name__ == '__main__':

    main()