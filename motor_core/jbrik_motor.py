from brickuberlib import BricKuberLib
from utils import log_utils

class JbrikMotorLib(object):
    Cuber = BricKuberLib("EV3", True)
    FaceUp = 1

    def __init__(self):
        log_utils.log("Initializing jbrik")
        raw_input("\nPress Enter to continue...\n")

    def rotate_face(self, rotcount, dir="CW"):
        rotdeg = 90 * rotcount
        if dir == "CC":
            rotdeg = rotdeg * -1

        self.Cuber.spin(rotdeg)

    def flip(self, dir="F"):
        log_utils.log("Start faceUp: " + self.FaceUp.__str__())
        if dir == "F":
            self.Cuber.flip(True)
            if self.FaceUp < 5:
                if self.FaceUp == 4:
                    self.Faceup = 1
                else:
                    self.FaceUp += 1
            else:
                print("no - op")
                SystemExit(1)

        log_utils.log("End faceUp: " + self.FaceUp.__str__())


    def shutdown(self):
        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.
        self.Cuber.BP.reset_all()

    #Cuber.grab()
    #Cuber.release()
    #Cuber.spin(360)
    #Cuber.home_all()
    #Cuber.flip(True)
    #Cuber.spin(-90)

    #Cuber.home_all()


