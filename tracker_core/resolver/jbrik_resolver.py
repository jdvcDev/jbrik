import json
from colortools import colortools
from utils import log_utils

# https://www.raspberrypi.org/documentation/raspbian/applications/camera.md
# raspistill -q 100 -e png -t 1 -sh 100 -br 60 -o /tmp/rubiks-side-U.png
# raspistill -v -w 400 -h 400  -e png -t 1 -sh 100 -br 50 -mm spot -o /tmp/jbrik/rubiks-side-R.png

#https://www.speedsolving.com/threads/rubiks-color-resolver-convert-rgb-values-of-each-square-to-u-l-f-r-b-or-d.64053/
#https://github.com/cs0x7f/min2phase/issues/7
# https://python-colormath.readthedocs.io/en/latest/delta_e.html

facerotpos = {
    1:3,
    2:6,
    3:9,
    4:2,
    5:5,
    6:8,
    7:1,
    8:4,
    9:7
}

def _map_rgb_to_rowcells(jsonin):
    mappedcolors = {}
    count = 1
    for i in range (1, 19):
        for j in range (1,4):
            if count <= jsonin.__len__():
                key = i.__str__() + "." + j.__str__()
                #print key
                mappedcolors[key] = jsonin[count.__str__()]
                count += 1

    return mappedcolors

def _convert_mapped_rowcells_to_cubestatestr(mappedcolors):
    results = {}
    for rowcell in mappedcolors:
        color = colortools.find_closest_lab_color(mappedcolors[rowcell])
        results[rowcell] = color

    cstr = ""
    for i in range (1, 19):
        for j in range (1,4):
            key = i.__str__() + "." + j.__str__()
            if results.__contains__(key):
                print(key + " " + results[key])
                if results[key] == "White":
                    cstr += "w"
                if results[key] == "Green":
                    cstr += "g"
                if results[key] == "Yellow":
                    cstr += "y"
                if results[key] == "Blue":
                    cstr += "b"
                if results[key] == "Red":
                    cstr += "r"
                if results[key] == "Orange":
                    cstr += "o"

    return cstr

def _get_destpos_for_rotcount(startpos, rotcount):
    for i in range(1, rotcount+1):
        dest = facerotpos[startpos]
        startpos = dest

    return dest

def _adjust_facevals_for_rotation(jsonin, rotcount):
    result = {}
    for start in jsonin:
        endpos = _get_destpos_for_rotcount(int(start), rotcount)
        result[int(start)] = jsonin[endpos.__str__()]

    return result

def _adjust_facevals_for_all_rotations(facecolormap, rotcount):
    adjrotface = {}
    if facecolormap[0] != "":
        jsonin = json.loads(facecolormap[0])
        if not confirm_json_element_length(jsonin):
            adjrotface[0] = ""
        else:
            adjrotface[0] = facecolormap[0]

    for i in range(1, rotcount + 1):
        if facecolormap[i] ==  "":
            continue
        jsonin = json.loads(facecolormap[i])
        if not confirm_json_element_length(jsonin):
            adjrotface[i] = ""
            continue
        # convert to json here
        str = json.dumps(_adjust_facevals_for_rotation(jsonin, i))
        adjrotface[i] = str
    return adjrotface

def confirm_json_element_length(jsonin):
    count = 0
    for element in jsonin:
        idx = int(element)
        if jsonin[idx.__str__()] == None:
            return False

        count += 1

    return count == 9

def resolve_colors(facerotcolormap, rotcount):
    adjfacemap = _adjust_facevals_for_all_rotations(facerotcolormap, rotcount)
    #for res in adjfacemap:
        #print(res.__str__() + " " + adjfacemap[res].__str__())

    bestapproxcolor = colortools.map_to_lowest_average_lab_color_distance_for_rowcell(adjfacemap)
    cstr = ""
    for tile in bestapproxcolor:
        log_utils.log("Tile: " + tile.__str__() + " is color: " + bestapproxcolor[tile])
        if bestapproxcolor[tile] == "White":
            cstr += "w"
        if bestapproxcolor[tile] == "Green":
            cstr += "g"
        if bestapproxcolor[tile] == "Yellow":
            cstr += "y"
        if bestapproxcolor[tile] == "Blue":
            cstr += "b"
        if bestapproxcolor[tile] == "Red":
            cstr += "r"
        if bestapproxcolor[tile] == "Orange":
            cstr += "o"

    return cstr