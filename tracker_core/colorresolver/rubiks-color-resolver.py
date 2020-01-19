#!/usr/bin/env python3

from rubikscolorresolver import resolve_colors
import logging
import sys


'''
/rubikscolorresolver/resource/3x3x3-jbrik-01.txt
'''


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)7s: %(message)s"
)

resolve_colors(sys.argv)
