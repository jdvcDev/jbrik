import jbrik_solver_phase1
import jbrik_solver_phase2
import jbrik_solver_phase3
import jbrik_solver_phase4
import jbrik_solver_phase5
import jbrik_solver_phase6
import jbrik_solver_phase7
import jbrik_cube


def solve_cube(cubestatestr):
    cubestatestr = "oogrwgwyrrgbwobyrygwbyyrwgwowowrobbyoggrgbwyrboyobyrbg"
    #cubestatestr = "wrrowbwrorywgoobgbowrwyoyywogrbryogygbbwgybwygrgrbbyog" # 11/22/78/6/16/24/27

    Cube = jbrik_cube.JbrikCube(cubestatestr)

    Cube = jbrik_solver_phase1.solvecross(Cube)
    print
    Cube.print_cube("", True)
    Cube.print_solvemap()

    Cube = jbrik_solver_phase2.solvecrosscorners(Cube)
    print
    Cube.print_cube("", True)
    Cube.print_solvemap()

    Cube = jbrik_solver_phase3.solve_middle(Cube)
    print
    Cube.print_cube("", True)
    Cube.print_solvemap()

    Cube = jbrik_solver_phase4.face_oppface_cross(Cube)
    print
    Cube.print_cube("", True)
    Cube.print_solvemap()

    Cube = jbrik_solver_phase5.solve_crossoppface_orbits(Cube)
    print
    Cube.print_cube("", True)
    Cube.print_solvemap()

    Cube = jbrik_solver_phase6.position_oppface_corners(Cube)
    print
    Cube.print_cube("", True)
    Cube.print_solvemap()

    Cube = jbrik_solver_phase7.solve_oppface_corners(Cube)
    print
    Cube.print_cube("", True)
    Cube.print_solvemap()

    return Cube.solveMap

solve_cube("")