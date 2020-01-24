import commands
from utils import log_utils

def convert_face_pics_to_rgb_facemap(picrotcount, picpath, picname, pictype, facenum):
    facemap = {}
    for j in range(0, picrotcount + 1):
        # imgfile = "./tracker_core/tracker/resource/jbrik_img/rubiks-side-" + i.__str__() + j.__str__() + ".png"
        imgfile = picpath + picname + facenum.__str__() + j.__str__() + "." + pictype
        str = "python ./tracker_core/tracker/rubiks-cube-tracker.py -f " + imgfile
        log_utils.log("Converting image file: " + imgfile + " to rgb values.")
        raw_result = commands.getstatusoutput(str)[1]
        # attempt to skip a face that didn't get resolved correctly
        if raw_result.__contains__("AssertionError"):
            facemap[j] = ""
            continue
        raw_result = raw_result.split("\n")
        raw_result = raw_result[-1]
        log_utils.log("Result: " + raw_result)
        facemap[j] = raw_result

    return facemap