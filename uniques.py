"""
Identifying unique songs by artist
"""
import os

import time, datetime

import pandas as pd 
import json

import collections

import lyricsgenius

__scrobbles__ = 'downloads/gps56-2.csv'

__key__ = "UgvKlj9wHavgvBZScdTzfIKL2DKiIatIwPVV0M6JpEqm8YgIC_eJiQsYcsnmU2G-"

genius = lyricsgenius.Genius(__key__, timeout = 60, sleep_time = 0)
genius.verbose = False




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
        d = {artist: {song: '' for song in songs} for artist, songs in d.items()}
        return d

    def return_uniques(self, uniques_json):
        with open(uniques_json) as f:
            uniques_dict = json.load(f)
        return uniques_dict


    def fill_lyrics(self, json_file):
        with open(json_file) as f_read:
            d = json.load(f_read)
            n_songs = len(self.flatten_dict(d))
            time0 = time.time()
            i = 0
            for artist, songs in d.items():
                for song in songs.keys():
                    i += 1
                    percent_done = round(i/n_songs, 3)
                    dt = round(time.time() - time0, 2)
                    time_remaining = round(dt/i*(n_songs-i))
                    print('[[{} / {} ({}%)]]'.format(i, n_songs, percent_done), '[[{}s elapsed ({}s remaining)]]'.format(dt, datetime.timedelta(seconds = time_remaining)), artist, '--', song,)
                    d[artist][song] = self.find_lyrics(artist, song)
                    with open(json_file, 'w') as f_write:
                        json.dump(d, f_write)
        


    @staticmethod
    def find_lyrics(artist, song):
        try:
            song = genius.search_song(' - '.join((artist, song)))
            return song.lyrics
        except (AttributeError, TypeError):
            return 'NOT FOUND - AttributeError'
        except TypeError:
            return 'NOT FOUND - TypeError'


    @staticmethod
    def flatten_dict(d):
        # ungroups keys in nested dict
        return [(artist, song, lyrics) for artist, songs in d.items() for song, lyrics in songs.items()]


    @staticmethod
    def unflatten_dict(list_tups):
        # groups keys
        d = collections.defaultdict(dict)
        for artist, song, lyrics in list_tups:
            d[artist][song] = lyrics
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