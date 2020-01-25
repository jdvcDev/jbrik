import jbrik_solver_phase1
import jbrik_solver_phase2
import jbrik_solver_phase3
import jbrik_solver_phase4
import jbrik_solver_phase5
import jbrik_solver_phase6
import jbrik_solver_phase7
import jbrik_cube


def solve_cube(cubestatestr):
    #cubestatestr = "yygrwgrrrbbbroowrbggoyywowbgbyyrbrbwroooggwwwyoggbwoyy" # 10/20/27/6/25/16/26
    #cubestatestr = "wbbywrrbggoogogorbywwyyrrbbyrrorboywowyggyywrgwgobgbow" # 10/13/46/6/25/8/27
    #cubestatestr = "oworwbbggowyroybbrwrwrygrobwbrbrygogygywgorogbywybgowy" # 10/13/31/6/0/16/26
    #cubestatestr = "bybbwgobygoooogyorgywryryggrrwwrgwbwoyoogybwgbrrbbwrwy" # 7/22/31/6/25/16/52
    #cubestatestr = "gywowobgyoyrrgbbgwrrboybrgrbwwobrobgoygyrwgroywygobwwy" # 13/22/24/6/25/16/52

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

    return Cube.solveMap

#solve_cube("")