import jbrik_solver_phase1
import jbrik_solver_phase2
import jbrik_solver_phase3
import jbrik_solver_phase4
import jbrik_solver_phase5
import jbrik_solver_phase6
import jbrik_solver_phase7
import jbrik_cube
import jbrik_solver_move_lib


cubeStateStr = "woyywggobybywowygwrorgyrrbbgwoyrroygrbwyggorbwrgwbbboo" # 7/17/55/0/41/16/27 solved
#cubeStateStr = "grywwbbybworgorwrbbgygybrbrgwgbrgwyogwyygoywowrooboryo" # 9/14/32/6/17/8/0 solved
#cubeStateStr = "wggywywrygybboobobrwywyrobbgyogrbgorywwgggrboywrrbowro" # 10/23/24/6/8/16/52 solved
#cubeStateStr = "woygwyybwoyrwobywoggwryryogbbrwrgoyrbowrggbwboogbbyrrg" # 10/26/54/6/16/16/27 solved
#cubeStateStr = "wwwwwwwwwooooogyyoggyyyobbroyyrrrrrrgbbggggrgyybobbrbb" # 0/0/24/6/17/8/0 solved
#cubeStateStr = "worowrobbwwyyowrggworgybbyoyryrrbbbygygggrogwrwoybwbog" # 7/16/62/6/25/8/27 solved
#cubeStateStr = "wwwwwwwwwoooooyybygrggygbbbyoyyrrrrrgyoggrgoorbbybbrgb" # 0/0/53/6/41/16/26 SOLVED!!

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

Cube = jbrik_solver_phase5.solve_crossoppface_orbits(Cube)
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
