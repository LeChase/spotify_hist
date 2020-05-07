"""
Identifying unique songs by artist
"""
import os

import pandas as pd 
import json

import collections


__scrobbles__ = 'downloads/gps56-2.csv'


class Unique:
    """
    Class to extract unique artist/song combinations.
    Saves known combinations to json on disk for future reference.
    """

    def __init__(self, scrobbles_csv = __scrobbles__):

        self.scrobbles_csv = scrobbles_csv


    def update_json(self, uniques_json):
        # if json already exists, add new uniques and rewrite
        # nothing is overwritten, only adding occurs
        if os.path.isfile(uniques_json):
            with open(uniques_json) as f:
                uniques_dict_old = json.load(f)
            uniques_dict_new = self.collect_uniques()
            total_uniques = self.merge_dicts(uniques_dict_new, uniques_dict_old)
        else:
            total_uniques = self.collect_uniques()

        with open(uniques_json, 'w') as f:
                json.dump(total_uniques, f)


    def collect_uniques(self):
        # given scrobbles, collect unique artist/song combos in dict
        scrobbles_df = pd.read_csv(self.scrobbles_csv, header = None, names = ['artist', 'album', 'song', 'datetime'])
        uniques_df = scrobbles_df.drop_duplicates(['artist', 'song'])[['artist', 'song']]
        collected = uniques_df.groupby('artist')['song'].apply(list).reset_index(name = 'songs')
        d = collected.to_dict('records')
        d = {item['artist']: item['songs'] for item in d}
        return d




    @staticmethod
    def flatten_dict(d):
        # ungroups keys
        return [(key, value) for key, values in d.items() for value in values]


    @staticmethod
    def unflatten_dict(list_tups):
        # groups keys
        d = collections.defaultdict(list)
        for key, val in list_tups:
            d[key].append(val)
        return dict(d)

    @staticmethod
    def merge_dicts(dict1, dict2):
        return {**dict1, **dict2}


    @staticmethod
    def dict_diff(dict_new, dict_old):
        # returns the items present in dict_new that are NOT present in dict_old
        return Unique.unflatten_dict(set(Unique.flatten_dict(dict_new)) - set(Unique.flatten_dict(dict_old)))







if __name__ == '__main__':

    pass