"""
script to obtain lyrics using genius API
"""

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
    except AttributeError:
        return 'NOT FOUND'


def main():
    
    df = pd.read_csv(__scrobbles__, header = None, names = ['artist', 'album', 'song', 'datetime'])
    uniques = df.drop_duplicates(['artist', 'song'])[['artist', 'song']]
    
    print(len(uniques), 'unique artist & song combinations')
    print('starting:', time.ctime())
    uniques['lyrics'] = uniques.apply(get_lyrics, axis = 1)
    print('ending:', time.ctime())
    
    uniques.to_pickle(__output__)
    
    print('complete')



if __name__ == '__main__':
    
    main()