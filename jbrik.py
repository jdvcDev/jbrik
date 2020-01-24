import time     # import the time library for the sleep function
import sys
import commands
from utils import log_utils
from tracker_core import tracker
from tracker_core import resolver
from solver_core import jbrik_solver as solver
from motor_core import jbrik_motor as motor

picRotCount = 3
picPath = "/tmp/jbrik/"
picName = "rubiks-side-"
picType = "png"
picCmd = "raspistill -v -w 400 -h 400  -e " + picType + " -t 1 -sh 100 -br 50 -mm spot -o "



# TODO move this method to the tracker
# take pictures
def photo_face_rotations(facenum, cuber):
    # raspistill -q 100 -e png -t 1 -sh 100 -br 60 -o /tmp/rubiks-side-U.png
    # raspistill -v -w 400 -h 400  -e png -t 1 -sh 100 -br 50 -mm spot -o /tmp/jbrik/rubiks-side-10.png

    for i in range(0, picRotCount + 1):
        log_utils.log("Taking rotation pic: " + i.__str__() + " of face: " + facenum.__str__())
        picstr = picCmd + picPath + picName + facenum.__str__() + i.__str__() + "." + picType
        log_utils.log("Cmd: " + picstr)
        commands.getstatusoutput(picstr)
        log_utils.log("Rotate 90 CW")
        cuber.rotate_cube(1)

    # spin 90 to return to starting stat
    log_utils.log("Rotation pics for face: " + facenum.__str__() + " complete.")

# load picture to map
def resolve_cubestate():
    # python rubiks-cube-tracker.py -f ./resource/jbrik_img/rubiks-side-62.png
    cubestatestr = ""

    for facenum in range(1, 7):
        # Convert the photo of the face into a map of rgb values
        facemap = tracker.jbrick_tracker.convert_face_pics_to_rgb_facemap(picRotCount, picPath,
                                                                          picName, picType, facenum)

        # convert the map of face rgb values to cubeStateStr
        cubestatestr += resolver.jbrik_resolver.resolve_colors(facemap, picRotCount)

    return cubestatestr

def photo_all_faces(cuber):
    # Photo inline cube faces
    for facenum in range(1, 7):
        print("Flip to facenum: " + facenum.__str__())
        cuber.flip_to_facenumup(facenum, True)
        photo_face_rotations(facenum, cuber)

def run_solve_movements(solvemap, cuber):
    #for phase in solvemap:
    for phase in range(1,2):
        log_utils.log("Performing movement ops for phase: " + phase.__str__())
        solveoplist = solvemap[phase]
        motoroplist = convert_solve_movements_to_motor_movements(solveoplist)
        log_utils.log("Converted solve op list to motor op list:\nsolveoplist: " + solveoplist.__str__()
                      + "\nmotoroplist: " + motoroplist.__str__())
        cuber.perform_motor_ops_for_phase(motoroplist)

def convert_solve_movements_to_motor_movements(solveroplist):
    motoroplist = []
    for solveop in solveroplist:
        motorop = motor.convert_solver_op_to_motor_op(solveop)
        motoroplist.append(motorop)

    return motoroplist



try:
    # initialize the solver machine
    Cuber = motor.JbrikMotorLib()

    # take photos of all faces
#    photo_all_faces(Cuber)

    # Load photos into color map and covert to cubeStateString
    CubeStateStr = "wbbywrrbggoogogorbywwyyrrbbyrrorboywowyggyywrgwgobgbow"
    #CubeStateStr = resolve_cubestate()
    log_utils.log("\n\nInitial cube state: " + CubeStateStr)

    # Solve cube
    SolveMap = solver.solve_cube(CubeStateStr)

    # Run movement commands on cube
    run_solve_movements(SolveMap,  Cuber)

finally:
    Cuber.release_cube()
    Cuber.shutdown()
    pass

