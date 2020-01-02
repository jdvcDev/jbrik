from inspect import currentframe, getframeinfo
import jbrik_solver_phase1
import jbrik_cube
import log_utils
import move_lib

cubeStateStr = "bggwwworygybwobywgboyyyogorobbgrrorwrbwggyryrwowgbroby"

# TODO move this to tracker/solver
def solvecross(cube):
    log_utils.log("Starting cross solve")

    ccolor = cube.get_cell_val_by_rowcell("2.2")
    facetosolve = 1
    log_utils.log("Center color for face 1: "  + ccolor + "\n")

    faced = False
    while not faced:
        # face first order cross cells
        startSolveLen = -1
        while cube.get_solve_move_list().__len__() != startSolveLen:
            startSolveLen = cube.get_solve_move_list().__len__()
            cube = jbrik_solver_phase1.facecross_o1(cube, ccolor, facetosolve)
            log_utils.log("Start solve length: " + startSolveLen.__str__() + " solvelist length: "
                  + cube.get_solve_move_list().__len__().__str__() + "\n")
            cube.print_cube("", True)

        # face second order cross cells
        cube = jbrik_solver_phase1.facecross_o2(cube, ccolor, facetosolve)

        # face third order cross cells
        cube = jbrik_solver_phase1.facecross_o3(cube, ccolor, facetosolve)

        for crosscell in cube.get_cross_rowcell_for_face(1):
            if cube.get_cell_val_by_rowcell(crosscell) != ccolor:
                faced = False
                break
            else:
                faced = True

    log_utils.log("Cross is faced")

    # solve frst order cross cell, i.e rotate fce
#    cube = jbrik_solver_phase1.solve_cross_o1(cube, ccolor, facetosolve)
    # for each remaining unsolved
#    cube = jbrik_solver_phase1.solve_cross_o2(cube, ccolor, facetosolve)

#    cube = move_lib.ninetydswap("2.3", "CW", cube)
#    cube = move_lib.ninetydswap("2.3", "CC", cube)
#    cube = move_lib.oneeightydswap("2.3", cube)
    return cube

Cube = jbrik_cube.JbrikCube(cubeStateStr)
#raw_input("\nPress Enter to continue...\n")

solvedCube = solvecross(Cube)
#print
#solvedCube.print_cube("", True)