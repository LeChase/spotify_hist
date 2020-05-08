"""
methods for pulling data from Spotify

uses Spotify API via spotipy wrapper
"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# setting env var in python
import os
os.environ['SPOTIPY_CLIENT_ID'] = '68be2578e21e439a92f5fcc00f9cfb6a'
os.environ['SPOTIPY_CLIENT_SECRET'] = '45c1b5c64c8e4cbebc3d37c963e04bf9'

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())


class Spotify:

    failed_result = 'FAILED'

    @classmethod
    def get_track_id(cls, artist, song):
        try:
            result = sp.search(q = 'artist: {} track: {}'.format(artist, song),  type = 'track')
            return result['tracks']['items'][0]['id']
        except IndexError:
            # cannot find track
            return cls.failed_result

    @staticmethod
    def get_features(artist, song):
        ID = Spotify.get_track_id(artist, song)
        return sp.audio_features(ID)



if __name__ == '__main__':

    pass