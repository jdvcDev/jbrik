from brickuberlib import BricKuberLib
from utils import log_utils
from solver_core import jbrik_cube

class JbrikMotorLib(object):
    _Cuber = None
    _FaceUp = 1

    def __init__(self):
        log_utils.log("Initializing jbrik")
        self._Faceup = 1
        self._Cuber = BricKuberLib("EV3", True)
        raw_input("\nPress Enter to continue...\n")

    def get_face_up(self):
        return self._FaceUp

    def get_face_down(self):
        return jbrik_cube.oppositefaces[self.get_face_up()]

    def rotate_cube(self, rotcount, dir="CW"):
        self._Cuber.release()
        rotdeg = 90 * rotcount
        if dir == "CC":
            rotdeg = rotdeg * -1

        self._Cuber.spin(rotdeg)

    def rotate_face(self, rotcount, dir="CW"):
        # TODO implement a grab here for face rotation

        self.rotate_cube(rotcount, dir)

        # TODO and a release

    def flip(self, dir="F", release=False):
        log_utils.log("Start faceUp: " + self._FaceUp.__str__())
        if dir == "F":
            #self._Cuber.flip(True)
            self._Cuber.flip(release)
            if self._FaceUp < 5:
                if self._FaceUp == 4:
                    self._FaceUp = 1
                else:
                    self._FaceUp += 1
            else:
                print("no - op")
                SystemExit(1)

        log_utils.log("End faceUp: " + self._FaceUp.__str__())

    # TODO complete and test
    def _flip_1_5(self):
        curfaceup = self._FaceUp
        if curfaceup != 1:
            print("flipping to face 1")
            self.flip_to_facenumup(1)

        self.rotate_cube(1)
        self.flip()
        self.rotate_cube(1, "CC")
        # need to manually set faceup here because rotation screws that up
        self._FaceUp = 5

    # TODO complete and test
    def _flip_5_1(self):
        self.rotate_cube(1, "CC")
        self.flip()
        self.rotate_cube(1, "CW")
        # need to manually set faceup here because rotation screws that up
        self._FaceUp = 1

    # TODO complete and test
    def _flip_1_6(self):
        curfaceup = self._FaceUp
        if curfaceup != 1:
            print("flipping to face 1")
            self.flip_to_facenumup(1)

        self.rotate_cube(1, "CC")
        self.flip()
        self.rotate_cube(1, "CW")
        # need to manually set faceup here because rotation screws that up
        self._FaceUp = 6

    # TODO complete and test
    def _flip_6_1(self):
        self.rotate_cube(1, "CW")
        self.flip()
        self.rotate_cube(1, "CC")
        # need to manually set faceup here because rotation screws that up
        self._FaceUp = 1

    # TODO complete and test
    def flip_to_facenumup(self, facenum):
        print("flipping to face: " + facenum.__str__())
        curfaceup = self._FaceUp
        if curfaceup == facenum:
            log_utils.log("Current FaceUp is already in position.")
            return

        # Going to 5 from 1-4
        if facenum == 5 and curfaceup <= 4:
            self._flip_1_5()
        # Going to 1-4 from 5
        elif facenum <= 4 and curfaceup == 5:
            self._flip_5_1()
            while curfaceup != facenum and curfaceup <= 4:
                self.flip()
        # Going to 1-4 from 6
        elif facenum == 6 and curfaceup <= 4:
            self._flip_1_6()
        # Going to 6 to 1-4
        elif facenum <= 4 and curfaceup == 6:
            self._flip_6_1()
            while curfaceup != facenum and curfaceup <= 4:
                self.flip()
        # Going 5-6 from 5-6
        elif (facenum == 5 or facenum == 6) and curfaceup > 4:
            for i in range(0, 2):
                self.flip()
            self.rotate_cube(2, "CW")
            self._FaceUp = facenum
        # Going to 1-4 from 1-4
        else:
            while curfaceup != facenum and curfaceup <= 4:
                self.flip()
                curfaceup = self._FaceUp

    # TODO complete and test
    def perform_solver_op(self, solverop):
        motorop = self._convert_solver_op_to_motor_op(self, solverop)
        facenumup = motorop[0]
        self.flip_to_facenumup(self, facenumup)
        print("perform motor op")

    # converts a movement from the solver engine to a motor movement
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
#        self._Cuber.BP.set_motor_position(self._Cuber.MOTOR_PORTS[self._Cuber.MOTOR_GRAB], self._Cuber.MOTOR_GRAB_POSITION_REST)
        self._Cuber.BP.reset_all()


    #Cuber.grab()
    #Cuber.release()
    #Cuber.spin(360)
    #Cuber.home_all()
    #Cuber.flip(True)
    #Cuber.spin(-90)

    #Cuber.home_all()


