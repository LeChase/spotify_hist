"""
Identifying unique songs by artist
"""

import pandas as pd 
import json

import collections


__scrobbles__ = 'downloads/gps56-2.csv'


class Unique:

    def __init__(self, scrobbles):

        self.scrobbles = scrobbles

        self.scrobbles_df = pd.read_csv(self.scrobbles, header = None, names = ['artist', 'album', 'song', 'datetime'])
        self.uniques = self.scrobbles_df.drop_duplicates(['artist', 'song'])[['artist', 'song']]

        # # pseudo code 
        # if json already exists:
        #     compare to existing
        #     get difference
        #     look up lyrics to these new records
        #     append these lyrics to existing database 
        # else:
        #     create json ('reset')
        #     find lyrics for all
        #     save to new database


    @staticmethod
    def reset(scrobbles_path, output_path):
        # recreate JSON file with unique artist/song combos from scrobbles input file
        scrobbles_df = pd.read_csv(scrobbles_path, header = None, names = ['artist', 'album', 'song', 'datetime'])
        uniques = scrobbles_df.drop_duplicates(['artist', 'song'])[['artist', 'song']]
        collected = uniques.groupby('artist')['song'].apply(list).reset_index(name = 'songs')
        d = collected.to_dict('records')
        d = {item['artist']: item['songs'] for item in d}

        with open(output_path, 'w') as f:
            json.dump(d, f)

    







if __name__ == '__main__':

    pass