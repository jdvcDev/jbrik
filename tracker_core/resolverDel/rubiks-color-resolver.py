#!/usr/bin/env python3

'''
shamelessly taken from https://github.com/dwalton76/rubiks-color-resolver
credit to https://github.com/dwalton76

usage:

jdoe@laptop[rubiks-color-resolverDel]# ./usr/bin/rubiks-color-resolverDel.py --filename ./tests/test-data/3x3x3-tetris.txt

python rubiks-color-resolverDel.py --filename ./resource/3x3x3-random-01.txt


python rubiks-color-resolverDel.py --filename ./resource/3x3x3-random-01.txt
'''

from resolverlib import resolve_colors
import logging
import sys


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)7s: %(message)s"
)

resolve_colors(sys.argv)
