import time     # import the time library for the sleep function
import sys
from utils import log_utils
from tracker_core import tracker
from tracker_core import resolver
from solver_core import jbrik_solver as solver
from motor_core import jbrik_motor as motor

_PicRotCount = 3
_DebugSteps = False
_TruingGrab = True


# take pictures
def _photo_face_rotations(facenum, cuber):
    for rotnum in range(0, _PicRotCount + 1):
        if _TruingGrab:
            cuber.grab_cube()
            cuber.release_cube()
        tracker.jbrick_tracker.photo_face(facenum, rotnum)
        if rotnum > -1:
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
        facemap = tracker.jbrick_tracker.convert_face_pics_to_rgb_facemap(facenum, _PicRotCount)

        # convert the map of face rgb values to cubeStateStr
        cubestatestr += resolver.jbrik_resolver.resolve_colors(facemap, _PicRotCount)

    return cubestatestr

def _photo_all_faces(cuber):
    # Photo inline cube faces
    for facenum in range(1, 7):
        log_utils.log("Flip to facenum: " + facenum.__str__())
        cuber.flip_to_facenumup(facenum, True)
#        if cuber._TruingGrab:
#            cuber.grab_cube()
#            cuber.release_cube()

        _photo_face_rotations(facenum, cuber)

def _run_solve_movements(solvemap, cuber):
    #for phase in solvemap:
    for phase in range(1, 8):
        log_utils.log("Performing movement ops for phase: " + phase.__str__())
        solveoplist = solvemap[phase]
        motoroplist = _convert_solve_movements_to_motor_movements(solveoplist)
        log_utils.log("Converted solve op list to motor op list:\nsolveoplist: " + solveoplist.__str__()
                      + "\nmotoroplist: " + motoroplist.__str__())
        cuber.perform_motor_ops_for_phase(motoroplist)
        if _DebugSteps:
            raw_input("\nPhase: " + phase.__str__() + " complete, Press Enter to continue...\n")

def _convert_solve_movements_to_motor_movements(solveroplist):
    motoroplist = []
    for solveop in solveroplist:
        motorop = motor.convert_solver_op_to_motor_op(solveop)
        motoroplist.append(motorop)

    return motoroplist


Cuber = None
try:
    # initialize the solver machine
    Cuber = motor.JbrikMotorLib(_TruingGrab)

    # take photos of all faces
    _photo_all_faces(Cuber)

    # Load photos into color map and covert to cubeStateString
    CubeStateStr = _resolve_cubestate()
    log_utils.log("\n\nInitial cube state: " + CubeStateStr)

    # Solve cube
    SolveMap = solver.solve_cube(CubeStateStr)
    if _DebugSteps:
        raw_input("\nSolution determined, Press Enter to continue...\n")

    # Run movement commands on cube
    _run_solve_movements(SolveMap,  Cuber)

finally:
    Cuber.release_cube()
    Cuber.shutdown()
    pass

