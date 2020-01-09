import log_utils
import move_lib
import jbrik_cube

def solve_middle(cube):
    log_utils.log("Starting middle row solve")
    facetosolve = 3

    #check for an lr solution first
    cube = perform_lr_solve_on_rowcell(cube, facetosolve)

    # for each oppface crossrowcell
    # rotate until rowcell adjacent to crossrowcell is alignined with center color
    cube = align_oppface_crossrowcell_to_adj_ccolor(facetosolve, cube)

    # check if crossrowcell matches color on either left or right face, build a static mapping to determin comparison
#    if crossrowcell != "":
#        cube = perform_lr_solve_on_rowcell(cube)

    # if matched, perform either left or right solve algo
    # if not continue to next color

    return cube

# TODO will need to determine how to enter this method in a way that will stop us from infinite looping when there is no
# lr solution, i.e we might just find the same match again.
def align_oppface_crossrowcell_to_adj_ccolor(facetosolve, cube):
    oppfacecrossrowcells = jbrik_cube.get_cross_rowcell_for_face(facetosolve)

    for crossrowcell in oppfacecrossrowcells:
#        if crossrowcell == "8.1":
#            continue
        ccolor = cube.get_center_color_for_facenum(facetosolve)
        adjrowcell = jbrik_cube.get_adjrowccell_for_rowcell(crossrowcell)
        adjrowcellcolor = cube.get_cell_val_by_rowcell(adjrowcell)
        adjrowcellcolorccolor = cube.get_center_color_for_rowcell(adjrowcell)

        # will be an issue here if all adjcell have ccolor
        if adjrowcellcolor == ccolor:
            continue

# TODO need to not rotate but instead check destination because we may not find a solution for the face
        rotcount = 0
        while adjrowcellcolor != adjrowcellcolorccolor:
            log_utils.log("Rotate face: " + facetosolve.__str__()
                          + " CW1 and check for match to adjacent face center color.")
            rotcount = rotcount + 1
            cube = move_lib.perform_rotation_str(facetosolve.__str__() + "CW1", cube, False)
            adjrowcellcolor = cube.get_cell_val_by_rowcell(adjrowcell)

        if rotcount > 0:
            movestr = facetosolve.__str__() + "CW" + rotcount.__str__()
            log_utils.log("Perform transition: " + movestr)
            cube.get_current_solve_move_list().append(movestr)

        log_utils.log("Solveface orbit towcell: " + adjrowcell + " of color: " + adjrowcellcolor
                      + " is aligned for LR check.")
        return cube

    return cube

def perform_lr_solve_on_rowcell(cube, facetosolve):
    oppfacecrossrowcells = jbrik_cube.get_cross_rowcell_for_face(facetosolve)

    for crossrowcell in oppfacecrossrowcells:
        crossrowcellcolor = cube.get_cell_val_by_rowcell(crossrowcell)
        adjrowcell = jbrik_cube.get_adjrowccell_for_rowcell(crossrowcell)
        adjrowcellcolor = cube.get_cell_val_by_rowcell(adjrowcell)
        adjrowcellcolorccolor = cube.get_center_color_for_rowcell(adjrowcell)

        if adjrowcellcolor == adjrowcellcolorccolor:
            adjrowcell = jbrik_cube.get_adjrowccell_for_rowcell(crossrowcell)
            lrrowcells = jbrik_cube.get_oppface_centerrowcell_lr_middle_destcells(crossrowcell)
            lcrossrowcell = lrrowcells.split(" ")[0]
            rcrossrowcell = lrrowcells.split(" ")[1]
            lface =jbrik_cube.get_face_for_rowcell(lcrossrowcell).__str__()
            rface = jbrik_cube.get_face_for_rowcell(rcrossrowcell).__str__()
            fface = jbrik_cube.get_face_for_rowcell(adjrowcell).__str__()
            tface = facetosolve.__str__()

            lcrossccolor = cube.get_center_color_for_rowcell(lcrossrowcell)
            rcrossccolor = cube.get_center_color_for_rowcell(rcrossrowcell)

            if crossrowcellcolor == lcrossccolor:
                log_utils.log("Perform an L cross solve.")
                # 3 = tface
                # 2 = lface
                # 6 = fface
                # 3CC 2CC 3CW 2CW 3CW 6CW 3CC 6CC
                solutionlist = [tface + "CC1", lface + "CC1", tface + "CW1", lface + "CW1", tface + "CW1", fface + "CW1", tface + "CC1", fface + "CC1"]

                for move in solutionlist:
                    cube = move_lib.perform_rotation_str(move, cube)

                return cube

            if crossrowcellcolor == rcrossccolor:
                log_utils.log("Perform a R cross solve.")
                return cube


    return cube

