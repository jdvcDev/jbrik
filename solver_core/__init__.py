import jbrik_solver_phase1
import jbrik_solver_phase2
import jbrik_cube
import log_utils
import move_lib

cubeStateStr = ""
#cubeStateStr = "owowwwywbgoryorobowowgyybrwryggrgyrybrrggoybbwygobbgbr" # solved in 29
#cubeStateStr = "rgrowgrgwyworoobwoybbryygboyoworywywbrbrgbgyyowgbbgrwg" # loops at pahse 2
#cubeStateStr = "bbwywgyrwowgooowgrgrgwybyowrgrrroywobwbygyryybbogbrobg" # loops at phase 1
#cubeStateStr = "grrowgwywgbbrorogygoobyggwyrbborwrwwborygwogbyywrbbyyo" # loops at phase 1
#cubeStateStr = "gorowbbyowoywobbgbryrrygowowrbgrrywgwyywgogyygrrbbbwgo" # loops at phase 1

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

