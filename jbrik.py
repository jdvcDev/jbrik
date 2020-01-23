import time     # import the time library for the sleep function
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



#from motor_core import brickuberlib
# initialize the solver machine
#Cuber = jbrik_motor.JbrikMotorLib()
#Cuber = brickuberlib.BricKuberLib("EV3", True)
#Cuber.spin(90)
#Cuber.flip()




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

        '''
        facemap = {}
        for j in range(0, picRotCount + 1):
            #imgfile = "./tracker_core/tracker/resource/jbrik_img/rubiks-side-" + i.__str__() + j.__str__() + ".png"
            imgfile = picPath + picName + i.__str__() + j.__str__() + "." + picType
            str = "python ./tracker_core/tracker/rubiks-cube-tracker.py -f " + imgfile
            log_utils.log("Converting image file: " + imgfile + " to rgb values.")
            raw_result = commands.getstatusoutput(str)[1]
            raw_result = raw_result.split("\n")
            raw_result = raw_result[-1]
            log_utils.log("Result: " + raw_result)
            facemap[j] = raw_result
        '''
    return cubestatestr

def photo_all_faces():
    # Photo inline cube faces
    for facenum in range(1, 7):
        print("Flip to facenum: " + facenum.__str__())
        Cuber.flip_to_facenumup(facenum)
        # TODO implement release in flip to facenum
        Cuber._Cuber.release()
        photo_face_rotations(facenum)

    '''    
    for facenum in range(1, 3):
        print("Flip to facenum: " + facenum.__str__())
        #photo_face_rotations(facenum)
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

def run_solve_movements(solvemap):
    for phase in solvemap:
        log_utils.log("Performing movement ops for phase: " + phase.__str__())
        motor.perform_solver_ops(solvemap[phase])






# initialize the solver machine
Cuber = motor.JbrikMotorLib()
#Cuber.flip_to_facenumup(3)
#time.sleep(0.5)
#Cuber.flip_to_facenumup(1)
#Cuber.flip_to_facenumup(6)
#time.sleep(0.5)
#Cuber.flip_to_facenumup(1)



# take photos of all faces
photo_all_faces()

# Load photos into color map and covert to cubeStateString
CubeStateStr = resolve_cubestate()
#log_utils.log("\n\nInitial cube state: " + cubeStateStr)

# Solve cube
SolveMap = solver.solve_cube(CubeStateStr)

# Run movement commands on cube
run_solve_movements()

Cuber.release_cube()

Cuber.shutdown()

