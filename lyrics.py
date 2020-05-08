"""
methods for pulling lyrics from Genius

uses Genius API
"""

import lyricsgenius


__key__ = "UgvKlj9wHavgvBZScdTzfIKL2DKiIatIwPVV0M6JpEqm8YgIC_eJiQsYcsnmU2G-"

genius = lyricsgenius.Genius(__key__, timeout = 60, sleep_time = 0)
genius.verbose = False



class Lyrics:

    @staticmethod
    def find_lyrics(artist, song):
        try:
            song = genius.search_song(' - '.join((artist, song)))
            return song.lyrics
        except (AttributeError, TypeError):
            return 'FAILED'




if __name__ == '__main__':

    pass