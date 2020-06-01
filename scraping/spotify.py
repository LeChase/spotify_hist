"""
methods for pulling data from Spotify

uses Spotify API via spotipy wrapper
"""

import os

import pandas as pd

from scraping import engine, keys

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials



class Spotify(engine.Engine):

    # setting env var in python
    os.environ['SPOTIPY_CLIENT_ID'] = keys._SPOTIPY_CLIENT_ID
    os.environ['SPOTIPY_CLIENT_SECRET'] = keys._SPOTIPY_CLIENT_SECRET

    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    @classmethod
    def get_track_id(cls, artist, song):
        try:
            result = cls.sp.search(q = 'artist: {} track: {}'.format(artist, song),  type = 'track')
            return result['tracks']['items'][0]['id']
        except IndexError:
            # cannot find track
            return cls.failed_result

    @classmethod
    def get_features(cls, artist, song):
        ID = cls.get_track_id(artist, song)
        features = cls.sp.audio_features(ID)
        # features is a single element list ... 
        # not sure why, but i have to return this in order for scraper to be able to put into dataframe
        # checking features[0] since sometimes features = [None] if it failed 
        return features if features[0] else cls.failed_result

    @classmethod
    def get_genres(cls, artist, song = ''):
        try:
            result = cls.sp.search(q = 'artist: {}'.format(artist),  type = 'artist')
            return result['artists']['items'][0]['genres'][0]
        except IndexError:
            # cannot find track
            return cls.failed_result

    @classmethod
    def get_top50_features(cls):
        # the playlist URI should be static 
        top_50_URI = 'spotify:playlist:37i9dQZEVXbLRQDuF5jeBp'
        top_50_tracks = [item['track']['uri'] for item in cls.sp.playlist_tracks(top_50_URI)['items']]
        top_50_features = [cls.sp.audio_features(URI)[0] for URI in top_50_tracks]
        df_features = pd.DataFrame(top_50_features)
        df_features.to_json('scraping/output/top_50/features.json', orient = 'table')
        return df_features



if __name__ == '__main__':

    pass