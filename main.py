"""
main script

"""

import uniques


__json_path__ = "output\unique.json"

def main():

    test = uniques.Unique()

    test.update_json(__json_path__)

    test.fill_lyrics(__json_path__)




if __name__ == '__main__':

    main()