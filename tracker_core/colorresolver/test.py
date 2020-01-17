import webcolors
import numpy as np
import math
import cv2
import colorsys

from math import ceil, sqrt

knowncolors = {
    "Red": [255,0,0],
    "Orange": [255,165,0],
    "Yellow": [255,255,0],
    #"Green": [0,128,0],
    "Green": [0, 255, 0],
    "Blue": [0,0,255],
    "White": [255,255,255]
}
testcolors = {
    (193, 12, 26): "red",
    (253, 198, 186): "orange",
    (44, 253, 225): "green",
    (252, 171, 163): "orange",
    (19, 151, 253): "blue",
    (46, 254, 231): "green",
    (20, 136, 252): "blue",
    (207, 15, 39): "red",
    (246, 252, 249): "white"
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
    print("rgb [" + type + "]: " + inrgb.__str__() + " is color: " + name)

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






for color in testcolors:
    print("test color: " + testcolors[color] + " " + color.__str__())
    actual_name, closest_name = get_colour_name(color)
    if actual_name is None:
        actual_name = "none"
    closestwebrgb = getNearestWebSafeColor(color[0], color[1], color[2])
    lab1 = rgb2lab(color)
    labtuple = [lab1.L, lab1.a, lab1.b]

    print ("actual: " + actual_name)
    print ("closest web rgb:" + closestwebrgb.__str__())
    print("closest web name: " + closest_name)
    find_closest_cube_color(color, "raw")
    find_closest_cube_color(closestwebrgb, "web")
    find_closest_cube_color(labtuple, "lab")
    print





'''

def get_lab_distance(lab1, lab2):
    """
    http://www.w3resource.com/python-exercises/math/python-math-exercise-79.php

    In mathematics, the Euclidean distance or Euclidean metric is the "ordinary"
    (i.e. straight-line) distance between two points in Euclidean space. With this
    distance, Euclidean space becomes a metric space. The associated norm is called
    the Euclidean norm.
    """
    return sqrt(((lab1.L - lab2.L) ** 2) + ((lab1.a - lab2.a) ** 2) + ((lab1.b - lab2.b) ** 2))


lab1 = rgb2lab([252, 171, 163])
for color in knowncolors:
    lab2 = rgb2lab(knowncolors[color])
    distance = get_lab_distance(lab1, lab2)
    print("lab1: "  + lab1.__str__())
    print("lab2: " + lab2.__str__())
    print("Color: " + color + " " + distance.__str__() + "\n")

knowncolors = {
    "Red": [255,0,0],
    "Orange": [255,165,0],
    "Yellow": [255,255,0],
    "Green": [0,128,0],
    "Blue": [0,0,255],
    "White": [255,255,255],

#{"1": [193, 12, 26],  r
# "2": [253, 198, 186], o
# "3": [44, 253, 225], g
# "4": [252, 171, 163], o
# "5": [19, 151, 253], b
# "6": [46, 254, 231], g
# "7": [20, 136, 252], b
# "8": [207, 15, 39], r
# "9": [246, 252, 249]} w
}


# create upper/lower bounds
sensitivity = 10
for color in knowncolors:
    bgr = np.uint8([[[knowncolors[color][2], knowncolors[color][1], knowncolors[color][0]]]])
    hsvkc = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    lower = np.uint8([hsvkc[0][0][0] - sensitivity, 50, 50])  # yellow lower
    upper = np.uint8([hsvkc[0][0][0] + sensitivity, 255, 255])  # yellow upper

    print(color + " " + hsvkc.__str__())
    print("lower: " + lower.__str__())
    print("upper: " + upper.__str__())
    print

for rgb in testcolors:
    print (rgb.__str__() + " " + testcolors[rgb])


color = np.uint8([[[26,12,193]]]) # red #here insert the bgr values which you want to convert to hsv
#color = np.uint8([[[253,151,19]]]) # blue #here insert the bgr values which you want to convert to hsv
#color = np.uint8([[[0,255,0]]]) # green #here insert the bgr values which you want to convert to hsv
hsvcolor1 = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)
print("input hsv: " + hsvcolor1[0][0].__str__())

#color2 = np.uint8([[[0,0,255]]]) #here insert the bgr values which you want to convert to hsv
color2 = np.uint8([[[255,0,0]]]) # blue
#color2 = np.uint8([[[0,255,0]]]) # green
#color2 = np.uint8([[[0,165,255]]]) # orange
hsvcolor2 = cv2.cvtColor(color2, cv2.COLOR_BGR2HSV)
print("known hsv: " + hsvcolor2[0][0].__str__())

sensitivity = 40
lower = np.uint8([hsvcolor2[0][0][0] - sensitivity, 50, 50]) # yellow lower
upper = np.uint8([hsvcolor2[0][0][0] + sensitivity, 255, 255]) # yellow upper
print("lower: " + lower.__str__())
print("upper: " + upper.__str__())

inrange = cv2.inRange(hsvcolor1, lower, upper)
print(inrange)
'''


