"""
script to obtain lyrics using genius API
"""

import os

import pandas as pd
import time

import lyricsgenius, json


__scrobbles__ = 'downloads/gps56-2.csv'
__key__ = "UgvKlj9wHavgvBZScdTzfIKL2DKiIatIwPVV0M6JpEqm8YgIC_eJiQsYcsnmU2G-"
__output__ = "lyrics/lyrics.pkl"


genius = lyricsgenius.Genius(__key__, timeout = 60, sleep_time = 2)
genius.verbose = False


def get_lyrics(row):
    try:
        song = genius.search_song(' - '.join((row.artist, row.song)))
        return song.lyrics
    except (AttributeError, TypeError):
        return 'NOT FOUND - AttributeError'
    except TypeError:
        return 'NOT FOUND - TypeError'



def main():
    
    df = pd.read_csv(__scrobbles__, header = None, names = ['artist', 'album', 'song', 'datetime'])
    uniques = df.drop_duplicates(['artist', 'song'])[['artist', 'song']]
    
    print(len(uniques), 'unique artist & song combinations')
    print('starting:', time.ctime())
    uniques['lyrics'] = uniques.apply(get_lyrics, axis = 1)
    print('ending:', time.ctime())
    
    uniques.to_pickle(__output__)
    
    print('complete')


class Lyrics:
    # class to gather lyrics on unique artist/song combos from scrobble history
    # incldues methods to update a previous lyric output with newer scrobble history

    def __init__(self, scrobbles, output = None):

        self.scrobbles = scrobbles
        self.output = output

        self.scrobbles_df = pd.read_csv(self.scrobbles, header = None, names = ['artist', 'album', 'song', 'datetime'])
        self.uniques = self.scrobbles_df.drop_duplicates(['artist', 'song'])[['artist', 'song']]
        if self._has_existing_output():
            self.output_df = pd.read_pickle(self.output)
        else:
            self.output_df = None

    def init_lyrics(self):
        # initial gather lyrics of unique artist/song combinations
        df = pd.read_csv(self.scrobbles, header = None, names = ['artist', 'album', 'song', 'datetime'])
        uniques = df.drop_duplicates(['artist', 'song'])[['artist', 'song']]
        
        print(len(uniques), 'unique artist & song combinations')
        print('starting:', time.ctime())
        uniques['lyrics'] = uniques.apply(get_lyrics, axis = 1)
        print('ending:', time.ctime())
        
        uniques.to_pickle(__output__)
        
        print('complete')

    @staticmethod
    def get_lyrics(row):
        try:
            song = genius.search_song(' - '.join((row.artist, row.song)))
            return song.lyrics
        except (AttributeError, TypeError):
            return 'NOT FOUND - AttributeError'
        except TypeError:
            return 'NOT FOUND - TypeError'


    def _check_existing_output(self):
        # read existing output and compare artists/songs to those in the latest scrobbles
        if self._has_existing_output():
            uniques = df.drop_duplicates(['artist', 'song'])[['artist', 'song']]
            


    def _has_existing_output(self):
        if self.output == None:
            return False
        else:
            return os.path.isfile(self.output)

    



if __name__ == '__main__':
    
    main()