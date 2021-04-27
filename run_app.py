#!/usr/bin/env python

import os
import sys
from argparse import ArgumentParser
from pyfiglet import figlet_format

from utils import getConfig
from api import searchTracks, InvalidTrackName
from analysis import getAlbumStats, getTopAlbums, updateAllStats


def printTopAlbums(topAlbums):
    """
    Prints the list of top albums
    :param topAlbums: a list of the top albums sorted in descending order of likelihood to match queries
    """
    print("\nMost Likely Albums")
    for i, albumStats in enumerate(topAlbums):
        albumStr = "'{}' by {}, released {} (Matched {} Queries, Max Similarity of {}, Max Popularity of {})".format(
            albumStats.albumName,
            albumStats.artists,
            albumStats.releaseDate,
            albumStats.nrQueriesMatched,
            albumStats.maxSimilarity,
            albumStats.maxPopularity,
        )
        # print(str(i + 1) + '. ' + str(albumStats))
        print(str(i + 1) + ". " + albumStr)
    print("\n")


def run(conf, debug=False):
    """
    Runs the app
    :param conf: the config to use
    :param debug: true = more stuff is printed
    """
    quitVal = conf.get("Misc", "quit_val")
    prompt = conf.get("Misc", "prompt")
    nrAlbums = int(conf.get("Misc", "nr_albums_to_display"))
    userInput = ""
    queryResults = {}
    allAlbumStats = {}

    while True:
        userInput = input(prompt + " ")

        if userInput == quitVal:
            break

        try:
            queryResults[userInput] = searchTracks(
                conf, userInput, removeSingles=False, debug=debug
            )
        except InvalidTrackName as e:
            print(e.message)
            continue

        if debug:
            print(
                "{} tracks in results for '{}'".format(
                    len(queryResults[userInput]), userInput
                )
            )

        # Update the collection of all album stats
        thisAlbumStats = getAlbumStats(userInput, queryResults[userInput], debug)
        allAlbumStats = updateAllStats(thisAlbumStats, userInput, allAlbumStats)

        topAlbums = getTopAlbums(allAlbumStats, nrAlbums)
        printTopAlbums(topAlbums)

        # if debug:
        #     i = 0
        #     for album, stats in allAlbumStats.items():
        #         if i < 3:
        #             print("Album: {}\nStats: {}".format(album, stats))
        #             i += 1
        #         else:
        #             break


if __name__ == "__main__":

    parser = ArgumentParser()

    parser.add_argument(
        "--debug",
        help="Debug mode - more verbose logging.",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-c",
        "--config",
        help="The config to use. Default is config/base.cfg",
        dest="config",
        # "The directory that this script lives in" + "config/base.cfg"
        default=os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "config/base.cfg"
        ),
    )

    args = parser.parse_args()

    print(figlet_format("Spotif... I Forgot.", font="roman"))
    print("Album Finder\n")
    print(
        "Enter songs from that album you kinda-sorta-but-don't-really remember, and see if the results jog your memory!\n"
    )

    conf = getConfig(args.config)

    if args.debug:
        print("*" * 10 + "\nDEBUG MODE\n" + "*" * 10)
        print("Args: ", args)

    run(conf, args.debug)
