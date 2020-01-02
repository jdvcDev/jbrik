import copy
import log_utils
import move_lib
import jbrik_cube

def facecross_o1(cube, ccolor, facetosolve):
    log_utils.log("Checking for 1st order face transitions for face: " + facetosolve.__str__())

    # check for first order moves
    for rowcell in cube.get_cross_rowcell_for_face(facetosolve):
        log_utils.log("Checking state of " + rowcell)
        if cube.get_cell_val_by_rowcell(rowcell) == ccolor:
            log_utils.log(rowcell + " is faced.\n")
            continue
        #can replace some of this
        solvestr = get_facestr_for_cross_rowcell(rowcell, ccolor, cube)
        if solvestr != "" and solvestr is not None:
            log_utils.log(rowcell + " is solved by: " + solvestr)
            log_utils.log("Solve move list: " + cube.get_solve_move_list().__str__())
            cube = move_lib.perform_rotation_str(solvestr, cube)
        else:
            log_utils.log("No first order solution for " + rowcell + "\n")

    return cube

def facecross_o2(cube, ccolor, facetosolve):
    log_utils.log("Checking for 2nd order face transitions for face: " + facetosolve.__str__())
    opptosolveface = jbrik_cube.oppositefaces[facetosolve]
    log_utils.log("Face: " + opptosolveface.__str__() + " is opposite to the solving face.")

    o2inposition = False
    for rowcell in cube.get_cross_rowcell_for_face(opptosolveface):
        if cube.get_cell_val_by_rowcell(rowcell) == ccolor:
            log_utils.log(rowcell + " is a second order facing transition.")

            #identify the first cell that isn't faced
            for facecell in cube.get_cross_rowcell_for_face(facetosolve):
                log_utils.log("Checking state of " + facecell)
                if cube.get_cell_val_by_rowcell(facecell) != ccolor:
                    log_utils.log(facecell + " is not faced, move " + rowcell + " here.\n")
# DO MOVE
# need to move rowcell into first order pos

                    for crosscell in cube.get_cross_rowcell_for_face(opptosolveface):
                        adjfaceforrowcell = cube.get_adj_face_for_rowcell(crosscell)
                        if adjfaceforrowcell == cube.get_adj_face_for_rowcell(facecell):
                            log_utils.log("Rotate face: " + opptosolveface.__str__() + " until " + crosscell + " is " + ccolor)
                            break

                    rotcount = 0
                    while cube.get_cell_val_by_rowcell(crosscell) != ccolor:
                        rotcount = rotcount + 1
                        cube = move_lib.perform_rotation_str(opptosolveface.__str__() + "CW1", cube, False)
                    if rotcount > 0:
                        movestr = opptosolveface.__str__() + "CW" + rotcount.__str__()
                        log_utils.log("Perform transition: " + movestr)
                        cube.get_solve_move_list().append(movestr)
                        cube.print_cube()
                        o2inposition = True
                        break

                    '''
                    solvestr = get_facestr_for_cross_rowcell(rowcell, ccolor, cube)
                    if solvestr != "" and solvestr is not None:
                        log_utils.log(rowcell + " is solved by: " + solvestr)
                        cube = move_lib.perform_rotation_str(solvestr, cube)
                        o2inposition = True
                    '''

            cube = facecross_o1(cube, ccolor, facetosolve)
            if o2inposition:
                break

    log_utils.log("No more second order transitions for face: " + facetosolve.__str__())
    return cube


# cross facing for third order transitions
def facecross_o3(cube, ccolor, facetosolve):
    unwindlist = []
    postoface = ""

    # identify the next rowcell that needs to be faced
    for rowcell in cube.get_cross_rowcell_for_face(facetosolve):
        log_utils.log("Checking state of " + rowcell)
        if cube.get_cell_val_by_rowcell(rowcell) != ccolor:
            log_utils.log(rowcell + " is the rowcell to face.\n")
            postoface = rowcell
            break

    # identify the next rowcell to face
    opptosolveface = jbrik_cube.oppositefaces[facetosolve]
    sourcerowcell = ""
#    sourceface = 0
    for i in range(1, 7):
        log_utils.log("Checking face: " + i.__str__())
        if i == facetosolve:
            continue

        o2faced = False
        for rowcell in cube.get_cross_rowcell_for_face(i):
            log_utils.log("Checking state of " + rowcell)
            if cube.get_cell_val_by_rowcell(rowcell) == ccolor:
                log_utils.log(rowcell + " is the next cell to face in position: " + postoface + "\n")
                sourcerowcell = rowcell
                if cube.get_face_for_row(int(sourcerowcell.split(".")[0])) == opptosolveface:
                    cube = facecross_o2(cube, ccolor, facetosolve)
                    o2faced = True
                    break

                sourceface = i
                break
                # once identified need to stop search

        if o2faced:
            break

        # rotate rowcell into middle row if needed by checking if CW rotation puts sourcerowcell on oppface or solveface
        if sourcerowcell != "":
            rotdir = "CW"
            moveforward90 = False
#            facemiddlerow = (sourceface * 3) - 1
            rotface = cube.get_adj_face_for_rowcell(sourcerowcell)
            nextpos = cube.get_next_pos_for_face_rotation(rotface, sourcerowcell)

            if cube.get_face_for_row(int(nextpos.split(".")[0])) != opptosolveface and \
                    cube.get_face_for_row(int(nextpos.split(".")[0])) != facetosolve:
                rotface = cube.get_face_for_row(int(sourcerowcell.split(".")[0]))
                log_utils.log("Rotating face: " + rotface.__str__() + " " + "CW1 to move: " + sourcerowcell
                              + " into position to rotate to opposite face.")
                movestr = rotface.__str__() + "CW1"
                cube = move_lib.perform_rotation_str(movestr, cube)
                unwindmove = move_lib.reversetransition(movestr)
                unwindlist.append(unwindmove)

                facetrans = cube.get_transitions_for_frontface(rotface, "CW")
                for trans in facetrans:
                    if trans.split(" ")[0] == sourcerowcell:
                        currentpos = trans.split(" ")[1]
                        break

                rotface = cube.get_adj_face_for_rowcell(currentpos)
                nextpos = cube.get_next_pos_for_face_rotation(rotface, currentpos)

            if cube.get_face_for_row(int(nextpos.split(".")[0])) == opptosolveface:
                rotdir = "CW"
                log_utils.log("Rotating face: " + rotface.__str__() + " " + rotdir + "1 to move to opposite solve face.")
            elif cube.get_face_for_row(int(nextpos.split(".")[0])) == facetosolve:
                rotdir = "CC"
                log_utils.log("Rotating face: " + rotface.__str__() + " " + rotdir + "1 to move to opposite solve face.")

            # move sourcerowcell to oppositeface
            movestr = rotface.__str__() + rotdir + "1"
            cube = move_lib.perform_rotation_str(movestr, cube)
            unwindmove = move_lib.reversetransition(movestr)
            unwindlist.append(unwindmove)

            crosscellforoppface = cube.get_cross_rowcell_for_face(opptosolveface)

            # rotate face until its celladj in not one of the unwind moves
            unwindfaces = []
            for move in unwindlist:
                unwindfaces.append(move[0])
            for crosscell in crosscellforoppface:
                adjfaceforrowcell = cube.get_adj_face_for_rowcell(crosscell)
                if not unwindfaces.__contains__(adjfaceforrowcell.__str__()):
    #anywhere we do this kind of move max 4 moves
                    log_utils.log("Rotate face: " + opptosolveface.__str__() + " until " + crosscell + " is " + ccolor)
                    break

            # get the target cell out of the way of the unwind moves
            rotcount = 0
            while cube.get_cell_val_by_rowcell(crosscell) != ccolor:
                rotcount = rotcount + 1
                cube = move_lib.perform_rotation_str(opptosolveface.__str__() + "CW1", cube, False)
            if rotcount > 0:
                movestr = opptosolveface.__str__() + "CW" + rotcount.__str__()
                log_utils.log("Perform transition: " + movestr)
                cube.get_solve_move_list().append(movestr)

            # unwind movetounwind
            unwindlist.reverse()
            for move in unwindlist:
                log_utils.log("Performing unwinding tansition: " + move)
                cube = move_lib.perform_rotation_str(move, cube)

    cube = facecross_o2(cube, ccolor, facetosolve)
    return cube

# TODO rename this
def get_facestr_for_cross_rowcell(rowcell, ccolor, cube):
    log_utils.log("Looking for 1st order facing solution for: " + rowcell)
    adjface = cube.get_adj_face_for_rowcell(rowcell)
    log_utils.log(adjface.__str__() + " is the adjacent face for: " + rowcell)
    adjflist = jbrik_cube.centeradjacencies[adjface]

    rotationcount = 0
    cellidx = adjflist.index(rowcell)

    for i in range(0, cellidx):
        cell = adjflist[i]
        color = cube.get_cell_val_by_rowcell(cell)
        log_utils.log("Rotation: " + rotationcount.__str__() + " checks cell: " + cell + " which has color: " + color)
        if color == ccolor:
#            log_utils.log(cell + " contains the correct color")
            rotstr = adjface.__str__() + "CW" + rotationcount.__str__()
            #log_utils.log(rotstr + " to solve position: " + rowcell)
            if rotationcount > 0:
                return rotstr
            else:
                return
        rotationcount = rotationcount + 1

    for j in range(cellidx, 4):
        cell = adjflist[j]
        color = cube.get_cell_val_by_rowcell(cell)
        log_utils.log("Rotation: " + rotationcount.__str__() + " checks cell: " + cell + " which has color: " + color)
        if color == ccolor:
            #log_utils.log(cell + " contains the correct color")
            rotstr = adjface.__str__() + "CW" + rotationcount.__str__()
 #           log_utils.log(rotstr + " to solve position: " + rowcell)
            if rotationcount > 0:
                return rotstr
            else:
                return
        rotationcount = rotationcount + 1

    return

def solve_cross_o1(cube, ccolor, facetosolve):
    print("Solving first order cross")
    colormap = {}
    # identify if any cross rowcell are solved
    for rowcell in cube.get_cross_rowcell_for_face(facetosolve):
        adjrowcell = cube.get_adjcell_for_rowcell(rowcell)
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
    cube = move_lib.move_center_rowcell_to_new_pos_onface(solverowcell, targetrowcell, facetosolve, cube)

    return cube

def solve_cross_o2(cube, ccolor, facetosolve):
    print("Solving second order cross")
    for rowcell in cube.get_cross_rowcell_for_face(facetosolve):
        targetcell = move_lib.get_ninetydswap_targetcell(rowcell, facetosolve, "CW", cube)

        if not is_cross_rowcell_solved(rowcell, cube, ccolor, facetosolve):
            log_utils.log(rowcell + " is not solved.")
            log_utils.log("Trying a 90 degree CW swap: " + rowcell)
            startmovelen = cube.get_solve_move_list()
            cube = move_lib.ninetydswap(rowcell, "CW", cube)
            if not is_cross_rowcell_solved(targetcell, cube, ccolor, facetosolve):
                log_utils.log("90 degree CW swap did not solve: " + rowcell)
                cube = move_lib.ninetydswap(targetcell, "CC", cube)
                remove_moves_from_solvelist(startmovelen.__len__()-1, cube)

                log_utils.log("Trying a 90 degree CC swap: " + rowcell)
                targetcell = move_lib.get_ninetydswap_targetcell(rowcell, facetosolve, "CC", cube)
                cube = move_lib.ninetydswap(rowcell, "CC", cube)
                if not is_cross_rowcell_solved(targetcell, cube, ccolor, facetosolve):
                    startmovelen = cube.get_solve_move_list()
                    log_utils.log("90 degree CC swap did not solve: " + rowcell)
                    cube = move_lib.ninetydswap(targetcell, "CW", cube)
                    remove_moves_from_solvelist(startmovelen - 1, cube)

                    log_utils.log("Trying a 180 degree swap: " + rowcell)
                    cube = move_lib.oneeightydswap(rowcell, cube)

            else:
                log_utils.log(rowcell + " is solved.")

    return cube

def is_cross_rowcell_solved(rowcell, cube, ccolor, facetosolve):
    adjrowcell = cube.get_adjcell_for_rowcell(rowcell)
    adjrowcellcolor = cube.get_adjcell_color_for_center_rowcell(rowcell)
    adjfacecolor = cube.get_center_color_for_rowcell(adjrowcell)
    log_utils.log("Rowcell adjacent to: " + rowcell + " is " + adjrowcell + ", has color: " + adjrowcellcolor
                  + " and has face color: " + adjfacecolor)

    if adjrowcellcolor == adjfacecolor:
        log_utils.log(rowcell + " is solved.")
        return True

    return False

def remove_moves_from_solvelist(startmovepos, cube):
    removecount = cube.get_solve_move_list().__len__() - startmovepos + 1
    log_utils.log("Removing last " + removecount.__str__() + " moves from solvelist.")
    for i in range(startmovepos, cube.get_solve_move_list().__len__()):
        del cube.get_solve_move_list()[i]





