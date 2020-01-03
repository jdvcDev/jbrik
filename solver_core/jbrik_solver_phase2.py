
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
            # do solve


    log_utils.log("No more rowcells on opp face adjacent ring with color " + ccolor)

#rotate until color adj to white corner is matched to center color




    # identify first ccolor on oppface
    # rotate opp face until ccolor rowcell is under unsolved corner
    # rotate on ccolor rowcell adjface so that rowcell moves to oopfaceadjring (mark for unwind)
    # rotate oppface 180
    # unwind marked move
    # rotate oppface until adjring rowcell with ccolor is on same face as center with same color
    # rotate adj face that keeps ccolor rowcell on adj ring (mark for unwind)
    # rotate oppface until cc color rowcell in on axis with other ccolor cells
    # unwind marked move

    return cube

def solvecrosscorner_o2(cube, solverowcell, oppface):
    log_utils.log("Performing 2nd order crosscorner solve for: " + solverowcell)

    adjrowcell = get_non_oppface_adj_rowcell_for_corner(cube, solverowcell, oppface)
    rotface = jbrik_cube.get_face_for_rowcell(adjrowcell)
    log_utils.log("Rotate face: " + rotface.__str__())
    # if in pos .3 rotate CC
    # else rotate CW

# rotate on axis of matched color to move unsolved face corner to adj matched face
# rotate oppface so that original matched corner is back into pos where matched
# unwind faced axis move
    return cube

def move_rowcell_to_o2_solve_pos(cube, rowcell, oppface):
    '''
    rowcellface = cube.get_face_for_rowcell(rowcell)

    log_utils.log(rowcell + " is on face: " + rowcellface.__str__())
    rowcelladjs = jbrik_cube.celladjacencies[rowcellface]
    for rowcelladj in rowcelladjs:
        if rowcelladj.startswith(rowcell):
            log_utils.log(rowcell + " is on the corner: " + rowcelladj)
            for adj in rowcelladj.split(" "):
                if adj != rowcell and cube.get_face_for_rowcell(adj) != oppface:
                    adj = get_non_oppface_adj_rowcell_for_corner(cube, rowcell, oppface)
                    adjcolor = cube.get_cell_val_by_rowcell(adj)
                    adjface = cube.get_face_for_rowcell(adj)
                    log_utils.log(adj + " is the adjacent rowcell that shares the opposite to solve face is on"
                                        " face: " + adjface.__str__() + " and has color: " + adjcolor)
                    # rotate while adj color does not match its current location center color
                    rotcount = 0
                    destrowcell = adj
                    while cube.get_center_color_for_rowcell(adj) != adjcolor:
                    #while cube.get_center_color_for_rowcell(destrowcell) != "b":
                        rotcount += 1
                        log_utils.log("perform 90 CW rotation of face: " + oppface.__str__())
                        # rotate here and update adj rowcell
                        destrowcell = cube.get_next_pos_for_face_rotation(oppface, destrowcell)

                    log_utils.log("Rotate opposite to solve face: " + oppface.__str__() + " CW " +
                                  rotcount.__str__() + " times to make center color: " +
                                  cube.get_center_color_for_rowcell(adj) + " match at " + destrowcell)
                    return destrowcell
    '''
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
        destrowcell = cube.get_next_pos_for_face_rotation(oppface, destrowcell)

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



