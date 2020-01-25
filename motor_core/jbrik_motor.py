from brickuberlib import BricKuberLib
from utils import log_utils
from solver_core import jbrik_cube

class JbrikMotorLib(object):
    _Cuber = None
    _FaceUp = 1

    def __init__(self):
        log_utils.log("Initializing jbrik")
        self._FaceUp = 1
        self._Cuber = BricKuberLib("EV3", True)
        raw_input("\nInitialization complete, Press Enter to continue...\n")

    def get_face_up(self):
        return self._FaceUp

    def get_face_down(self):
        return jbrik_cube.OPPOSITEFACES[self.get_face_up()]

    def rotate_cube(self, rotcount, dir="CW", release=True):
        if release:
            self._Cuber.release()
        rotdeg = 90 * rotcount
        if dir == "CC":
            rotdeg = rotdeg * -1

        self._Cuber.spin(rotdeg, 30)

    def rotate_face(self, rotcount, dir="CW"):
        self._Cuber.grab()
        self.rotate_cube(rotcount, dir, False)

    def release_cube(self):
        self._Cuber.release()

    def grab_cube(self):
        self._Cuber.grab()

    def flip(self, dir="F", release=False):
        log_utils.log("Start faceUp: " + self._FaceUp.__str__())
        if dir == "F":
            self._Cuber.flip(release)
            if self._FaceUp < 5:
                if self._FaceUp == 4:
                    self._FaceUp = 1
                else:
                    self._FaceUp += 1
            else:
                # dont set the face here because flips involving faces 5-6 are compound movements and will be
                # set after complete
                pass

        log_utils.log("End faceUp: " + self._FaceUp.__str__())

    def _flip_1_5(self):
        curfaceup = self._FaceUp
        if curfaceup != 1:
            log_utils.log("flipping to face 1")
            self.flip_to_facenumup(1)

        self.rotate_cube(1)
        self.flip()
        self.rotate_cube(1, "CC")
        # need to manually set faceup here because rotation screws that up
        self._FaceUp = 5

    def _flip_5_1(self):
        self.rotate_cube(1, "CC")
        self.flip()
        self.rotate_cube(1, "CW")
        # need to manually set faceup here because rotation screws that up
        self._FaceUp = 1

    def _flip_1_6(self):
        curfaceup = self._FaceUp
        if curfaceup != 1:
            log_utils.log("flipping to face 1")
            self.flip_to_facenumup(1)

        self.rotate_cube(1, "CC")
        self.flip()
        self.rotate_cube(1, "CW")
        # need to manually set faceup here because rotation screws that up
        self._FaceUp = 6

    def _flip_6_1(self):
        self.rotate_cube(1, "CW")
        self.flip()
        self.rotate_cube(1, "CC")
        # need to manually set faceup here because rotation screws that up
        self._FaceUp = 1

    def flip_to_facenumup(self, facenum, release=False):
        log_utils.log("Flipping to face: " + facenum.__str__())
        curfaceup = self._FaceUp
        if curfaceup == facenum:
            log_utils.log("Current FaceUp is already in position.")
            return

        # Going to 5 from 1-4
        if facenum == 5 and curfaceup <= 4:
            self._flip_1_5()
            curfaceup = self._FaceUp
        # Going to 1-4 from 5
        elif facenum <= 4 and curfaceup == 5:
            self._flip_5_1()
            curfaceup = self._FaceUp
            while curfaceup != facenum and curfaceup <= 4:
                self.flip()
                curfaceup = self._FaceUp
        # Going to 1-4 from 6
        elif facenum == 6 and curfaceup <= 4:
            self._flip_1_6()
            curfaceup = self._FaceUp
        # Going to 6 to 1-4
        elif facenum <= 4 and curfaceup == 6:
            self._flip_6_1()
            curfaceup = self._FaceUp
            while curfaceup != facenum and curfaceup <= 4:
                self.flip()
                curfaceup = self._FaceUp
        # Going 5-6 from 5-6
        elif (facenum == 5 or facenum == 6) and curfaceup > 4:
            for i in range(0, 2):
                self.flip()
            self.rotate_cube(2, "CW")
            self._FaceUp = facenum
            curfaceup = self._FaceUp
        # Going to 1-4 from 1-4
        else:
            while curfaceup != facenum and curfaceup <= 4:
                self.flip()
                curfaceup = self._FaceUp

        if release:
            self.release_cube()

    def perform_motor_op(self, motorop):
        facenumup = int(motorop[0])
        dir = motorop[1:3]
        rotcount = int(motorop[3])

        #log_utils.log("Perform ing motor op: " + motorop)
        self.flip_to_facenumup(facenumup)
        self.rotate_face(rotcount, dir)

    def perform_motor_ops_for_phase(self, motoroplist):
        log_utils.log("Performing solver ops: " + motoroplist.__str__())
        opcount = 1
        for motorop in motoroplist:
            log_utils.log("Performing motor op " + opcount.__str__() + " of " + motoroplist.__len__().__str__()
                          + ": " + motorop)
            self.perform_motor_op(motorop)
            opcount += 1


    def shutdown(self):
        log_utils.log("shutting down cube.")
        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.
        #self._Cuber.BP.set_motor_position(self._Cuber.MOTOR_PORTS[self._Cuber.MOTOR_GRAB], self._Cuber.MOTOR_GRAB_POSITION_REST)
        self._Cuber.BP.reset_all()


# converts a movement from the solver engine to a motor movement
def convert_solver_op_to_motor_op(solverop):
    # 3CW1 = target face, direction, rotations
    # faceup = face opposite to target face
    # dir = opposite direction
    # 3CW1 = 1CC1
    targetface = solverop[0]
    faceup = jbrik_cube.OPPOSITEFACES[int(targetface)]
    dir = solverop[1:3]
    rotcount = solverop[3]
    rotdir = "CW"
    if dir == "CW":
        rotdir = "CC"

    return faceup.__str__() + rotdir + rotcount