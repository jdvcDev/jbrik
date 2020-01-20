from utils import log_utils
from tracker_core import resolver
import solver_core as solver
import commands


picRotCount = 3
picPath = "/tmp/jbrik/"
picName = "rubiks-side-"
picType = "png"
picCmd = "raspistill -v -w 400 -h 400  -e " + picType + " -t 1 -sh 100 -br 50 -mm spot -o "


# take pictures
def camera_photo_faces(facenum):
    # raspistill -q 100 -e png -t 1 -sh 100 -br 60 -o /tmp/rubiks-side-U.png
    # raspistill -v -w 400 -h 400  -e png -t 1 -sh 100 -br 50 -mm spot -o /tmp/jbrik/rubiks-side-10.png

    for i in range(0, picRotCount + 1):
        log_utils.log("Taking rotation pic: " + i.__str__() + " of face: " + facenum.__str__())
        picstr = picCmd + picPath + picName + facenum.__str__() + i.__str__() + "." + picType
        log_utils.log("Cmd: " + picstr)
        commands.getstatusoutput(picstr)
        print("rotate 90 CW")
        raw_input("\nPress Enter to continue...\n")

    log_utils.log("Rotation pics for face: " + facenum.__str__() + " complete.")

# load picture to map
def resolve_cubestate():
    # python rubiks-cube-tracker.py -f ./resource/jbrik_img/rubiks-side-62.png
    cubeStateStr = ""
    for i in range(1, 7):
        facemap = {}
        for j in range(0,4):
            #imgfile = "./tracker_core/tracker/resource/jbrik_img/rubiks-side-" + i.__str__() + j.__str__() + ".png"
            imgfile = picPath + picName + i.__str__() + j.__str__() + "." + picType
            str = "python ./tracker_core/tracker/rubiks-cube-tracker.py -f " + imgfile
            log_utils.log("Converting image file: " + imgfile + " to rgb values.")
            raw_result = commands.getstatusoutput(str)[1]
            raw_result = raw_result.split("\n")
            raw_result = raw_result[-1]
            log_utils.log("Result: " + raw_result)
            facemap[j] = raw_result

        cubeStateStr += resolver.resolve_colors(facemap)

    return cubeStateStr




# Photo cube faces
for facenum in range(1, 7):
    print("flip to facenum: " + facenum.__str__())
    raw_input("\nPress Enter to continue...\n")
    camera_photo_faces(facenum)

# Load photos into color map and covert to cubeStateString
cubeStateStr = resolve_cubestate()
log_utils.log("\n\nInitial cube state: " + cubeStateStr)

# Solve cube
solver.solve_cube(cubeStateStr)

exit(1)
