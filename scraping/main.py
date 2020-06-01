"""
call this script to run scraping
"""


from scraping.scraper import Scraper

from scraping.lyrics import Lyrics
from scraping.spotify import Spotify



def main():

    # # get lyrics
    # lyric_scraper = Scraper('lyrics', Lyrics, Lyrics.find_lyrics)
    # lyric_scraper.main()

    # # get spotify features 
    # spotify_scraper = Scraper('spotify', Spotify, Spotify.get_features)
    # spotify_scraper.main()

    # get genres
    genre_scraper = Scraper('genre', Spotify, Spotify.get_genres)
    genre_scraper.main_genre()


if __name__ == '__main__':

    main()