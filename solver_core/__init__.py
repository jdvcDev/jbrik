import jbrik_solver_phase1
import jbrik_solver_phase2
import jbrik_cube
import log_utils
import move_lib


cubeStateStr = "wwowwwoyggbroowwyoogbryyyrbgyrgrbrgwgrybgowryrobgbobby" # loops in 2
#cubeStateStr = "obggwgowogrbboyygwrwobyobwwrogbrgwrryyrrgyyrgwybobobwy" # solved in 6/21
#cubeStateStr = "gowowyygwgyrwoobogybowyyyrwbbbwrrrggogorgbbwyorwbbyrgr" # solved in 15/19
#cubeStateStr = "owowwwywbgoryorobowowgyybrwryggrgyrybrrggoybbwygobbgbr" # solved in 0/17
#cubeStateStr = "grrowgwywgbbrorogygoobyggwyrbborwrwwborygwogbyywrbbyyo" # solved in 13/16
#cubeStateStr = "gorowbbyowoywobbgbryrrygowowrbgrrywgwyywgogyygrrbbbwgo" # solved in 16/26
#cubeStateStr = "rwgrwbbbbyoogoyogwyrgrybrgwyyoorwbgyobgygrworgwwwbybor" # solved in 11/26
#cubeStateStr = "bwrwwwyworoggobygborogyyrrgwyybrbyrgworggowywbroobbgyb" # solved in 0/26
#cubeStateStr = "bbwywgyrwowgooowgrgrgwybyowrgrrroywobwbygyryybbogbrobg" # solved in 12/13
#cubeStateStr = "bbrgwgrogbwwwobgyowobyyboygbrobrrwoyggyogworywyrgbwrry" # solved in 6/19
#cubeStateStr = "rgrowgrgwyworoobwoybbryygboyoworywywbrbrgbgyyowgbbgrwg" # solved in 9/27


Cube = jbrik_cube.JbrikCube(cubeStateStr)

Cube = jbrik_solver_phase1.solvecross(Cube)
print
Cube.print_cube("", True)
Cube.print_solvemap()
#raw_input("\nPress Enter to continue...\n")

Cube = jbrik_solver_phase2.solvecrosscorners(Cube)
print
Cube.print_cube("", True)
Cube.print_solvemap()
#raw_input("\nPress Enter to continue...\n")

