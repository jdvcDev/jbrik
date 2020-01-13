from utils import log_utils
import jbrik_cube
import jbrik_solver_move_lib

# oppface cross orbits solved https://ruwix.com/the-rubiks-cube/how-to-solve-the-rubiks-cube-beginners-method/step-5-swap-yellow-edges/
def solve_crossoppface_orbits(cube):
    facetosolve = 3

    #identify a crossfowcell that can be flipped left to be solved, or flipped 180
    nextunsolved = get_next_unsolved_crossrowcell(facetosolve, cube)
    if nextunsolved == "":
        log_utils.log("All crosscells are solved.")
        return cube

    # a CW rotation is a leftshit
    if is_nextpos_solved_by_rowcell(facetosolve, nextunsolved, cube):
        print
        #rotate nextpos CW 1
        #if left
        # R U R' U R U2 R' U

    #if 180
    # (R U R' U R U2 R' U) y2 (R U R' U R U2 R' U)

    # check for a solve after each operation

    return cube

def get_next_unsolved_crossrowcell(facetosolve, cube):
    crosscells = jbrik_cube.get_cross_rowcell_for_face(facetosolve)
    ccolor = cube.get_center_color_for_facenum(facetosolve)

    for crosscell in crosscells:
        crosscellcolor = cube.get_cell_val_by_rowcell(crosscell)
        adjrowcell = jbrik_cube.get_adjrowccell_for_rowcell(crosscell)
        adjrowcellcolor = cube.get_cell_val_by_rowcell(adjrowcell)
        adjrowcellccolor = cube.get_center_color_for_rowcell(adjrowcell)

        if crosscellcolor != ccolor or adjrowcellcolor != adjrowcellccolor:
            return crosscell

    return ""

def is_nextpos_solved_by_rowcell(facetosolve, rowcell, cube):
    adjrowcell = jbrik_cube.get_adjrowccell_for_rowcell(rowcell)
    adjrowcellcolor = cube.get_cell_val_by_rowcell(adjrowcell)

    # we know rowcellcolor and ccolor match because we solve that in the last phase
    nextpos = jbrik_cube.get_next_centerpos_for_face_rotation(facetosolve, rowcell, dir="CW")
    nextposadjrowcell = jbrik_cube.get_adjrowccell_for_rowcell(nextpos)
    nextposadjrowcellccolor = cube.get_center_color_for_rowcell(nextposadjrowcell)

    if nextposadjrowcellccolor == adjrowcellcolor:
        log_utils.log("Current rowcell: " + rowcell + " with adjcolor: " + adjrowcellcolor + " moved to nextpos: "
                      + nextpos + " will solve next pos by matching adjcolor to nextpos adj center color: "
                      + nextposadjrowcellccolor)
        return True

    return False

