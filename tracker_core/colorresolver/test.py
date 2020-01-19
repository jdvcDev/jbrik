import json
from colortools import ciede2000
from colortools import colortools


# raspistill -q 100 -e png -t 1 -sh 100 -br 60 -o /tmp/rubiks-side-U.png
# raspistill -v -w 400 -h 400  -e png -t 1 -sh 100 -br 50 -mm spot -o /tmp/jbrik/rubiks-side-R.png

#https://www.speedsolving.com/threads/rubiks-color-resolver-convert-rgb-values-of-each-square-to-u-l-f-r-b-or-d.64053/
#https://github.com/cs0x7f/min2phase/issues/7

knowncolors = {
    "Red": [185,0,0],
    "Orange": [255,89,0],
    "Yellow": [255,255,0],
    "Green": [0, 155, 72],
    "Blue": [0, 69, 173],
    "White": [255,255,255]
}

testcolors = {
# {"1": [253, 254, 253],
    # "2": [254, 255, 254],
    # "3": [254, 255, 254],
    # "4": [254, 255, 254],
    # "5": [199, 194, 221],
    # "6": [254, 255, 254],
    # "7": [254, 254, 254],
    # "8": [254, 255, 254],
    # "9": [254, 255, 254]}

    (199, 194, 221): "1 yellow",
}


jsonstr = '{"1": [251, 105, 134], "2": [241, 239, 154], "3": [176, 47, 78], "4": [38, 127, 189], "5": [234, 227, 230], "6": [169, 22, 47], "7": [227, 222, 225], "8": [83, 195, 92], "9": [160, 16, 37], "10": [220, 204, 209], "11": [7, 98, 166], "12": [229, 224, 119], "13": [238, 75, 99], "14": [240, 65, 88], "15": [241, 68, 91], "16": [209, 202, 208], "17": [219, 219, 98], "18": [236, 64, 83], "19": [97, 198, 94], "20": [252, 102, 127], "21": [117, 205, 120], "22": [102, 201, 108], "23": [88, 200, 98], "24": [168, 23, 44], "25": [246, 100, 118], "26": [158, 15, 34], "27": [236, 237, 143], "28": [214, 206, 208], "29": [225, 222, 104], "30": [229, 226, 127], "31": [214, 207, 209], "32": [153, 17, 41], "33": [226, 224, 109], "34": [215, 219, 102], "35": [56, 173, 62], "36": [237, 59, 83], "37": [32, 120, 184], "38": [65, 187, 76], "39": [44, 130, 194], "40": [27, 119, 185], "41": [230, 233, 133], "42": [225, 219, 222], "43": [63, 181, 79], "44": [4, 106, 180], "45": [8, 107, 178], "46": [171, 50, 76], "47": [234, 226, 229], "48": [176, 47, 76], "49": [231, 225, 227], "50": [17, 120, 187], "51": [252, 95, 122], "52": [19, 113, 181], "53": [157, 14, 36], "54": [88, 195, 91]}'
test = json.loads(jsonstr)

#print(test["1"])



def map_rgb_to_rowcells(jsonin):
    mappedcolors = {}
    count = 1
    for i in range (1, 19):
        for j in range (1,4):
            if count <= test.__len__():
                key = i.__str__() + "." + j.__str__()
                #print key
                mappedcolors[key] = test[count.__str__()]
                count += 1

    return mappedcolors

#print(mappedcolors)

def convert_mapped_rowcells_to_cubestatestr(mappedcolors):
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

mappedcolors = map_rgb_to_rowcells(jsonstr)
print convert_mapped_rowcells_to_cubestatestr(mappedcolors)



#lowestcolorname = colortools.find_closest_lab_color([83, 195, 92])
#print("Closest match to: " + lowestcolorname)


