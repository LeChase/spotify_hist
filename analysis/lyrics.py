"""
module with methods for lyrics analysis
"""

import numpy as np

import nltk
from nltk.corpus import stopwords

import re

stop_words = [item.replace("""'""", '') for item in stopwords.words('english')]
stop_words.extend(['im', 'like', 'yeah', 'get', 'oh', 'aint', 'got', 'wanna', 'want', 'ooh', 'ay', 'ayy', 'uh', 'cant'])
stopwords.extend(['intro', 'verse', 'outro', 'verse', 'chorus', 'hook')

re_compiled = re.compile(r'[^a-zA-Z0-9- ]')



class Lyrics:

    @staticmethod
    def get_most_common(lyrics):
        # make all lower 
        lyrics = lyrics.lower()
        # remove newline characters with a space
        lyrics = lyrics.replace('\n', ' ')
        # remove any non-alphanumeric via regex
        lyrics = re.sub(re_compiled, '', lyrics)

        try:
            tokens = [item for item in lyrics.split() if item not in stop_words] 
            freq = nltk.FreqDist(tokens)
            most_common = freq.most_common(1)[0][0]
            if most_common in ('instrumental', '-', '', ' '):
                return np.nan
            else:
                return most_common
        except IndexError:
            return np.nan



if __name__ == '__main__':

    pass