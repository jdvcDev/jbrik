import jbrik_solver_phase1
import jbrik_solver_phase2
import jbrik_cube
import log_utils
import move_lib

cubeStateStr = "wborwygoywboooyyyroggrygwoyogbyrgrwwgwrbgrboybrbwbbgwr"


Cube = jbrik_cube.JbrikCube(cubeStateStr)
#raw_input("\nPress Enter to continue...\n")

solvedCube = jbrik_solver_phase1.solvecross(Cube)
print
solvedCube.print_cube("", True)
solvedCube.print_solvemap()


solvedCube = jbrik_solver_phase2.solvecroscorners(solvedCube)
print
solvedCube.print_cube("", True)
solvedCube.print_solvemap()


#simpllist = jbrik_cube.reducemovelist(solvelist)
#print("orig: " + solvelist.__len__().__str__() + " " + solvelist.__str__())
#print("simp: " + simpllist.__len__().__str__() + " " + simpllist.__str__())


