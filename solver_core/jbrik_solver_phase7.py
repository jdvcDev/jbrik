from utils import log_utils
import jbrik_cube
import jbrik_solver_move_lib

# oppface corners solved https://ruwix.com/the-rubiks-cube/how-to-solve-the-rubiks-cube-beginners-method/orient-yellow-corners-how-to-solve-last-layer-corner/

def solve_oppface_corners(cube):
    log_utils.log("Solving opposite face corners.")
    facetosolve = 3

    # orient so that (top) oppface front right corner is unsolved (as well as the front left corner) if you can get both

    # from the perspective of y up
    # when two corners
    # O O
    # X X

    # when opposite corners
    # O X same as   O
    # X O          X X
    #               O
    # then a CW top rotation to align corner

    # when 3 corners
    # O X same as   O
    # X X          X X
    #               X

    #for 7.1
    solverowcell = "7.1"
    facemap = jbrik_cube.oppface_cell_face_map[solverowcell]
    tface = facetosolve.__str__()
    bface = "1"
    rface = facemap[3].__str__()

    # do this algo 2, check for solve
    # if not solved, 2 more times
    # rotate top until next unsolved corner is in front top right
    # (R' D' R D) x2/4 + u inbetween and after
    movelist = [rface + "CC1", bface + "CC1", rface + "CW1", bface + "CW1"]

    # simulate opposite corners solving 7.1
    # rotate once to unsolved corner into top/front/right
    cube = jbrik_solver_move_lib.perform_rotation_str(tface + "CW1", cube)

    # do to rotations, if not solved in two do two more, pretend takes two for use case
    for i in range(1, 3):
        for rmove in movelist:
            cube = jbrik_solver_move_lib.perform_rotation_str(rmove, cube)


    # after 2 check for solve, pretend it is
    # simulate opposite corners solving 7.1

    # rotate until next unsolved is in top/front/right
    cube = jbrik_solver_move_lib.perform_rotation_str(tface + "CW2", cube)

    # do to rotations, if not solved in two do two more, pretend takes four for use case
    for i in range(1, 5):
        for rmove in movelist:
            cube = jbrik_solver_move_lib.perform_rotation_str(rmove, cube)

    cube = jbrik_solver_move_lib.perform_rotation_str(tface + "CW1", cube)


    cube.finalize_solve_phase()
    log_utils.log("Ppposite face corners solved.")
    return cube