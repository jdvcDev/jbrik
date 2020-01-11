import jbrik_solver_phase1
import jbrik_solver_phase2
import jbrik_solver_phase3
import jbrik_solver_phase4
import jbrik_solver_phase5
import jbrik_solver_phase6
import jbrik_solver_phase7
import jbrik_cube
import jbrik_solver_move_lib

cubeStateStr = "rwwwwwgwyroggorwbgoyrryyobbyororrbggoyyrggobwbywgbbboy" # 5/16/48/6
#cubeStateStr = "rwwwwwgwyroggorbbgyoryyyoybbgyorrbggogorgrobwwywbbbroy" # 0/9/16
#cubeStateStr = "yrygwroygyoyrobwowrbbyyggwrobbwrwgwrbgwygrryowoogbogbb" # 17/26/32/6
#cubeStateStr = "orowwbwgbooroobwogbbogyyrryggrwrbgwybwgygryrywowybgryb" # 15/15/32/6
#cubeStateStr = "gyrgwogowygbboogbyorogywwrybwrrrorrbybgygbowbrgwybwwyo" # 17/28/32/6
#cubeStateStr = "rrwbwbyybggoooyyrgowwbybyworgborrwybrgyogwwoobggybrgwr" # 12/21/39/0
cubeStateStr = "wwwwwwwwwoooooooyyyrryygyyrogyrryrrrgbbggrggggbbobbbbb" # 0/0/9/0/0/16/27 Complete!!
#cubeStateStr = "wwowwwoyggbroowwyoogbryyyrbgyrgrbrgwgrybgowryrobgbobby" # 12/18 loops on 3
#cubeStateStr = "rgrowgrgwyworoobwoybbryygboyoworywywbrbrgbgyyowgbbgrwg" # 9/27 loops on 3
#cubeStateStr = "gowowyygwgyrwoobogybowyyyrwbbbwrrrggogorgbbwyorwbbyrgr" # 15/19/31 loops in 3
#cubeStateStr = "owowwwywbgoryorobowowgyybrwryggrgyrybrrggoybbwygobbgbr" # 0/17/31 loops in 3
#cubeStateStr = "grrowgwywgbbrorogygoobyggwyrbborwrwwborygwogbyywrbbyyo" # 13/16/25 loops in 3
#cubeStateStr = "gorowbbyowoywobbgbryrrygowowrbgrrywgwyywgogyygrrbbbwgo" # 16/26/40 loops in 3
#cubeStateStr = "rwgrwbbbbyoogoyogwyrgrybrgwyyoorwbgyobgygrworgwwwbybor" # 11/26/24 loops in 3
#cubeStateStr = "bwrwwwyworoggobygborogyyrrgwyybrbyrgworggowywbroobbgyb" # 0/26/24 loops in 3
#cubeStateStr = "bbrgwgrogbwwwobgyowobyyboygbrobrrwoyggyogworywyrgbwrry" # 6/19/32 loops in 3
#cubeStateStr = "bbwywgyrwowgooowgrgrgwybyowrgrrroywobwbygyryybbogbrobg" # 12/13/41 fails in 4
#cubeStateStr = "obggwgowogrbboyygwrwobyobwwrogbrgwrryyrrgyyrgwybobobwy" # 6/21/32 loops in 4
#cubeStateStr = "wwwwwwwwwooogobyoygbbyyggybyoygrbrrrgroggrgyroybrbbrob" # 0/0/47 loops in 4
#cubeStateStr = "wwowwwgwwyorgorrygboyrybyrwbbgorybrwgbrggobyrogogbbyyo" # 0/23/47 loops in 4

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

Cube = jbrik_solver_phase4.face_oppface_cross(Cube)
print
Cube.print_cube("", True)
Cube.print_solvemap()
#raw_input("\nPress Enter to continue...\n")
'''
Cube = jbrik_solver_phase5.
print
Cube.print_cube("", True)
Cube.print_solvemap()
#raw_input("\nPress Enter to continue...\n")

Cube = jbrik_solver_phase6.position_oppface_corners(Cube)
print
Cube.print_cube("", True)
Cube.print_solvemap()
#raw_input("\nPress Enter to continue...\n")

Cube = jbrik_solver_phase7.solve_oppface_corners(Cube)
print
Cube.print_cube("", True)
Cube.print_solvemap()
#raw_input("\nPress Enter to continue...\n")
'''