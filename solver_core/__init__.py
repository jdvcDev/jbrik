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
#cubeStateStr = "yrygwroygyoyrobwowrbbyyggwrobbwrwgwrbgwygrryowoogbogbb" # 17/26/32/6
#cubeStateStr = "orowwbwgbooroobwogbbogyyrryggrwrbgwybwgygryrywowybgryb" # 15/15/32/6
#cubeStateStr = "gyrgwogowygbboogbyorogywwrybwrrrorrbybgygbowbrgwybwwyo" # 17/28/32/6
#cubeStateStr = "rrwbwbyybggoooyyrgowwbybyworgborrwybrgyogwwoobggybrgwr" # 12/21/39/0
#cubeStateStr = "wwwwwwwwwoooyogyrrgyybyyygoorbbryrrrgoyggggobgobrbbrbb" # 0/0/41/6
#cubeStateStr = "wwwwwwwwwoooyogyrrgyybyyygoorbbryrrrgoyggggobgobrbbrbb" # 0/0/39/6
#cubeStateStr = "gorbwryywbgooooybbgorrybwryoygwrrrywbwoggwggybgwbbyrwo" # 12/26/32/6
#cubeStateStr = "bbwywgyrwowgooowgrgrgwybyowrgrrroywobwbygyryybbogbrobg" # 12/13/41/6
#cubeStateStr = "obggwgowogrbboyygwrwobyobwwrogbrgwrryyrrgyyrgwybobobwy" # 6/21/32/6
#cubeStateStr = "wwwwwwwwwooogobyoygbbyyggybyoygrbrrrgroggrgyroybrbbrob" # 0/0/47/6
#cubeStateStr = "wwowwwgwwyorgorrygboyrybyrwbbgorybrwgbrggobyrogogbbyyo" # 0/23/47/6
#cubeStateStr = "obggwgowogrbboyygwrwobyobwwrogbrgwrryyrrgyyrgwybobobwy" # 6/21/32/6
#cubeStateStr = "wwwwwwwwwoooooooyyyrryygyyrogyrryrrrgbbggrggggbbobbbbb" # 0/0/9/0/0/16/27 Complete!!
#cubeStateStr = "wwwwwwwwwooorobyrroyyyyoyyrbogbrrrrrggyggggyboobgbbgbb" # 0/0 loops in 3
#cubeStateStr = "rwwwwwgwyroggorbbgyoryyyoybbgyorrbggogorgrobwwywbbbroy" # 0/9/16 loops in 3
#cubeStateStr = "oybowrygworrwobwwwgggbyyrbyyobwrrbgwoyrbgobwrgoyybgorg" # 10/22 loops in 3
#cubeStateStr = "wwowwwoyggbroowwyoogbryyyrbgyrgrbrgwgrybgowryrobgbobby" # 12/18 loops on 3
#cubeStateStr = "rgrowgrgwyworoobwoybbryygboyoworywywbrbrgbgyyowgbbgrwg" # 9/27 loops on 3
#cubeStateStr = "orobwrgyrrgwgoybgywwgwyrwrrbwyorygbybobygggborbwobwooy" # 8/14/32 loops in 3
#cubeStateStr = "gowowyygwgyrwoobogybowyyyrwbbbwrrrggogorgbbwyorwbbyrgr" # 15/19/30 loops in 3
#cubeStateStr = "owowwwywbgoryorobowowgyybrwryggrgyrybrrggoybbwygobbgbr" # 0/17/30 loops in 3
#cubeStateStr = "grrowgwywgbbrorogygoobyggwyrbborwrwwborygwogbyywrbbyyo" # 13/16/24 loops in 3
#cubeStateStr = "gorowbbyowoywobbgbryrrygowowrbgrrywgwyywgogyygrrbbbwgo" # 16/26/40 loops in 3
#cubeStateStr = "rwgrwbbbbyoogoyogwyrgrybrgwyyoorwbgyobgygrworgwwwbybor" # 11/26/23 loops in 3
#cubeStateStr = "bwrwwwyworoggobygborogyyrrgwyybrbyrgworggowywbroobbgyb" # 0/26/24 loops in 3
#cubeStateStr = "bbrgwgrogbwwwobgyowobyyboygbrobrrwoyggyogworywyrgbwrry" # 6/19/32 loops in 3

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
Cube = jbrik_solver_phase5.solve_crossopface_orbits(Cube)
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