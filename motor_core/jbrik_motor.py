from brickuberlib import BricKuberLib
from utils import log_utils
from solver_core import jbrik_cube

class JbrikMotorLib(object):
    _Cuber = BricKuberLib("EV3", True)
    _FaceUp = 1

    def __init__(self):
        log_utils.log("Initializing jbrik")
        raw_input("\nPress Enter to continue...\n")

    def rotate_cube(self, rotcount, dir="CW"):
        rotdeg = 90 * rotcount
        if dir == "CC":
            rotdeg = rotdeg * -1

        self._Cuber.spin(rotdeg)

    def rotate_face(self, rotcount, dir="CW"):
        # TODO implement a grab here for face rotation

        self.rotate_cube(rotcount, dir)

        # TODO and a release

    def flip(self, dir="F"):
        log_utils.log("Start faceUp: " + self._FaceUp.__str__())
        if dir == "F":
            self._Cuber.flip(True)
            if self._FaceUp < 5:
                if self._FaceUp == 4:
                    self._Faceup = 1
                else:
                    self._FaceUp += 1
            else:
                print("no - op")
                SystemExit(1)

        log_utils.log("End faceUp: " + self._FaceUp.__str__())

    def get_face_up(self):
        return self._FaceUp

    def get_face_down(self):
        return jbrik_cube.oppositefaces[self.get_face_up()]

    def flip_to_facenumup(self, facenum):
        # implement ops to put facenum up
        # need current face up
        print("stub")

    def perform_solver_op(self, solverop):
        motorop = self._convert_solver_op_to_motor_op(self, solverop)
        facenumup = motorop[0]
        self.flip_to_facenumup(self, facenumup)
        print("perform motor op")

    # converts a movement from the solver engine to a moter movement
    def _convert_solver_op_to_motor_op(self, solverop):
        # 3CW1 = target face, direction, rotations
        # faceup = face opposite to target face
        # dir = opposite direction
        # 3CW1 = 1CC1
        targetface = solverop[0]
        faceup = jbrik_cube.oppositefaces[int(targetface)]
        dir = solverop[1:3]
        rotcount = solverop[3]
        rotdir = "CW"
        if dir == "CW":
            rotdir = "CC"

        return faceup.__str__() + rotdir + rotcount



    def shutdown(self):
        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.
        self._Cuber.BP.reset_all()

    #Cuber.grab()
    #Cuber.release()
    #Cuber.spin(360)
    #Cuber.home_all()
    #Cuber.flip(True)
    #Cuber.spin(-90)

    #Cuber.home_all()


