import time     # import the time library for the sleep function
import sys
from utils import log_utils
from tracker_core import tracker
from tracker_core import resolver
from solver_core import jbrik_solver as solver
from motor_core import jbrik_motor as motor

PICROTCOUNT = 3

# take pictures
def _photo_face_rotations(facenum, cuber):
    for rotnum in range(0, PICROTCOUNT + 1):
        tracker.jbrick_tracker.photo_face(facenum, rotnum)
        log_utils.log("Rotate 90 CW")
        cuber.rotate_cube(1)

    # spin 90 to return to starting stat
    log_utils.log("Rotation pics for face: " + facenum.__str__() + " complete.")

# load picture to map
def _resolve_cubestate():
    # python rubiks-cube-tracker.py -f ./resource/jbrik_img/rubiks-side-62.png
    cubestatestr = ""

    for facenum in range(1, 7):
        # Convert the photo of the face into a map of rgb values
        facemap = tracker.jbrick_tracker.convert_face_pics_to_rgb_facemap(facenum, PICROTCOUNT)

        # convert the map of face rgb values to cubeStateStr
        cubestatestr += resolver.jbrik_resolver.resolve_colors(facemap, PICROTCOUNT)

    return cubestatestr

def _photo_all_faces(cuber):
    # Photo inline cube faces
    for facenum in range(1, 7):
        print("Flip to facenum: " + facenum.__str__())
        cuber.flip_to_facenumup(facenum, True)
        _photo_face_rotations(facenum, cuber)

def _run_solve_movements(solvemap, cuber):
    #for phase in solvemap:
    for phase in range(1,2):
        log_utils.log("Performing movement ops for phase: " + phase.__str__())
        solveoplist = solvemap[phase]
        motoroplist = _convert_solve_movements_to_motor_movements(solveoplist)
        log_utils.log("Converted solve op list to motor op list:\nsolveoplist: " + solveoplist.__str__()
                      + "\nmotoroplist: " + motoroplist.__str__())
        cuber.perform_motor_ops_for_phase(motoroplist)

def _convert_solve_movements_to_motor_movements(solveroplist):
    motoroplist = []
    for solveop in solveroplist:
        motorop = motor.convert_solver_op_to_motor_op(solveop)
        motoroplist.append(motorop)

    return motoroplist


Cuber = None
try:
    # initialize the solver machine
    Cuber = motor.JbrikMotorLib()

    # take photos of all faces
#    _photo_all_faces(Cuber)

    # Load photos into color map and covert to cubeStateString
    CubeStateStr = "wbbywrrbggoogogorbywwyyrrbbyrrorboywowyggyywrgwgobgbow"
#    CubeStateStr = _resolve_cubestate()
    log_utils.log("\n\nInitial cube state: " + CubeStateStr)

    # Solve cube
    SolveMap = solver.solve_cube(CubeStateStr)

    # Run movement commands on cube
    _run_solve_movements(SolveMap,  Cuber)

finally:
    Cuber.release_cube()
    Cuber.shutdown()
    pass

