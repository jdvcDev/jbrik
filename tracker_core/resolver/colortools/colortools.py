import webcolors
from math import ceil, sqrt
import ciede2000
import json

knowncolors = {
    "Red": [185,0,0],
    "Orange": [255,89,0],
    "Yellow": [255,255,0],
    "Green": [0, 155, 72],
    "Blue": [0, 69, 173],
    "White": [255,255,255]
}

def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name

def getNearestWebSafeColor(r, g, b):
    r = int(round( ( r / 255.0 ) * 5 ) * 51)
    g = int(round( ( g / 255.0 ) * 5 ) * 51)
    b = int(round( ( b / 255.0 ) * 5 ) * 51)
    return (r, g, b)

def get_lab_distance(lab1, lab2):
    """
    http://www.w3resource.com/python-exercises/math/python-math-exercise-79.php

    In mathematics, the Euclidean distance or Euclidean metric is the "ordinary"
    (i.e. straight-line) distance between two points in Euclidean space. With this
    distance, Euclidean space becomes a metric space. The associated norm is called
    the Euclidean norm.
    """
    return sqrt(((lab1.L - lab2.L) ** 2) + ((lab1.a - lab2.a) ** 2) + ((lab1.b - lab2.b) ** 2))


def find_closest_cube_color(inrgb, type):
    lowest = -1
    name = ""
    for kcolor in knowncolors:
        if type == "lab":
            klab = rgb2lab((knowncolors[kcolor][0], knowncolors[kcolor][1], knowncolors[kcolor][2]))
            #labtuple = [lab1.L, lab1.a, lab1.b]
            distance = sqrt(((inrgb[0] - klab.L) ** 2)
                            + ((inrgb[1] - klab.a) ** 2)
                            + ((inrgb[2] - klab.b) ** 2))
        else:
            distance = sqrt(((inrgb[0] - knowncolors[kcolor][0]) ** 2)
                            + ((inrgb[1] - knowncolors[kcolor][1]) ** 2)
                            + ((inrgb[2] - knowncolors[kcolor][2]) ** 2))

        if distance <= lowest or lowest == -1:
            lowest = distance
            name = kcolor
#        print("Distance to color: " + kcolor + " - " + distance.__str__())
#        print("lowest: " + lowest.__str__())
    #print("rgb [" + type + "]: " + inrgb.__str__() + " is color: " + name)
    return name

class LabColor(object):

    # @timed_function
    def __init__(self, L, a, b, red, green, blue):
        self.L = L
        self.a = a
        self.b = b
        self.red = red
        self.green = green
        self.blue = blue

    def __str__(self):
        return "Lab (%s, %s, %s)" % (self.L, self.a, self.b)

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        if self.L != other.L:
            return self.L < other.L

        if self.a != other.a:
            return self.a < other.a

        return self.b < other.b


# @timed_function
def rgb2lab(inputColor):
    (red, green, blue) = inputColor

    # XYZ -> Standard-RGB
    # https://www.easyrgb.com/en/math.php
    var_R = red / 255.0
    var_G = green / 255.0
    var_B = blue / 255.0

    if var_R > 0.04045:
        var_R = pow(((var_R + 0.055) / 1.055), 2.4)
    else:
        var_R = var_R / 12.92

    if var_G > 0.04045:
        var_G = pow(((var_G + 0.055) / 1.055), 2.4)
    else:
        var_G = var_G / 12.92

    if var_B > 0.04045:
        var_B = pow(((var_B + 0.055) / 1.055), 2.4)
    else:
        var_B = var_B / 12.92

    var_R = var_R * 100
    var_G = var_G * 100
    var_B = var_B * 100

    X = var_R * 0.4124 + var_G * 0.3576 + var_B * 0.1805
    Y = var_R * 0.2126 + var_G * 0.7152 + var_B * 0.0722
    Z = var_R * 0.0193 + var_G * 0.1192 + var_B * 0.9505

    reference_X = 95.047
    reference_Y = 100.0
    reference_Z = 108.883

    # XYZ -> CIE-L*ab
    # //www.easyrgb.com/en/math.php
    var_X = X / reference_X
    var_Y = Y / reference_Y
    var_Z = Z / reference_Z

    if var_X > 0.008856:
        var_X = pow(var_X, 1.0 / 3.0)
    else:
        var_X = (7.787 * var_X) + (16.0 / 116.0)

    if var_Y > 0.008856:
        var_Y = pow(var_Y, 1.0 / 3.0)
    else:
        var_Y = (7.787 * var_Y) + (16.0 / 116.0)

    if var_Z > 0.008856:
        var_Z = pow(var_Z, 1.0 / 3.0)
    else:
        var_Z = (7.787 * var_Z) + (16.0 / 116.0)

    L = (116 * var_Y) - 16
    a = 500 * (var_X - var_Y)
    b = 200 * (var_Y - var_Z)
    #print("RGB ({}, {}, {}), L {}, a {}, b {}".format(red, green, blue, L, a, b))
    return LabColor(L, a, b, red, green, blue)


def find_closest_lab_color(rgbin):
    xyz = ciede2000.rgb2xyz(rgbin)
    lab1 = ciede2000.xyz2lab(xyz)
    #distance = ciede2000.ciede2000(lab1, lab2)

    lowestdistance = -1
    lowestcolorname = ""
    for color in knowncolors:
        xyz2 = xyz = ciede2000.rgb2xyz(knowncolors[color])
        lab2 = ciede2000.xyz2lab(xyz2)
        distance = ciede2000.ciede2000(lab1, lab2)

        #print("color: " + color + " dist: " + distance.__str__())

        if lowestdistance == -1 or distance <= lowestdistance:
            lowestdistance = distance
            lowestcolorname = color

    return lowestcolorname

# takes a map of multiple face color mapping (from adjusted rotation photos) and
# returns the calculated color based on lowest Lab color average distance
def map_to_lowest_average_lab_color_distance_for_rowcell(colorfacemap):
    results = {}
    # for each tile on the face
    for i in range(1, 10):
        averagecolormap = {}
        for color in knowncolors:
            averagecolormap[color] = []

        # for each observation from rotation photo
        for rotnum in colorfacemap:
            #jsonstr = json.load(adjfacemap[rotnum])
            facemap = colorfacemap[rotnum]
            jsonstr = json.loads(facemap)
            observedrgb = jsonstr[i.__str__()]
#            print(observedrgb)

            xyz = ciede2000.rgb2xyz(observedrgb)
            lab1 = ciede2000.xyz2lab(xyz)

            for color in knowncolors:
                xyz2 = xyz = ciede2000.rgb2xyz(knowncolors[color])
                lab2 = ciede2000.xyz2lab(xyz2)
                distance = ciede2000.ciede2000(lab1, lab2)
                averagecolormap[color].append(distance)
#                print(observedrgb.__str__() + ": " + color + " " + distance.__str__())

        lowest = -1.0
        name = ""
        for color in averagecolormap:
            colorsum = sum(averagecolormap[color])
            coloravg = colorsum/float(colorfacemap.__len__())

            if lowest == -1.0 or coloravg <= lowest:
                lowest = coloravg
                name = color


#        print(i.__str__() + " " + name)
        results[i] = name

    return results