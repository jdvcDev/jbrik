from utils import log_utils
from tracker_core import resolver
import solver_core as solver
import commands
from motor_core import jbrik_motor

picRotCount = 3
picPath = "/tmp/jbrik/"
picName = "rubiks-side-"
picType = "png"
picCmd = "raspistill -v -w 400 -h 400  -e " + picType + " -t 1 -sh 100 -br 50 -mm spot -o "


# take pictures
def photo_face_rotations(facenum):
    # raspistill -q 100 -e png -t 1 -sh 100 -br 60 -o /tmp/rubiks-side-U.png
    # raspistill -v -w 400 -h 400  -e png -t 1 -sh 100 -br 50 -mm spot -o /tmp/jbrik/rubiks-side-10.png

    for i in range(0, picRotCount + 1):
        log_utils.log("Taking rotation pic: " + i.__str__() + " of face: " + facenum.__str__())
        picstr = picCmd + picPath + picName + facenum.__str__() + i.__str__() + "." + picType
        log_utils.log("Cmd: " + picstr)
        commands.getstatusoutput(picstr)
        print("rotate 90 CW")
        Cuber.rotate_cube(1)

    # spin 90 to return to starting state
    log_utils.log("Rotation pics for face: " + facenum.__str__() + " complete.")

# load picture to map
def resolve_cubestate():
    # python rubiks-cube-tracker.py -f ./resource/jbrik_img/rubiks-side-62.png
    cubeStateStr = ""
    for i in range(1, 7):
        facemap = {}
        for j in range(0, 4):
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


# implement a flip to face num
def photo_all_faces():
    # Photo inline cube faces
    for facenum in range(1, 7):
        print("Flip to facenum: " + facenum.__str__())
        Cuber.flip_to_facenumup(facenum)
        photo_face_rotations(facenum)

    '''
    for facenum in range(1, 5):
        print("Flip to facenum: " + facenum.__str__())
        photo_face_rotations(facenum)
        Cuber.flip()

    print("Fip to facenum: 5")
    Cuber.rotate_cube(1)
    Cuber.flip()
    Cuber.rotate_cube(1, "CC")
    photo_face_rotations(5)

    print("Flip to facenum: 6")
    Cuber.flip()
    Cuber.flip()
    Cuber.rotate_cube(2)
    photo_face_rotations(6)

    print("Flip to facenum: 1")
    Cuber.rotate_cube(1)
    Cuber.flip()
    Cuber.rotate_cube(1, "CW")
    '''


# initialize the solver machine
Cuber = jbrik_motor.JbrikMotorLib()

# take photos of all faces
photo_all_faces()

# Load photos into color map and covert to cubeStateString
cubeStateStr = resolve_cubestate()
log_utils.log("\n\nInitial cube state: " + cubeStateStr)

# Solve cube
#solver.solve_cube(cubeStateStr)

Cuber.shutdown()

exit(1)
