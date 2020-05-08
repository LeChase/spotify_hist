"""
methods for pulling data from Spotify

uses Spotify API via spotipy wrapper
"""

import os

from engine import Engine

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials



class Spotify(Engine):

    # setting env var in python
    os.environ['SPOTIPY_CLIENT_ID'] = '68be2578e21e439a92f5fcc00f9cfb6a'
    os.environ['SPOTIPY_CLIENT_SECRET'] = '45c1b5c64c8e4cbebc3d37c963e04bf9'

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



if __name__ == '__main__':

    pass