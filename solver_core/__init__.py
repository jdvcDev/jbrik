import jbrik_solver_phase1
import jbrik_solver_phase2
import jbrik_solver_phase3
import jbrik_cube
import log_utils
import move_lib



#cubeStateStr = "wwowwwoyggbroowwyoogbryyyrbgyrgrbrgwgrybgowryrobgbobby" # 12/18 loops on 3
#cubeStateStr = "rgrowgrgwyworoobwoybbryygboyoworywywbrbrgbgyyowgbbgrwg" # 9/27 loops on 3
cubeStateStr = "wwwwwwwwwoooyogyrrgyybyyygoorbbryrrrgoyggggobgobrbbrbb" # 0/0/39
#cubeStateStr = "gorbwryywbgooooybbgorrybwryoygwrrrywbwoggwggybgwbbyrwo" # 12/26/31
#cubeStateStr = "orobwrgyrrgwgoybgywwgwyrwrrbwyorygbybobygggborbwobwooy" # 8/14/32
#cubeStateStr = "orowwbwgbooroobwogbbogyyrryggrwrbgwybwgygryrywowybgryb" # 15/15/30
#cubeStateStr = "gyrgwogowygbboogbyorogywwrybwrrrorrbybgygbowbrgwybwwyo" # 17/28/32
#cubeStateStr = "rrwbwbyybggoooyyrgowwbybyworgborrwybrgyogwwoobggybrgwr" # 12/21/40
#cubeStateStr = "bbwywgyrwowgooowgrgrgwybyowrgrrroywobwbygyryybbogbrobg" # 12/13/38
#cubeStateStr = "obggwgowogrbboyygwrwobyobwwrogbrgwrryyrrgyyrgwybobobwy" # 6/21/32
#cubeStateStr = "gowowyygwgyrwoobogybowyyyrwbbbwrrrggogorgbbwyorwbbyrgr" # 15/19/30
#cubeStateStr = "owowwwywbgoryorobowowgyybrwryggrgyrybrrggoybbwygobbgbr" # 0/17/30
#cubeStateStr = "grrowgwywgbbrorogygoobyggwyrbborwrwwborygwogbyywrbbyyo" # 13/16/24
#cubeStateStr = "gorowbbyowoywobbgbryrrygowowrbgrrywgwyywgogyygrrbbbwgo" # 16/26/40
#cubeStateStr = "rwgrwbbbbyoogoyogwyrgrybrgwyyoorwbgyobgygrworgwwwbybor" # 11/26/23
#cubeStateStr = "bwrwwwyworoggobygborogyyrrgwyybrbyrgworggowywbroobbgyb" # 0/26/23
#cubeStateStr = "bbrgwgrogbwwwobgyowobyyboygbrobrrwoyggyogworywyrgbwrry" # 6/19/30


def solve_cube(cubestatestr):
    Cube = jbrik_cube.JbrikCube(cubestatestr)

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

    return Cube


solve_cube(cubeStateStr)
