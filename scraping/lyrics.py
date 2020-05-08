"""
methods for pulling lyrics from Genius

uses Genius API
"""

from engine import Engine

import lyricsgenius



class Lyrics(Engine):

    _geinus_key = "UgvKlj9wHavgvBZScdTzfIKL2DKiIatIwPVV0M6JpEqm8YgIC_eJiQsYcsnmU2G-"
    genius = lyricsgenius.Genius(_geinus_key, timeout = 60, sleep_time = 0)
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