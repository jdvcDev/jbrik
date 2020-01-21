from solver_core import jbrik_cube

class Test(object):
    _FaceUp = 3

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


test = Test()
print(test._convert_solver_op_to_motor_op("1CW1"))