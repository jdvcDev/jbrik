import webcolors
import math
from math import ceil, sqrt

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



#{"1": [193, 12, 26], "2": [253, 198, 186], "3": [44, 253, 225], "4": [252, 171, 163], "5": [19, 151, 253], "6": [46, 254, 231], "7": [20, 136, 252], "8": [207, 15, 39], "9": [246, 252, 249]}


requested_colour = [44, 253, 225]
actual_name, closest_name = get_colour_name(requested_colour)

print "Actual colour name:", actual_name, ", closest colour name:", closest_name

'''
(r,g,b)
Red 	FF0000 	255,0,0
Orange 	FFA500 	255,165,0
Yellow 	FFFF00 	255,255,0
Green 	008000 	0,128,0
Blue 	0000FF 	0,0,255
White 	FFFFFF 	255,255,255

mycolor is input, colorI is known

rgbDistance = Math.abs(myColor.getRed() - colorI.getRed() + Math.abs(myColor.getGreen() - colorI.getGreen()) + Math.abs(myColor.getBlue() - colorI.getBlue())
'''
knowncolors = {
    "Red": [255,0,0],
    "Orange": [255,165,0],
    "Yellow": [255,255,0],
    "Green": [0,128,0],
    "Blue": [0,0,255],
    "White": [255,255,255],
}
'''
least = 255
cubecolor = ""
for color in knowncolors:
    rgbDistance = abs(knowncolors[color][0] - 193) + abs(knowncolors[color][1] - 12) + abs(knowncolors[color][2] - 26)
    #rgbDistance = abs(knowncolors[color][0] - 44) + abs(knowncolors[color][1] - 253) + abs(knowncolors[color][2] - 225)
    #rgbDistance = abs(knowncolors[color][0] - 193) + abs(knowncolors[color][1] - 12) + abs(knowncolors[color][2] - 26)
    if rgbDistance < least:
        least = rgbDistance
        cubecolor = color
    print(color + " = " + rgbDistance.__str__())

print("\ncube color: " + cubecolor)
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
    var_R = red / 255
    var_G = green / 255
    var_B = blue / 255

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
        var_X = pow(var_X, 1 / 3)
    else:
        var_X = (7.787 * var_X) + (16 / 116)

    if var_Y > 0.008856:
        var_Y = pow(var_Y, 1 / 3)
    else:
        var_Y = (7.787 * var_Y) + (16 / 116)

    if var_Z > 0.008856:
        var_Z = pow(var_Z, 1 / 3)
    else:
        var_Z = (7.787 * var_Z) + (16 / 116)

    L = (116 * var_Y) - 16
    a = 500 * (var_X - var_Y)
    b = 200 * (var_Y - var_Z)
    # log.info("RGB ({}, {}, {}), L {}, a {}, b {}".format(red, green, blue, L, a, b))

    return LabColor(L, a, b, red, green, blue)
'''
knowncolors = {
    "Red": [255,0,0],
    "Orange": [255,165,0],
    "Yellow": [255,255,0],
    "Green": [0,128,0],
    "Blue": [0,0,255],
    "White": [255,255,255],

for color in knowncolors:
    rgbDistance = abs(knowncolors[color][0] - 193) + abs(knowncolors[color][1] - 12) + abs(knowncolors[color][2] - 26)
    #rgbDistance = abs(knowncolors[color][0] - 44) + abs(knowncolors[color][1] - 253) + abs(knowncolors[color][2] - 225)
    #rgbDistance = abs(knowncolors[color][0] - 193) + abs(knowncolors[color][1] - 12) + abs(knowncolors[color][2] - 26)
    if rgbDistance < least:
        least = rgbDistance
        cubecolor = color
    print(color + " = " + rgbDistance.__str__())
}
'''

#{"1": [193, 12, 26], "2": [253, 198, 186], "3": [44, 253, 225], "4": [252, 171, 163], "5": [19, 151, 253], "6": [46, 254, 231], "7": [20, 136, 252], "8": [207, 15, 39], "9": [246, 252, 249]}
lab2 = rgb2lab((193, 12, 26))
lab1 = rgb2lab((255,0,0))
distance = get_lab_distance(lab1, lab2)
print(distance)

for color in knowncolors:
    lab2 = rgb2lab(knowncolors[color])
    distance = get_lab_distance(lab1, lab2)
    print("Color: " + color + " " + distance.__str__())


