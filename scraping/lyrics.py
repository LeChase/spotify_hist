"""
methods for pulling lyrics from Genius

uses Genius API
"""

from scraping import engine, keys

import lyricsgenius



class Lyrics(engine.Engine):

    genius = lyricsgenius.Genius(keys._genius_key, timeout = 60, sleep_time = 0)
    genius.verbose = False

    @classmethod
    def find_lyrics(cls, artist, song):
        try:
            song = cls.genius.search_song(' - '.join((artist, song)))
            return song.lyrics
        except (AttributeError, TypeError):
            # if the song cannot be found
            return cls.failed_result




if __name__ == '__main__':

    pass