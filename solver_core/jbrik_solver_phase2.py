import log_utils
import move_lib
import jbrik_cube


def solvecrosscorners(cube):
    log_utils.log("Solving cross corners")
    ccolor = cube.get_cell_val_by_rowcell("2.2")
    facetosolve = 1
    oppface = jbrik_cube.oppositefaces[facetosolve]

    cube = move_oppfaceadjring_rowcells_into_o2_and_solve(cube, oppface, ccolor)
    log_utils.log("No more rowcells on opp face adjacent ring with color " + ccolor)

    cube = move_oppface_corner_into_oppfaceadjring(cube, oppface, ccolor)

    while not are_all_crosscorners_solved(cube, facetosolve):
        cube = solvecrosscorners(cube)

    log_utils.log("All cross corners solved.")
    cube.finalize_solve_phase()
    return cube

def move_oppfaceadjring_rowcells_into_o2_and_solve(cube, oppface, ccolor):
    oppfaceadjring = jbrik_cube.faceadjacencies[oppface]

    # identify first, if any rowcells that are centercolor on opp face ring
    log_utils.log("Looking for " + ccolor + " rowcell on opp face adjacent ring")
    for rowcell in oppfaceadjring:
        if cube.get_cell_val_by_rowcell(rowcell) == ccolor:
            log_utils.log(rowcell + " is on opp face adjacent ring and is " + ccolor)
            destrowcell = move_rowcell_to_o2_solve_pos(cube, rowcell, oppface)
            log_utils.log(destrowcell + " is in 2nd order solve position.")
            cube = solvecrosscorner_o2(cube, destrowcell, oppface)

    return cube

def move_oppface_corner_into_oppfaceadjring(cube, oppface, ccolor):
    # we know solveface is one because we're solving the cross, could dynamically figure out though using oppface
    solveface = 1

    oppfaceadjring = jbrik_cube.faceadjacencies[oppface]
    oppfacecornerrowcells = jbrik_cube.get_cornercell_rowcells_for_face(oppface)
    solvefacecornerrowcells = jbrik_cube.get_cornercell_rowcells_for_face(solveface)

    unsolvedcorner = ""
    unsolvedadjfaces = []
    # identify first unsolved corner on solveface
    for solverowcell in solvefacecornerrowcells:
        if not is_crosscorner_solved((cube, solverowcell)):
            log_utils.log(solverowcell + " is not solved")
            unsolvedcorner = solverowcell
            solverowcelladjcells = get_adjrowccell_for_rowcell(solverowcell)
            for solveadjrowcell in solverowcelladjcells:
                unsolvedadjfaces.append(jbrik_cube.get_face_for_rowcell(solveadjrowcell))

        if unsolvedcorner != "":
            break

    # get first cccolor cell on oppface
    for rowcell in oppfacecornerrowcells:
        if cube.get_cell_val_by_rowcell(rowcell) == ccolor:
            log_utils.log("Move : " + rowcell + " to opposite face adjacent ring.")
            adjcell = get_non_oppface_adj_rowcell_for_corner(cube, rowcell, oppface)

            # before determining rotface move rowcell to under unsolved corner
            # rotate oppface unit rowcell shares the same adjfaces as solveadjrowcell
            print("Rotate " + oppface.__str__() + " until " + rowcell + " has adjacent faces: "
                  + unsolvedadjfaces.__str__())
# START FROM HERE


            # rotface need to be the face that puts the unsolved corner onto the oppfaceadjring
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

def are_all_crosscorners_solved(cube, facenum):
    cornerrowcells = jbrik_cube.get_cornercell_rowcells_for_face(facenum)

    for rowcell in cornerrowcells:
        if not is_crosscorner_solved((cube, rowcell)):
            return False
    return True

def is_crosscorner_solved((cube, rowcell)):
    facenum = jbrik_cube.get_face_for_rowcell(rowcell)
    adjrowcellsforface = jbrik_cube.celladjacencies[facenum]

    ccolor = cube.get_center_color_for_facenum(facenum)
    if cube.get_cell_val_by_rowcell(rowcell) != ccolor:
        return False

    adjrowcells = get_adjrowccell_for_rowcell(rowcell)
    for adjrowcell in adjrowcells:
        if cube.get_cell_val_by_rowcell(adjrowcell) != cube.get_center_color_for_rowcell(adjrowcell):
            return False

    '''
    for adjrowcells in adjrowcellsforface:
        if adjrowcells.startswith(rowcell):
            checkrowcells = adjrowcells.split(" ")
            for checkcell in checkrowcells:
                if checkcell == rowcell:
                    continue

                if cube.get_cell_val_by_rowcell(checkcell) != cube.get_center_color_for_rowcell(checkcell):
                    return False
    '''
    return True

def get_adjrowccell_for_rowcell(rowcell):
    returnlist = []

    facenum = jbrik_cube.get_face_for_rowcell(rowcell)
    adjrowcellsforface = jbrik_cube.celladjacencies[facenum]

    for adjrowcells in adjrowcellsforface:
        if adjrowcells.startswith(rowcell):
            checkrowcells = adjrowcells.split(" ")
            for checkcell in checkrowcells:
                if checkcell == rowcell:
                    continue
                returnlist.append(checkcell)

    return returnlist
