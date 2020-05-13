"""
module containing class for initial scraping of data for artist/songs
"""

import os

import pandas as pd, numpy as np

import time, datetime

from analysis.uniques import Unique
from scraping.lyrics import Lyrics
from scraping.spotify import Spotify



class Scraper:

    def __init__(self, output_type, engine, scrape_func):

        self.engine = engine
        self.output_type = output_type
        self.scrape_func = scrape_func

        self.output_path = lambda f_type: "scraping/output/{}/{}.json".format(self.output_type, f_type)

    @staticmethod
    def get_from_json(json_path):
        if os.path.isfile(json_path):
            df = pd.read_json(json_path, orient = 'table')
            set_index = set(df.index)
        else:
            df = pd.DataFrame(index = pd.MultiIndex(levels = [[]]*2, codes = [[]]*2, names = ['artist', 'song']))
            set_index = set()
        return df, set_index

    def main(self):

        unique_scrobbles = Unique.get_uniques()

        completed_json = self.output_path('completed')
        failed_json = self.output_path('failed')
        yet_json = self.output_path('yet')

        completed_df, completed_set = self.get_from_json(completed_json)
        failed_df, failed_set = self.get_from_json(failed_json)
        yet_df, yet_set = self.get_from_json(yet_json)

        # remove completed and failed, artist/song combos from the set, and add those yet to be found
        unique_scrobbles -= (completed_set | failed_set)
        unique_scrobbles |= yet_set

        df = pd.DataFrame(index = pd.MultiIndex.from_tuples(unique_scrobbles, names =  ['artist', 'song']))
        df = df.sort_index()
        df[self.output_type] = np.nan

        # update the yet json file 
        df.to_json(yet_json, orient = 'table')

        df_copy = df.copy()

        time0 = time.time()
        n_songs = len(df_copy)

        # iterate over the original 'yet' dataframe
        # copied df is used for editing
        for i, (artist, song) in enumerate(df.index, 1):
            percent_done = round(100*i/n_songs, 3)
            dt = round(time.time() - time0)
            time_remaining = round(dt/i*(n_songs-i))
            print('[[{} / {} ({}%)]]'.format(i, n_songs, percent_done), \
                    '[[{}s elapsed ({}s remaining)]]'.format(datetime.timedelta(seconds = dt), 
                                                            datetime.timedelta(seconds = time_remaining)), \
                    artist, '--', song)
            
            output = self.scrape_func(artist, song)
            if output == self.engine.failed_result:
                failed_df.at[(artist, song), self.output_type] = output
                failed_df.to_json(failed_json, orient = 'table')
            else:
                # print(output)
                completed_df.at[(artist, song), self.output_type] = output
                completed_df.to_json(completed_json, orient = 'table')
            df_copy = df_copy.drop((artist, song))
            df_copy.to_json(yet_json, orient = 'table')









if __name__ == '__main__':
    pass