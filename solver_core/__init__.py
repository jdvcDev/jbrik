import jbrik_solver_phase1
import jbrik_solver_phase2
import jbrik_cube
import log_utils
import move_lib

#cubeStateStr = "gorowbbyowoywobbgbryrrygowowrbgrrywgwyywgogyygrrbbbwgo"
cubeStateStr = "gwwwwwgwgwoyooobbyoyboygoyobrgrrrorbrgwggyrbrwbygbbyyr"

Cube = jbrik_cube.JbrikCube(cubeStateStr)

solvedCube = jbrik_solver_phase1.solvecross(Cube)
print
solvedCube.print_cube("", True)
solvedCube.print_solvemap()
#raw_input("\nPress Enter to continue...\n")

solvedCube = jbrik_solver_phase2.solvecrosscorners(solvedCube)
print
solvedCube.print_cube("", True)
solvedCube.print_solvemap()
#raw_input("\nPress Enter to continue...\n")


#bug in collapsing this:
#Solve list[26]: ['3CW1', '3CC1', '6CC1', '3CW1', '6CW1', '3CW1', '3CC1', '5CC1', '3CW1', '5CW1', '3CW3', '4CC1', '3CC2', '4CW1', '3CW1', '3CW1', '5CW1', '3CC1', '5CC1', '5CC1', '3CW1', '5CW1', '3CC1', '5CC1', '3CW1', '5CW1']
