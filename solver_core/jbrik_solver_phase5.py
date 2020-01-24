from utils import log_utils
import jbrik_cube
import jbrik_solver_move_lib

# oppface cross orbits solved https://ruwix.com/the-rubiks-cube/how-to-solve-the-rubiks-cube-beginners-method/step-5-swap-yellow-edges/
def solve_crossoppface_orbits(cube):
    facetosolve = 3

    solved = False

    while not solved:
        crosscells = jbrik_cube.get_cross_rowcell_for_face(facetosolve)
        solvedcells = []
        for crosscell in crosscells:
            if not is_rowcell_solved(facetosolve, crosscell, cube):

                tface = facetosolve.__str__()

                # a CW rotation is a leftshift
                if is_nextpos_solved_by_rowcell(facetosolve, crosscell, cube):
                    log_utils.log("A leftshift of rowcell: " + crosscell + " solves the next pos.")

                    # "0.0": ["f", "l", "r"],
                    facemap = jbrik_cube.OPPFACE_CENTERCELL_FACEMAP[crosscell]
                    rface = facemap[2].__str__()

                    # R U R' U R U2 R' U
                    movelist = [rface + "CW1", tface + "CW1", rface + "CC1", tface + "CW1", rface + "CW1",
                                tface + "CW2", rface + "CC1", tface + "CW1", ]

                    for move in movelist:
                        cube = jbrik_solver_move_lib.perform_rotation_str(move, cube)

                elif is_180pos_solved_by_rowcell(facetosolve, crosscell, cube):
                    log_utils.log("A 180shift of rowcell: " + crosscell + " solves the 180 pos.")

                    #destrowcell = jbrik_cube.get_oneeightydswap_targetcell(crosscell)
                    destrowcell = jbrik_cube.get_ninetydswap_targetcell(crosscell, "CW")
                    facemap = jbrik_cube.OPPFACE_CENTERCELL_FACEMAP[destrowcell]
                    rface = facemap[2].__str__()

                    # first a CW1 before calculating faces
                    cube = jbrik_solver_move_lib.perform_rotation_str(tface + "CW1", cube)

                    movelist = [rface + "CW1", tface + "CW1", rface + "CC1", tface + "CW1", rface + "CW1",
                                tface + "CW2", rface + "CC1", tface + "CW1", ]

                    for move in movelist:
                        cube = jbrik_solver_move_lib.perform_rotation_str(move, cube)

                    destrowcell = jbrik_cube.get_oneeightydswap_targetcell(destrowcell)
                    facemap = jbrik_cube.OPPFACE_CENTERCELL_FACEMAP[destrowcell]

                    rface = facemap[2].__str__()
                    movelist = [rface + "CW1", tface + "CW1", rface + "CC1", tface + "CW1", rface + "CW1",
                                tface + "CW2", rface + "CC1", tface + "CW1", ]
                    for move in movelist:
                        cube = jbrik_solver_move_lib.perform_rotation_str(move, cube)

            else:
                solvedcells.append(crosscell)

        if solvedcells.__len__() == 4:
            solved = True

    cube.finalize_solve_phase(5,)
    log_utils.log("Opposite face cross solved")
    return cube

def is_rowcell_solved(facetosolve, rowcell, cube):
    ccolor = cube.get_center_color_for_facenum(facetosolve)

    crosscellcolor = cube.get_cell_val_by_rowcell(rowcell)
    adjrowcell = jbrik_cube.get_adjrowccell_for_rowcell(rowcell)
    adjrowcellcolor = cube.get_cell_val_by_rowcell(adjrowcell)
    adjrowcellccolor = cube.get_center_color_for_rowcell(adjrowcell)

    if crosscellcolor != ccolor or adjrowcellcolor != adjrowcellccolor:
        return False

    return True

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

def is_180pos_solved_by_rowcell(facetosolve, rowcell, cube):
    adjrowcell = jbrik_cube.get_adjrowccell_for_rowcell(rowcell)
    adjrowcellcolor = cube.get_cell_val_by_rowcell(adjrowcell)

    # we know rowcellcolor and ccolor match because we solve that in the last phase
    nextpos = jbrik_cube.get_next_centerpos_for_face_rotation(facetosolve, rowcell, dir="CW")
    nextpos = jbrik_cube.get_next_centerpos_for_face_rotation(facetosolve, nextpos, dir="CW")

    nextposadjrowcell = jbrik_cube.get_adjrowccell_for_rowcell(nextpos)
    nextposadjrowcellccolor = cube.get_center_color_for_rowcell(nextposadjrowcell)

    if nextposadjrowcellccolor == adjrowcellcolor:
        log_utils.log("Current rowcell: " + rowcell + " with adjcolor: " + adjrowcellcolor + " moved to 180pos: "
                      + nextpos + " will solve 180pos by matching adjcolor to nextpos adj center color: "
                      + nextposadjrowcellccolor)
        return True

    return False