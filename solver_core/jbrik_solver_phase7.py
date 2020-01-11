from utils import log_utils
import jbrik_cube
import jbrik_solver_move_lib

# oppface corners solved https://ruwix.com/the-rubiks-cube/how-to-solve-the-rubiks-cube-beginners-method/orient-yellow-corners-how-to-solve-last-layer-corner/

def solve_oppface_corners(cube):
    log_utils.log("Solving opposite face corners.")
    facetosolve = 3



    #for 7.1
#    solverowcell = "7.1"
#    facemap = jbrik_cube.oppface_cell_face_map[solverowcell]
#    tface = facetosolve.__str__()
#    bface = "1"
#    rface = facemap[3].__str__() #6


    # identify the corners that are not ccolor(unsolvedsolved)
    unsolvedrowcells = "7.3 9.1"

    # orient so that (top) oppface front right corner is unsolved (as well as the front left corner) if you can get both
    # find right hand face for solved rowcell combo
    tface = facetosolve.__str__()
    bface = "1"
    rface = jbrik_cube.oppfacecell_rface_align_map[unsolvedrowcells].__str__()

    # special case where solved rows are opposites
    if unsolvedrowcells == "7.1 9.3" or unsolvedrowcells == "7.3 9.1":
        # rotate once to move unsolved corner into top/front/right
        cube = jbrik_solver_move_lib.perform_rotation_str(tface + "CW1", cube)

    # do this algo 2, check for solve
    # if not solved, 2 more times
    # rotate top until next unsolved corner is in front top right
    # (R' D' R D) x2/4 + u inbetween and after
    movelist = [rface + "CC1", bface + "CC1", rface + "CW1", bface + "CW1"]


    # do to rotations, if not solved in two do two more, pretend takes two for use case
#    for i in range(1, 3):
#        for rmove in movelist:
#            cube = jbrik_solver_move_lib.perform_rotation_str(rmove, cube)

    cube = attempt_corner_solve(movelist, cube)

    # after 2 check for solve, pretend it is
    # simulate opposite corners solving 7.1

    # rotate until next unsolved is in top/front/right
    cube = jbrik_solver_move_lib.perform_rotation_str(tface + "CW2", cube)

    # do to rotations, if not solved in two do two more, pretend takes four for use case
#    for i in range(1, 5):
#        for rmove in movelist:
#            cube = jbrik_solver_move_lib.perform_rotation_str(rmove, cube)

    cube = attempt_corner_solve(movelist, cube)
    cube = attempt_corner_solve(movelist, cube)

    cube = jbrik_solver_move_lib.perform_rotation_str(tface + "CW1", cube)


    cube.finalize_solve_phase()
    log_utils.log("Opposite face corners solved.")
    return cube

def attempt_corner_solve(movelist, cube):
    for i in range(0, 2):
        for rmove in movelist:
            cube = jbrik_solver_move_lib.perform_rotation_str(rmove, cube)

    return cube