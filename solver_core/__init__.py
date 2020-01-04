import jbrik_solver_phase1
import jbrik_solver_phase2
import jbrik_cube
import log_utils
import move_lib

cubeStateStr = "owbywrrrbwbywoygrrrwwoyorggbrooroggwogyygwobgybwybgybb"


Cube = jbrik_cube.JbrikCube(cubeStateStr)
#raw_input("\nPress Enter to continue...\n")

solvedCube = jbrik_solver_phase1.solvecross(Cube)
print
solvedCube.print_cube("", True)
solvedCube.print_solvemap()

deststr = jbrik_cube.get_dest_pos_for_face_rotation("18.1", "3CW3")


solvedCube = jbrik_solver_phase2.solvecrosscorners(solvedCube)
print
solvedCube.print_cube("", True)
solvedCube.print_solvemap()



