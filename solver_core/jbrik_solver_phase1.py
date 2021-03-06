from utils import log_utils
import jbrik_solver_move_lib
import jbrik_cube

# solveface cross https://ruwix.com/the-rubiks-cube/how-to-solve-the-rubiks-cube-beginners-method/step-1-first-layer-edges/
def solvecross(cube):
    log_utils.log("Starting cross solve")

    ccolor = cube.get_cell_val_by_rowcell("2.2")
    facetosolve = 1
    log_utils.log("Center color for face 1: " + ccolor + "\n")

    faced = False
    while not faced:
        # face first order cross cells
        cube = facecross_o1(cube, ccolor, facetosolve)

        # face second order cross cells
        cube = facecross_o2(cube, ccolor, facetosolve)

        # face third order cross cells
        cube = facecross_o3(cube, ccolor, facetosolve)

        if are_all_cross_rowcells_faced(cube, ccolor, facetosolve):
            faced = True

    log_utils.log("Cross is faced")

    # solve first order cross cell, i.e rotate fce
    cube = solve_cross_o1(cube, ccolor, facetosolve)

    # for each remaining unsolved
    cube = solve_cross_o2(cube, ccolor, facetosolve)

    while not are_all_cross_rowcells_solved(cube, ccolor, facetosolve):
        cube = solvecross(cube)

    cube.finalize_solve_phase(1,)
    log_utils.log("Cross is solved")
    return cube

# rotate adj face to face a center cell (repeat until no more exist)
def facecross_o1(cube, ccolor, facetosolve, atomic=False):
    startsolvelen = -1
    while cube.get_current_solve_move_list().__len__() != startsolvelen:
        startsolvelen = cube.get_current_solve_move_list().__len__()

        log_utils.log("Checking for 1st order face transitions for face: " + facetosolve.__str__())

        # check for first order moves
        for rowcell in jbrik_cube.get_cross_rowcell_for_face(facetosolve):
            log_utils.log("Checking state of " + rowcell)
            if cube.get_cell_val_by_rowcell(rowcell) == ccolor:
                log_utils.log(rowcell + " is faced.\n")
                continue
            #can replace some of this
            solvestr = get_facestr_for_cross_rowcell(rowcell, ccolor, cube)
            if solvestr != "" and solvestr is not None:
                log_utils.log(rowcell + " is solved by: " + solvestr)
                log_utils.log("Solve move list: " + cube.get_current_solve_move_list().__str__())
                cube = jbrik_solver_move_lib.perform_rotation_str(solvestr, cube)
                if atomic:
                    return cube
            else:
                log_utils.log("No first order solution for " + rowcell + "\n")

        log_utils.log("Start solve length: " + startsolvelen.__str__() + " solvelist length: "
                      + cube.get_current_solve_move_list().__len__().__str__() + "\n")
        cube.print_cube("", True)
    return cube

# rotate opposite face to align cell then _o1
def facecross_o2(cube, ccolor, facetosolve):
    log_utils.log("Checking for 2nd order face transitions for face: " + facetosolve.__str__())
    opptosolveface = jbrik_cube.OPPOSITEFACES[facetosolve]
    log_utils.log("Face: " + opptosolveface.__str__() + " is opposite to the solving face.")

    o2inposition = False
    for rowcell in jbrik_cube.get_cross_rowcell_for_face(opptosolveface):
        if cube.get_cell_val_by_rowcell(rowcell) == ccolor:
            log_utils.log(rowcell + " is a second order facing transition.")

            #identify the first cell that isn't faced
            for facecell in jbrik_cube.get_cross_rowcell_for_face(facetosolve):
                log_utils.log("Checking state of " + facecell)
                if cube.get_cell_val_by_rowcell(facecell) != ccolor:
                    log_utils.log(facecell + " is not faced, move " + rowcell + " here.\n")

                    for crosscell in jbrik_cube.get_cross_rowcell_for_face(opptosolveface):
                        adjfaceforrowcell = jbrik_cube.get_adj_face_for_rowcell(crosscell)
                        if adjfaceforrowcell == jbrik_cube.get_adj_face_for_rowcell(facecell):
                            log_utils.log("Rotate face: " + opptosolveface.__str__() + " until " + crosscell + " is " + ccolor)
                            break

                    rotcount = 0
                    while cube.get_cell_val_by_rowcell(crosscell) != ccolor:
                        rotcount = rotcount + 1
                        cube = jbrik_solver_move_lib.perform_rotation_str(opptosolveface.__str__() + "CW1", cube, False)
                    if rotcount > 0:
                        movestr = opptosolveface.__str__() + "CW" + rotcount.__str__()
                        log_utils.log("Perform transition: " + movestr)
                        cube.get_current_solve_move_list().append(movestr)
                        cube.print_cube()
                        o2inposition = True
                        break

            cube = facecross_o1(cube, ccolor, facetosolve)
            if o2inposition:
                break

    log_utils.log("No more second order transitions for face: " + facetosolve.__str__())
    return cube

# move cell to middle of adj solve face then to opp face, _o2
def facecross_o3(cube, ccolor, facetosolve):
    unwindlist = []
    resultpos = ""

    # identify the next rowcell that needs to be faced
    for rowcelltoface in jbrik_cube.get_cross_rowcell_for_face(facetosolve):
        log_utils.log("Checking state of " + rowcelltoface)
        if cube.get_cell_val_by_rowcell(rowcelltoface) != ccolor:
            log_utils.log(rowcelltoface + " is the rowcell to face.\n")
            resultpos = rowcelltoface
            break

    if resultpos == "":
        log_utils.log("No more cross positions to face on face: " + facetosolve.__str__())
        return cube

    # identify the first rowcell we can move into resultpos
    opptosolveface = jbrik_cube.OPPOSITEFACES[facetosolve]
    rowcelltomove = ""
    for facenum in range(1, 7):
        log_utils.log("Checking face: " + facenum.__str__() + " for cross cells that can face: " + resultpos)
        if facenum == facetosolve or facenum == opptosolveface:
            log_utils.log("Skipping solve/opp face: " + facenum.__str__())
            continue

        rowcelltomove = get_centerrowcell_of_color_from_face(cube, facenum, ccolor)
        if rowcelltomove != "":
            break

    # rotate rowcell into middle row if needed by checking if CW rotation puts rowcelltomove adj oppface or solveface
    if rowcelltomove != "":
        rotdir = "CW"
        rotface = jbrik_cube.get_face_for_rowcell(rowcelltomove)
        nextpos = jbrik_cube.get_next_centerpos_for_face_rotation(rotface, rowcelltomove)
        resultposadjface = jbrik_cube.get_adj_face_for_rowcell(resultpos)


        # if nextpos is not adj to oppface or solveface we want to go there
        rowcelladjtonextpos = jbrik_cube.get_adjrowccell_for_rowcell(nextpos)
        nextposadjface = jbrik_cube.get_face_for_rowcell(rowcelladjtonextpos)
        if nextposadjface != opptosolveface and nextposadjface != facetosolve:
            # first align resultpos to to the face we want to rotate
            rotcount = 0
            while cube.get_cell_val_by_rowcell(resultpos) == ccolor:
                rotcount = rotcount + 1
                cube = jbrik_solver_move_lib.perform_rotation_str(facetosolve.__str__() + "CW1", cube, False)
            if rotcount > 0:
                movestr = facetosolve.__str__() + "CW" + rotcount.__str__()
                log_utils.log("Perform transition: " + movestr)
                cube.get_current_solve_move_list().append(movestr)

            rotface = jbrik_cube.get_face_for_rowcell(rowcelltomove)
            log_utils.log("Rotating face: " + rotface.__str__() + " " + "CW1 to move: " + rowcelltomove
                          + " into position: " + nextpos + " for next rotation to opposite face.")
            movestr = rotface.__str__() + "CW1"
            cube = jbrik_solver_move_lib.perform_rotation_str(movestr, cube)
            rowcelltomove = nextpos


        # Were in the middle row at this point and in o1 position, either use an o1 transition or use a static move set to find face and move
        if nextposadjface == resultposadjface:
            log_utils.log("Rowcell: " + nextpos + " is in first order solve position for: " + resultpos)
            o1move = jbrik_cube.get_crosscenter_solvface_trans(nextpos)
            cube = jbrik_solver_move_lib.perform_rotation_str(o1move, cube)

            return cube


        # we're in o2 position (solveface rotation) but a non midrow because we're on a 4/6 face
        if jbrik_cube.FIVESIXMIDROWCROSSROWCELLS.__contains__(rowcelltomove):
            log_utils.log(rowcelltomove + " is an o2 position but non mid row because it on a 4/6 face")
            nextposmovestr = jbrik_cube.get_crosscenter_solvface_trans(rowcelltomove)
            resultpos = jbrik_cube.get_dest_pos_for_face_rotation(rowcelltomove, nextposmovestr)

            rotcount = 0
            while cube.get_cell_val_by_rowcell(resultpos) == ccolor:
                rotcount = rotcount + 1
                cube = jbrik_solver_move_lib.perform_rotation_str(facetosolve.__str__() + "CW1", cube, False)
            if rotcount > 0:
                movestr = facetosolve.__str__() + "CW" + rotcount.__str__()
                log_utils.log("Performed transition: " + movestr)
                cube.get_current_solve_move_list().append(movestr)

            # resultpos is now ready to be faced
            cube = jbrik_solver_move_lib.perform_rotation_str(nextposmovestr, cube)

            return cube



        # we're in a middle row but a non o1 position rotate a non face position into the dest cell for nextpos
        if rowcelltomove != opptosolveface and rowcelltomove != facetosolve:
            # identify the destination of the next nextpos rotation
            nextposmovestr = jbrik_cube.get_crosscenter_solvface_trans(rowcelltomove)
            resultpos = jbrik_cube.get_dest_pos_for_face_rotation(rowcelltomove, nextposmovestr)

            rotcount = 0
            while cube.get_cell_val_by_rowcell(resultpos) == ccolor:
                rotcount = rotcount + 1
                cube = jbrik_solver_move_lib.perform_rotation_str(facetosolve.__str__() + "CW1", cube, False)
            if rotcount > 0:
                movestr = facetosolve.__str__() + "CW" + rotcount.__str__()
                log_utils.log("Perform transition: " + movestr)
                cube.get_current_solve_move_list().append(movestr)

            # resultpos is now ready to be faced
            cube = jbrik_solver_move_lib.perform_rotation_str(nextposmovestr, cube)

            return cube

        # we're on the oppface orbit,
        # rotate solveface until rowcelltomove and rowcelltoface share an adjface
        # rotate the adjface until rowcelltoface is ccolor, might be a transition for this get_facetrans_to_resultin_rowcell(rowcelltomove)
        print(" if we made it this far nextpos is on oppface orbit??")


        print("should never get here eject")

    return cube


def get_centerrowcell_of_color_from_face(cube, facenum, ccolor):
    for rowcell in jbrik_cube.get_cross_rowcell_for_face(facenum):
        log_utils.log("Checking state of " + rowcell)
        if cube.get_cell_val_by_rowcell(rowcell) == ccolor:
            return rowcell

    return ""

# TODO this whole method can be replaces by worflow using jbrik_cube.get_crosscenter_solvface_trans(rowcell)
def get_facestr_for_cross_rowcell(rowcell, ccolor, cube):
    log_utils.log("Looking for 1st order facing solution for: " + rowcell)
    adjface = jbrik_cube.get_adj_face_for_rowcell(rowcell)
    log_utils.log(adjface.__str__() + " is the adjacent face for: " + rowcell)
    adjflist = jbrik_cube.CENTERADJACENCIES[adjface]

    rotationcount = 0
    cellidx = adjflist.index(rowcell)

    for i in range(0, cellidx):
        cell = adjflist[i]
        color = cube.get_cell_val_by_rowcell(cell)
        log_utils.log("Rotation: " + rotationcount.__str__() + " checks cell: " + cell + " which has color: " + color)
        if color == ccolor:
            #log_utils.log(cell + " contains the correct color")
            rotstr = adjface.__str__() + "CW" + rotationcount.__str__()
            #log_utils.log(rotstr + " to solve position: " + rowcell)
            if rotationcount > 0:
                return rotstr
            else:
                return ""
        rotationcount = rotationcount + 1

    for j in range(cellidx, 4):
        cell = adjflist[j]
        color = cube.get_cell_val_by_rowcell(cell)
        log_utils.log("Rotation: " + rotationcount.__str__() + " checks cell: " + cell + " which has color: " + color)
        if color == ccolor:
            #log_utils.log(cell + " contains the correct color")
            rotstr = adjface.__str__() + "CW" + rotationcount.__str__()
            #log_utils.log(rotstr + " to solve position: " + rowcell)
            if rotationcount > 0:
                return rotstr
            else:
                return ""
        rotationcount = rotationcount + 1

    return ""

def solve_cross_o1(cube, ccolor, facetosolve):
    print("Solving first order cross")
    colormap = {}
    # identify if any cross rowcell are solved
    for rowcell in jbrik_cube.get_cross_rowcell_for_face(facetosolve):
        adjrowcell = jbrik_cube.get_adjcell_for_rowcell(rowcell)
        adjrowcellcolor = cube.get_adjcell_color_for_center_rowcell(rowcell)
        adjfacecolor = cube.get_center_color_for_rowcell(adjrowcell)
        log_utils.log("Rowcell adjacent to: " + rowcell + " is " + adjrowcell + ", has color: " + adjrowcellcolor
                      + " and has face color: " + adjfacecolor)
        colormap[adjfacecolor] = adjrowcell

        if adjrowcellcolor == adjfacecolor:
            log_utils.log(rowcell + " is solved.  No first order solve needed.")
            return cube

    # work with last rowcell populated
    solverowcell = adjrowcell
    log_utils.log("Solving: " + solverowcell)
    targetrowcell = colormap[adjrowcellcolor]
    log_utils.log("Rotating face: " + facetosolve.__str__() + " until " + solverowcell + "is in position: " + targetrowcell)
    cube = jbrik_solver_move_lib.move_center_rowcell_to_new_pos_onface(solverowcell, targetrowcell, facetosolve, cube)

    return cube

def solve_cross_o2(cube, ccolor, facetosolve):
    log_utils.log("Solving second order cross.")
    for rowcell in jbrik_cube.get_cross_rowcell_for_face(facetosolve):
        targetcellcw = jbrik_cube.get_ninetydswap_targetcell(rowcell, "CW")
        targetcellcc = jbrik_cube.get_ninetydswap_targetcell(rowcell, "CC")
        targetcell180 = jbrik_cube.get_oneeightydswap_targetcell(rowcell)

        if not is_cross_rowcell_solved(rowcell, cube, ccolor):
            log_utils.log(rowcell + " is not solved.")

            log_utils.log("Does a 90deg CW swap targetcell: " + targetcellcw + " need to be solved?")
            if not is_cross_rowcell_solved(targetcellcw, cube, ccolor):
                log_utils.log("90deg CW swap targetcell: " + targetcellcw + " needs to be solved.")
                log_utils.log("Trying a 90 degree CW swap: " + rowcell)
                startmovelen = cube.get_current_solve_move_list()
                cube = jbrik_solver_move_lib.ninetydswap(rowcell, "CW", cube)
                if not is_cross_rowcell_solved(targetcellcw, cube, ccolor):
                    log_utils.log("90 degree CW swap did not solve: " + rowcell)
                    cube = jbrik_solver_move_lib.ninetydswap(targetcellcw, "CC", cube)
                    remove_moves_from_solvelist(startmovelen.__len__() - 1, cube)
                else:
                    log_utils.log("90 degree CW swap solved: " + targetcellcw)
                    continue

            log_utils.log("Does a 90deg CC swap targetcell: " + targetcellcc + " need to be solved?")
            if not is_cross_rowcell_solved(targetcellcc, cube, ccolor):
                log_utils.log("90deg CC swap targetcell: " + targetcellcc + " needs to be solved.")
                log_utils.log("Trying a 90 degree CC swap: " + rowcell)
                startmovelen = cube.get_current_solve_move_list()
                cube = jbrik_solver_move_lib.ninetydswap(rowcell, "CC", cube)
                if not is_cross_rowcell_solved(targetcellcc, cube, ccolor):
                    log_utils.log("90 degree CC swap did not solve: " + rowcell)
                    cube = jbrik_solver_move_lib.ninetydswap(targetcellcc, "CW", cube)
                    remove_moves_from_solvelist(startmovelen.__len__() - 1, cube)
                else:
                    log_utils.log("90 degree CC swap solved: " + targetcellcc)
                    continue

            log_utils.log("Does a 180deg swap targetcell: " + targetcell180 + " need to be solved?")
            if not is_cross_rowcell_solved(targetcell180, cube, ccolor):
                log_utils.log("180deg swap targetcell: " + targetcell180 + " needs to be solved.")
                log_utils.log("Trying a 180 degree swap: " + rowcell)
                startmovelen = cube.get_current_solve_move_list()
                cube = jbrik_solver_move_lib.oneeightydswap(rowcell, cube)
                if not is_cross_rowcell_solved(targetcell180, cube, ccolor):
                    print("This is a problem because we've already checked the other possible solutions EJECT!")
                    # TODO exception
                    exit(1)
                else:
                    log_utils.log("180 degree swap solved: " + targetcell180)
                    continue

        else:
            log_utils.log(rowcell + " is solved.")

    return cube

def is_cross_rowcell_solved(rowcell, cube, ccolor):
    adjrowcell = jbrik_cube.get_adjcell_for_rowcell(rowcell)
    adjrowcellcolor = cube.get_adjcell_color_for_center_rowcell(rowcell)
    adjfacecolor = cube.get_center_color_for_rowcell(adjrowcell)
    rowcellcolor = cube.get_cell_val_by_rowcell(rowcell)
    log_utils.log("Rowcell adjacent to: " + rowcell + " is " + adjrowcell + ", has color: " + adjrowcellcolor
                  + " and has face color: " + adjfacecolor)

    if adjrowcellcolor == adjfacecolor and rowcellcolor == ccolor:
        return True

    return False

#this blow up
def remove_moves_from_solvelist(startmovepos, cube):
    removecount = cube.get_current_solve_move_list().__len__() - startmovepos + 1
    log_utils.log("Removing last " + removecount.__str__() + " moves from solvelist.")

    newlist = []
    for i in range(0, startmovepos+1):
        newlist.append(cube.get_current_solve_move_list()[i])
    cube.currentSolveList = newlist

def are_all_cross_rowcells_solved(cube, ccolor, facetosolve):
    for rowcell in jbrik_cube.get_cross_rowcell_for_face(facetosolve):
        if not is_cross_rowcell_solved(rowcell, cube, ccolor):
            return False

    return True

def are_all_cross_rowcells_faced(cube, ccolor, facetosolve):
    for rowcell in jbrik_cube.get_cross_rowcell_for_face(facetosolve):
        if cube.get_cell_val_by_rowcell(rowcell) != ccolor:
            return False

    return True
