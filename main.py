"""
main script

"""

from scraping.scraper import Scraper

from scraping.lyrics import Lyrics
from scraping.spotify import Spotify



def main():

    # get lyrics
    lyric_scraper = Scraper('lyrics', Lyrics, Lyrics.find_lyrics)
    lyric_scraper.main()

    # get spotify features 
    spotify_scraper = Scraper('spotify', Spotify, Spotify.get_features)
    spotify_scraper.main()



if __name__ == '__main__':

    main()