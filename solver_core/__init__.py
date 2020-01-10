import jbrik_solver_phase1
import jbrik_solver_phase2
import jbrik_solver_phase3
import jbrik_cube
import log_utils
import move_lib


cubeStateStr = "wwowwwoyggbroowwyoogbryyyrbgyrgrbrgwgrybgowryrobgbobby" # solved in 12/18 loops on 3
#cubeStateStr = "rgrowgrgwyworoobwoybbryygboyoworywywbrbrgbgyyowgbbgrwg" # solved in 9/27 loops on 3
#cubeStateStr = "orowwbwgbooroobwogbbogyyrryggrwrbgwybwgygryrywowybgryb" # solved in 15/15/32
#cubeStateStr = "gyrgwogowygbboogbyorogywwrybwrrrorrbybgygbowbrgwybwwyo" # solved in 17/28/32
#cubeStateStr = "rrwbwbyybggoooyyrgowwbybyworgborrwybrgyogwwoobggybrgwr" # solved in 12/21/39
#cubeStateStr = "bbwywgyrwowgooowgrgrgwybyowrgrrroywobwbygyryybbogbrobg" # solved in 12/13/41
#cubeStateStr = "obggwgowogrbboyygwrwobyobwwrogbrgwrryyrrgyyrgwybobobwy" # solved in 6/21/32
#cubeStateStr = "gowowyygwgyrwoobogybowyyyrwbbbwrrrggogorgbbwyorwbbyrgr" # solved in 15/19/31
#cubeStateStr = "owowwwywbgoryorobowowgyybrwryggrgyrybrrggoybbwygobbgbr" # solved in 0/17/31
#cubeStateStr = "grrowgwywgbbrorogygoobyggwyrbborwrwwborygwogbyywrbbyyo" # solved in 13/16/25
#cubeStateStr = "gorowbbyowoywobbgbryrrygowowrbgrrywgwyywgogyygrrbbbwgo" # solved in 16/26/40
#cubeStateStr = "rwgrwbbbbyoogoyogwyrgrybrgwyyoorwbgyobgygrworgwwwbybor" # solved in 11/26/24
#cubeStateStr = "bwrwwwyworoggobygborogyyrrgwyybrbyrgworggowywbroobbgyb" # solved in 0/26/24
#cubeStateStr = "bbrgwgrogbwwwobgyowobyyboygbrobrrwoyggyogworywyrgbwrry" # solved in 6/19/32


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

Cube = jbrik_solver_phase3.solve_middle(Cube)
print
Cube.print_cube("", True)
Cube.print_solvemap()
#raw_input("\nPress Enter to continue...\n")
