from utils import log_utils
from tracker_core import resolver
import solver_core as solver
import commands




# take pictures


#load picture to map
# python rubiks-cube-tracker.py -f ./resource/jbrik_img/rubiks-side-62.png

cubeStateStr = ""
for i in range(1, 7):
    facemap = {}
    for j in range(0,4):
        imgfile = "./tracker_core/tracker/resource/jbrik_img/rubiks-side-" + i.__str__() + j.__str__() + ".png"
        str = "python ./tracker_core/tracker/rubiks-cube-tracker.py -f " + imgfile
        log_utils.log("Converting image file: " + imgfile + " to rgb values.")
        raw_result = commands.getstatusoutput(str)[1]
        raw_result = raw_result.split("\n")
        raw_result = raw_result[-1]
        log_utils.log("Result: " + raw_result)
        facemap[j] = raw_result

    cubeStateStr += resolver.resolve_colors(facemap)


# rrrywgobwyooboywowbwbgybbbgyyoyrgwwygryogrggorogwbrrwb loopng
log_utils.log("\n\nInitial cube state: " + cubeStateStr)

#solver.solve_cube(cubeStateStr)