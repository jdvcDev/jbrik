#!/usr/bin/env python2

'''
shamelessly taken from https://github.com/dwalton76/rubiks-cube-tracker
credit to https://github.com/dwalton76

usage:

python rubiks-cube-tracker.py --filename resource/jbrik_img


python rubiks-cube-tracker.py --filename resource/rubiks-side-B.png
python rubiks-cube-tracker.py --filename resource/jbrik_img2/rubiks-side-U.png
2020-01-15 20:36:35,664          trackerlib.py     INFO: Analyze resource/rubiks-side-B.png
{"1": [193, 12, 26], "2": [253, 198, 186], "3": [44, 253, 225], "4": [252, 171, 163], "5": [19, 151, 253], "6": [46, 254, 231], "7": [20, 136, 252], "8": [207, 15, 39], "9": [246, 252, 249]}


{"1": [137, 106, 103], "2": [145, 48, 49], "3": [135, 103, 60], "4": [136, 105, 60], "5": [140, 105, 103], "6": [24, 52, 24], "7": [28, 52, 26], "8": [133, 40, 40], "9": [20, 34, 50]}
{"1": [133, 105, 68], "2": [21, 36, 57], "3": [134, 104, 65], "4": [136, 107, 111], "5": [137, 51, 55], "6": [137, 105, 110], "7": [125, 99, 61], "8": [20, 49, 25], "9": [131, 99, 103]}
{"1": [72, 16, 17], "2": [146, 48, 48], "3": [72, 15, 15], "4": [28, 54, 25], "5": [138, 104, 60], "6": [75, 17, 18], "7": [66, 16, 15], "8": [12, 29, 46], "9": [20, 33, 49]}
{"1": [27, 54, 28], "2": [142, 108, 109], "3": [140, 44, 47], "4": [137, 105, 62], "5": [77, 21, 22], "6": [73, 17, 18], "7": [134, 43, 45], "8": [129, 98, 57], "9": [28, 53, 28]}
{"1": [68, 17, 16], "2": [19, 35, 52], "3": [140, 107, 102], "4": [132, 104, 56], "5": [32, 56, 29], "6": [27, 55, 26], "7": [129, 42, 41], "8": [67, 15, 14], "9": [19, 34, 50]}
{"1": [166, 98, 64], "2": [95, 5, 10], "3": [43, 63, 13], "4": [166, 98, 64], "5": [15, 29, 28], "6": [22, 32, 30], "7": [26, 31, 27], "8": [157, 13, 24], "9": [161, 16, 27]}




{"1": [137, 106, 103],
"2": [145, 48, 49],
"3": [135, 103, 60],
"4": [136, 105, 60],
"5": [140, 105, 103],
"6": [24, 52, 24],
"7": [28, 52, 26],
"8": [133, 40, 40],
"9": [20, 34, 50]
"10": [133, 105, 68],
"11": [21, 36, 57],
"12": [134, 104, 65],
"13": [136, 107, 111],
"14": [137, 51, 55],
"15": [137, 105, 110],
"16": [125, 99, 61],
"17": [20, 49, 25],
"18": [131, 99, 103],
"19": [72, 16, 17],
"20": [146, 48, 48],
"21": [72, 15, 15],
"22": [28, 54, 25],
"23": [138, 104, 60],
"24": [75, 17, 18],
"25": [66, 16, 15],
"26": [12, 29, 46],
"27": [20, 33, 49],
"28": [27, 54, 28],
"29": [142, 108, 109],
"30": [140, 44, 47],
"31": [137, 105, 62],
"32": [77, 21, 22],
"33": [73, 17, 18],
"34": [134, 43, 45],
"35": [129, 98, 57],
"36": [28, 53, 28],
"37": [68, 17, 16],
"38": [19, 35, 52],
"39": [140, 107, 102],
"40": [132, 104, 56],
"41": [32, 56, 29],
"42": [27, 55, 26],
"43": [129, 42, 41],
"44": [67, 15, 14],
"45": [19, 34, 50],
"46": [166, 98, 64],
"47": [95, 5, 10],
"48": [43, 63, 13],
"49": [166, 98, 64],
"50": [15, 29, 28],
"51": [22, 32, 30],
"52": [26, 31, 27],
"53": [157, 13, 24],
"54": [161, 16, 27]}




'''

from trackerlib import RubiksVideo, RubiksImage, merge_two_dicts
from math import sqrt
import argparse
import json
import logging
import os
import sys


def convert_keys_to_int(dict_to_convert):
    result = {}

    for (key, value) in dict_to_convert.items():
        result[int(key)] = value

    return result


# Logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(filename)22s %(levelname)8s: %(message)s"
)
log = logging.getLogger(__name__)

# Color the errors and warnings in red
logging.addLevelName(
    logging.ERROR, "\033[91m   %s\033[0m" % logging.getLevelName(logging.ERROR)
)
logging.addLevelName(
    logging.WARNING, "\033[91m %s\033[0m" % logging.getLevelName(logging.WARNING)
)

# Command line args
parser = argparse.ArgumentParser("Rubiks Square Extractor")
parser.add_argument(
    "-d", "--directory", type=str, help="Directory of images to examine"
)
parser.add_argument("-f", "--filename", type=str, help="Image to examine")
parser.add_argument("--index", type=int, default=0, help="side index number (0-5)")
parser.add_argument(
    "--name", type=str, default=None, help="side name (U, L, F, R, B, D)"
)
parser.add_argument("--debug", action="store_true", help="Enable debugs")
parser.add_argument(
    "-w", "--webcam", type=int, default=None, help="webcam to use...0, 1, etc"
)
args = parser.parse_args()

if args.webcam is None and args.directory is None and args.filename is None:
    log.error("args.directory and args.filename are None")
    sys.exit(1)

if args.debug:
    log.setLevel(logging.DEBUG)

if args.webcam is not None:
    rvid = RubiksVideo(args.webcam)
    rvid.analyze_webcam()

elif args.filename:
    log.setLevel(logging.DEBUG)
    rimg = RubiksImage(args.index, args.name, args.debug)
    rimg.analyze_file(args.filename)
    print(json.dumps(rimg.data, sort_keys=True))

else:
    data = {}

    if not os.path.isdir(args.directory):
        sys.stderr.write("ERROR: directory %s does not exist\n" % args.directory)
        sys.exit(1)
    cube_size = None
    cube_size = None

    for (side_index, side_name) in enumerate(("U", "L", "F", "R", "B", "D")):
        filename = os.path.join(args.directory, "rubiks-side-%s.png" % side_name)

        if os.path.exists(filename):
            # log.info("filename %s, side_index %s, side_name %s" % (filename, side_index, side_name))

            # log.info("filename %s, side_index %s, side_name %s" % (filename, side_index, side_name))
            rimg = RubiksImage(side_index, side_name, debug=args.debug)
            rimg.analyze_file(filename, cube_size)

            if cube_size is None:
                side_square_count = len(rimg.data.keys())
                cube_size = int(sqrt(side_square_count))

            data = merge_two_dicts(data, rimg.data)
            # log.info("cube_size %d" % cube_size)

        else:
            sys.stderr.write("ERROR: %s does not exist\n" % filename)
            sys.exit(1)

    print(json.dumps(data, sort_keys=True))
