import log_utils
import move_lib
import jbrik_cube


def solvecrosscorners(cube):
    log_utils.log("Solving cross corners")
    ccolor = cube.get_cell_val_by_rowcell("2.2")
    facetosolve = 1
    oppface = jbrik_cube.oppositefaces[facetosolve]
    oppfaceadjring = jbrik_cube.faceadjacencies[oppface]

    # identify first, if any rowcells that are centercolor on opp face ring
    log_utils.log("Looking for " + ccolor + " rowcell on opp face adjacent ring")
    for rowcell in oppfaceadjring:
        if cube.get_cell_val_by_rowcell(rowcell) == ccolor:
            log_utils.log(rowcell + " is on opp face adjacent ring and is " + ccolor)
            destrowcell = move_rowcell_to_o2_solve_pos(cube, rowcell, oppface)
            log_utils.log(destrowcell + " is in 2nd order solve position.")
            cube = solvecrosscorner_o2(cube, destrowcell, oppface)

    # identify cell on opposite face and move to
    log_utils.log("No more rowcells on opp face adjacent ring with color " + ccolor)

    '''
    oppfacecornerrowcells = jbrik_cube.get_cornercell_rowcells_for_face(oppface)
    for rowcell in oppfacecornerrowcells: # named trans_oppface_corners_into_o2_pos
        # get first white cell on oppface
        if cube.get_cell_val_by_rowcell(rowcell) == ccolor:
            log_utils.log("Move : " + rowcell + " to opposite face adjacent ring.")
            adjcell = get_non_oppface_adj_rowcell_for_corner(cube, rowcell, oppface)
            rotface = jbrik_cube.get_face_for_rowcell(adjcell)
            rotdir = "CW"
            # try CW rotation
            destrowcell = jbrik_cube.get_next_pos_for_face_rotation(rotface, rowcell)
            if not oppfaceadjring.__contains__(destrowcell):
                rotdir = "CC"

            rotstr = rotface.__str__() + rotdir + "1"
            unwindmove = move_lib.reversetransition(rotstr)
            log_utils.log("Rotate face: " + rotstr + "to put " + destrowcell + " into position for 2nd order solve.")
            cube = move_lib.perform_rotation_str(rotstr, cube)

            log_utils.log("Rotate face: " + oppface.__str__() + " 180 to move destrowcell: " + destrowcell
                          + " out of the way of the unwind move: " + unwindmove) # destrowcell wrong here
            rotstr2 = oppface.__str__() + rotdir + "2"
            cube = move_lib.perform_rotation_str(rotstr2, cube)

            log_utils.log("Performing unwind: " + unwindmove) # destrowcell wrong here
            cube = move_lib.perform_rotation_str(unwindmove, cube)

            # should now be in 2nd order solve position
            break
    '''


    #unwind last move

    while not are_all_crosscorners_solved(cube, facetosolve, ccolor):
        cube = solvecrosscorners(cube)

    log_utils.log("All cross corners solved.")
    cube.finalize_solve_phase()
    return cube



def trans_oppface_corner_into_o2_pos(cube, oppface, ccolor):
    oppfaceadjring = jbrik_cube.faceadjacencies[oppface]
    oppfacecornerrowcells = jbrik_cube.get_cornercell_rowcells_for_face(oppface)
    for rowcell in oppfacecornerrowcells: # named trans_oppface_corners_into_o2_pos
        # get first white cell on oppface
        if cube.get_cell_val_by_rowcell(rowcell) == ccolor:
            log_utils.log("Move : " + rowcell + " to opposite face adjacent ring.")
            adjcell = get_non_oppface_adj_rowcell_for_corner(cube, rowcell, oppface)
            rotface = jbrik_cube.get_face_for_rowcell(adjcell)
            rotdir = "CW"
            # try CW rotation
            destrowcell = jbrik_cube.get_next_pos_for_face_rotation(rotface, rowcell)
            if not oppfaceadjring.__contains__(destrowcell):
                rotdir = "CC"

            rotstr = rotface.__str__() + rotdir + "1"
            unwindmove = move_lib.reversetransition(rotstr)
            log_utils.log("Rotate face: " + rotstr + "to put " + destrowcell + " into position for 2nd order solve.")
            cube = move_lib.perform_rotation_str(rotstr, cube)

            log_utils.log("Rotate face: " + oppface.__str__() + " 180 to move destrowcell: " + destrowcell
                          + " out of the way of the unwind move: " + unwindmove) # destrowcell wrong here
            rotstr2 = oppface.__str__() + rotdir + "2"
            cube = move_lib.perform_rotation_str(rotstr2, cube)

            log_utils.log("Performing unwind: " + unwindmove)
            cube = move_lib.perform_rotation_str(unwindmove, cube)

            # should now be in 2nd order solve position
            return cube

def solvecrosscorner_o2(cube, solverowcell, oppface):
    log_utils.log("Performing 2nd order crosscorner solve for: " + solverowcell)

    adjrowcell = get_non_oppface_adj_rowcell_for_corner(cube, solverowcell, oppface)
    rotface = jbrik_cube.get_face_for_rowcell(adjrowcell)
    rotdir = "CW"
    if solverowcell.split(".")[1] == "3":
        rotdir = "CC"

    rotstr = rotface.__str__() + rotdir + "1"
    log_utils.log("Rotate face: " + rotstr + " to put " + solverowcell + " into position to align with solveface.")
    cube = move_lib.perform_rotation_str(rotstr, cube)
    unwindmove = move_lib.reversetransition(rotstr)

    rotstr2 = oppface.__str__() + rotdir + "1"
    log_utils.log("Rotate face: " + rotstr2 + " to align " + solverowcell + " solveface.") # no accurate info
    cube = move_lib.perform_rotation_str(rotstr2, cube)

    log_utils.log("Rotate face: " + unwindmove + " to solve corner")
    cube = move_lib.perform_rotation_str(unwindmove, cube)

    return cube

def move_rowcell_to_o2_solve_pos(cube, rowcell, oppface):
    adj = get_non_oppface_adj_rowcell_for_corner(cube, rowcell, oppface)
    adjcolor = cube.get_cell_val_by_rowcell(adj)
    adjface = jbrik_cube.get_face_for_rowcell(adj)
    log_utils.log(adj + " is the adjacent rowcell that shares the opposite to solve face is on"
                        " face: " + adjface.__str__() + " and has color: " + adjcolor)
    # rotate while adj color does not match its current location center color
    rotcount = 0
    destrowcell = adj
    while cube.get_center_color_for_rowcell(adj) != adjcolor:
        rotcount += 1
        log_utils.log("perform 90 CW rotation of face: " + oppface.__str__())
        # rotate here and update adj rowcell
        destrowcell = jbrik_cube.get_next_pos_for_face_rotation(oppface, destrowcell)

    log_utils.log("Rotate opposite to solve face: " + oppface.__str__() + " CW " +
                  rotcount.__str__() + " times to make center color: " +
                  cube.get_center_color_for_rowcell(adj) + " match at " + destrowcell)
    return destrowcell

def get_non_oppface_adj_rowcell_for_corner(cube, rowcell, oppface):
    rowcellface = jbrik_cube.get_face_for_rowcell(rowcell)

    log_utils.log(rowcell + " is on face: " + rowcellface.__str__())
    rowcelladjs = jbrik_cube.celladjacencies[rowcellface]
    for rowcelladj in rowcelladjs:
        if rowcelladj.startswith(rowcell):
            log_utils.log(rowcell + " is on the corner: " + rowcelladj)
            for adj in rowcelladj.split(" "):
                if adj != rowcell and jbrik_cube.get_face_for_rowcell(adj) != oppface:
                    return adj

def are_all_crosscorners_solved(cube, facenum, ccolor):
    cornerrowcells = jbrik_cube.get_cornercell_rowcells_for_face(facenum)
    for rowcell in cornerrowcells:
        if cube.get_cell_val_by_rowcell(rowcell) != ccolor:
            return False

    return True



