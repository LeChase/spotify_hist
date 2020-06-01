"""
Identifying unique songs by artist
"""

import pandas as pd 


__scrobbles__ = 'downloads/gps56-2.csv'


class Unique:
    """
    Class to extract unique artist/song combinations.
    Saves known combinations to json on disk for future reference.
    """

    @staticmethod
    def get_uniques():
        # returns a set of tuples containing artist, song combinations
        scrobbles_df = pd.read_csv(__scrobbles__, header = None, names = ['artist', 'album', 'song', 'datetime'])
        uniques_df = scrobbles_df.drop_duplicates(['artist', 'song'])[['artist', 'song']]
        return set(pd.MultiIndex.from_frame(uniques_df))

    @staticmethod
    def get_unique_artists():
        # returns set of unique artists from scrobbles 
        scrobbles_df = pd.read_csv(__scrobbles__, header = None, names = ['artist', 'album', 'song', 'datetime'])
        uniques_df = scrobbles_df.drop_duplicates(['artist'])['artist']
        return set(uniques_df)


    




if __name__ == '__main__':

    pass