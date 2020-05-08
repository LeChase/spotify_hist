"""
module containing class for initial scraping of data for artist/songs
"""

import os

import pandas as pd, numpy as np

import time, datetime

from uniques import Unique
from lyrics import Lyrics
from spotify import Spotify



class Scraper:

    def __init__(self):

        pass

    @staticmethod
    def main(output_type, func):
        # example working with lyrics for now 

        unique_scrobbles = Unique.get_uniques()


        # init json files
        if os.path.isfile('output/{}/completed.json'.format(output_type)):
            completed_df = pd.read_json("output/{}/completed.json".format(output_type), orient = 'table')
            completed_set = set(completed_df.index)
        else:
            completed_df = pd.DataFrame(index = pd.MultiIndex(levels = [[]]*2, codes = [[]]*2, names = ['artist', 'song']))
            completed_set = set()

        if os.path.isfile('output/{}/failed.json'.format(output_type)):
            failed_df = pd.read_json("output/{}/failed.json".format(output_type), orient = 'table')
            failed_set = set(failed_df.index)
        else:
            failed_df = pd.DataFrame(index = pd.MultiIndex(levels = [[]]*2, codes = [[]]*2, names = ['artist', 'song']))
            failed_set = set()

        if os.path.isfile('output/{}/yet.json'.format(output_type)):
            yet_df = pd.read_json("output/{}/yet.json".format(output_type), orient = 'table')
            yet_set = set(yet_df.index)
        else:
            yet_df = pd.DataFrame(index = pd.MultiIndex(levels = [[]]*2, codes = [[]]*2, names = ['artist', 'song']))
            yet_set = set()

        # remove completed and failed, artist/song combos from the set, and add those yet to be found
        unique_scrobbles -= (completed_set | failed_set)
        unique_scrobbles |= yet_set

        df = pd.DataFrame(index = pd.MultiIndex.from_tuples(unique_scrobbles, names =  ['artist', 'song']))
        df = df.sort_index()
        df[output_type] = np.nan

        # update the yet json file 
        df.to_json('output/{}/yet.json'.format(output_type), orient = 'table')

        df_copy = df.copy()

        time0 = time.time()
        n_songs = len(df)

        # iterate over the original 'yet' dataframe
        # copied df is used for editing
        try:
            for i, (artist, song) in enumerate(df.index, 1):
                percent_done = round(100*i/n_songs, 3)
                dt = round(time.time() - time0)
                time_remaining = round(dt/i*(n_songs-i))
                print('[[{} / {} ({}%)]]'.format(i, n_songs, percent_done), \
                        '[[{}s elapsed ({}s remaining)]]'.format(datetime.timedelta(seconds = dt), 
                                                                datetime.timedelta(seconds = time_remaining)), \
                        artist, '--', song)
                
                song_lyrics = func(artist, song)
                if song_lyrics == Lyrics.failed_result:
                    failed_df.at[(artist, song), output_type] = song_lyrics
                    failed_df.to_json("output/{}/failed.json".format(output_type), orient = 'table')
                else:
                    completed_df.at[(artist, song), output_type] = song_lyrics
                    completed_df.to_json("output/{}/completed.json".format(output_type), orient = 'table')
                df_copy = df_copy.drop((artist, song))
                df_copy.to_json("output/{}/yet.json".format(output_type), orient = 'table')

        except Exception as e:
            # update completed/failed/yet json files
            print(e)
            pass








if __name__ == '__main__':
    pass