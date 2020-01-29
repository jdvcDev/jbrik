from utils import log_utils
import jbrik_solver_move_lib
import jbrik_cube

# middlerow https://ruwix.com/the-rubiks-cube/how-to-solve-the-rubiks-cube-beginners-method/step3-second-layer-f2l/
def solve_middle(cube):
    log_utils.log("Starting middle row solve")
    facetosolve = 3

    cyclecount = 1
    solvedcount = get_solved_count(cube)
    solvedcells = get_solved_rowcells(cube)

    solved = are_all_middle_rowcells_solved(cube)
    while not solved:
        log_utils.log("Starting solve cycle: " + cyclecount.__str__())

        presolvedcount = get_solved_count(cube)
        cube = align_oppface_crossrowcell_to_adj_ccolor(facetosolve, cube)
        solvedcount = get_solved_count(cube)
        solvedcells = get_solved_rowcells(cube)

        presolvedcount = get_solved_count(cube)
        cube = perform_lr_solve_on_cross_rowcells(facetosolve, cube)
        solvedcount = get_solved_count(cube)
        solvedcells = get_solved_rowcells(cube)

        # Exhaust all non "destructive" solve algos before munging with existing middle row state
        if presolvedcount != solvedcount:
            cyclecount += 1
            continue

        presolvedcount = get_solved_count(cube)
        cube = swap_backwards_oriented_mid_rowcells(facetosolve, "swap", cube)
        solvedcount = get_solved_count(cube)
        solvedcells = get_solved_rowcells(cube)

        presolvedcount = get_solved_count(cube)
        cube = swap_non_oriented_mid_rowcells_to_top(facetosolve, cube)
        solvedcount = get_solved_count(cube)
        solvedcells = get_solved_rowcells(cube)

        cyclecount +=1
        solved = are_all_middle_rowcells_solved(cube)

    cube.finalize_solve_phase(3,)
    log_utils.log("Middle row is solved")

    return cube

#put a case in here for
def swap_non_oriented_mid_rowcells_to_top(facetosolve, cube):
    # change this to get all mid row cells
    for rowcell in jbrik_cube.MIDDLE_ROWCCELLS:
        rowcellcolor = cube.get_cell_val_by_rowcell(rowcell)
        rowcellccolor = cube.get_center_color_for_rowcell(rowcell)
        adjrowcell = jbrik_cube.get_adjrowccell_for_rowcell(rowcell)
        adjrowcellcolor = cube.get_cell_val_by_rowcell(adjrowcell)
        adjrowcellccolor = cube.get_center_color_for_rowcell(adjrowcell)
        ccolor = cube.get_center_color_for_facenum(facetosolve)

        if (rowcellcolor != rowcellccolor and adjrowcellcolor != adjrowcellccolor and rowcellcolor != ccolor
            and adjrowcellcolor != ccolor) \
           or (rowcellcolor == rowcellccolor and adjrowcellcolor == ccolor):

            log_utils.log("Rowcell: " + rowcell + " is either a total missalign or solved by an LR swap, with "
                                          "cell color: " + rowcellcolor + " and adjacent color: "
                  + adjrowcellcolor)

            movedir = jbrik_cube.get_centerrow_orbit_trans_dir(rowcell)

            # get middle cell in the direction of movement and if it's solved skip this transition
            midlrs = jbrik_cube.MIDDLE_ROWCCELLS_LR_ADJ[rowcell]

            movestrlist = ""
            if movedir == "L":
                if is_middle_rowcell_solved(midlrs.split(" ")[0], cube):
                    return cube

                movestrlist = get_lrcross_solution_list(facetosolve, adjrowcell, rowcell, "L")
            else:
                if is_middle_rowcell_solved(midlrs.split(" ")[1], cube):
                    return cube

                movestrlist = get_lrcross_solution_list(facetosolve, adjrowcell, rowcell, "R")

            movestrlist.append(facetosolve.__str__() + "CW2")

            # one time put is in the right place but reverse
            for i in range(0, 3):
                for rmove in movestrlist:
                    cube = jbrik_solver_move_lib.perform_rotation_str(rmove, cube)

            return cube

    return cube

def get_solved_count(cube):
    count = 0
    for rowcell in jbrik_cube.FIVESIXMIDROWCROSSROWCELLS:
        if is_middle_rowcell_solved(rowcell, cube):
            count += 1

    return count

def get_solved_rowcells(cube):
    solvedcells = []
    for rowcell in jbrik_cube.FIVESIXMIDROWCROSSROWCELLS:
        if is_middle_rowcell_solved(rowcell, cube):
            solvedcells.append(rowcell)

    return solvedcells

def are_all_middle_rowcells_solved(cube):
    for rowcell in jbrik_cube.FIVESIXMIDROWCROSSROWCELLS:
        if not is_middle_rowcell_solved(rowcell, cube):
            return False

    return True

def is_middle_rowcell_solved(rowcell, cube):
    rowcellcolor = cube.get_cell_val_by_rowcell(rowcell)
    rowcellccolor = cube.get_center_color_for_rowcell(rowcell)
    adjrowcell = jbrik_cube.get_adjrowccell_for_rowcell(rowcell)
    adjrowcellcolor = cube.get_cell_val_by_rowcell(adjrowcell)
    adjrowcellccolor = cube.get_center_color_for_rowcell(adjrowcell)

    if rowcellcolor != rowcellccolor or adjrowcellcolor != adjrowcellccolor:
        return False

    return True

def swap_backwards_oriented_mid_rowcells(facetosolve, swaptype, cube):
    for rowcell in jbrik_cube.FIVESIXMIDROWCROSSROWCELLS:
        cube = swap_backwards_oriented_mid_rowcell(facetosolve, rowcell, swaptype, cube)

    return cube

def swap_backwards_oriented_mid_rowcell(facetosolve, rowcell, swaptype, cube):
    rowcellcolor = cube.get_cell_val_by_rowcell(rowcell)
    rowcellccolor = cube.get_center_color_for_rowcell(rowcell)
    adjrowcell = jbrik_cube.get_adjrowccell_for_rowcell(rowcell)
    adjrowcellcolor = cube.get_cell_val_by_rowcell(adjrowcell)
    adjrowcellccolor = cube.get_center_color_for_rowcell(adjrowcell)

    # check orientation
    if rowcellcolor == adjrowcellccolor and adjrowcellcolor == rowcellccolor:
        log_utils.log("Rowcell: " + rowcell + " is backwards oriented, swapping.")
        if jbrik_cube.FIVESIXMIDROWCROSSROWCELLS_L.__contains__(rowcell):
            # its a leftswap
            #movestrlist = get_leftcross_solution_list(facetosolve, adjrowcell, rowcell)
            movestrlist = get_lrcross_solution_list(facetosolve, adjrowcell, rowcell, "L")
            log_utils.log("leftswap " + swaptype + " rowcell: " + rowcell + " of color: " + rowcellccolor + " and adjacent cell: "
                          + adjrowcell + " with color: " + adjrowcellcolor)
        else:
            # its a rightswap
            #movestrlist = get_rightcross_solution_list(facetosolve, adjrowcell, rowcell)
            movestrlist = get_lrcross_solution_list(facetosolve, adjrowcell, rowcell, "R")
            log_utils.log("Rightswap " + swaptype + " rowcell: " + rowcell + " of color: " + rowcellccolor + " and adjacent cell: "
                          + adjrowcell + " with color: " + adjrowcellcolor)

        for rmove in movestrlist:
            cube = jbrik_solver_move_lib.perform_rotation_str(rmove, cube)

        cube = jbrik_solver_move_lib.perform_rotation_str("3CW2", cube)

        if swaptype != "back":
            for rmove in movestrlist:
                cube = jbrik_solver_move_lib.perform_rotation_str(rmove, cube)

    return cube

def align_oppface_crossrowcell_to_adj_ccolor(facetosolve, cube):
    oppfacecrossrowcells = jbrik_cube.get_cross_rowcell_for_face(facetosolve)

    for crossrowcell in oppfacecrossrowcells:
        ccolor = cube.get_center_color_for_facenum(facetosolve)
        rowcellcolor = cube.get_cell_val_by_rowcell(crossrowcell)
        adjrowcell = jbrik_cube.get_adjrowccell_for_rowcell(crossrowcell)
        adjrowcellcolor = cube.get_cell_val_by_rowcell(adjrowcell)
        adjrowcellccolor = cube.get_center_color_for_rowcell(adjrowcell)

        # will be an issue here if all adjcell have ccolor
        if adjrowcellcolor == ccolor or rowcellcolor == ccolor:
            continue

        # if crossrowcellcolor is not facetosolve ccolor then it must be one of the adj ccolors
        testrowcell = adjrowcell
        testrowcellccolor = adjrowcellccolor
        rotcount = 0
        while adjrowcellcolor != testrowcellccolor:
            if rotcount > 3:
                log_utils.log("No solveface alignment.")
                return cube

            log_utils.log("Rotate face: " + facetosolve.__str__()
                          + " CW1 and check for match to adjacent face center color.")
            rotcount = rotcount + 1
            testrowcell = jbrik_cube.get_dest_pos_for_face_rotation(testrowcell, facetosolve.__str__() + "CW1")
            testrowcellccolor = cube.get_center_color_for_rowcell(testrowcell)

        # we've idetified a match, rotate here
        if rotcount > 0:
            rotstr = facetosolve.__str__() + "CW" + rotcount.__str__()
            log_utils.log("Perform transition: " + rotstr)
            cube = jbrik_solver_move_lib.perform_rotation_str(rotstr, cube)

            adjtestrowcell = jbrik_cube.get_adjrowccell_for_rowcell(testrowcell)
            log_utils.log("Solveface orbit rowcell: " + adjtestrowcell + " of color: " + adjrowcellcolor
                          + " is aligned for LR check.")

            cube = perform_lr_solve_on_cross_rowcell(facetosolve, adjtestrowcell, cube)
            return cube

    return cube

def perform_lr_solve_on_cross_rowcells(facetosolve, cube):
    oppfacecrossrowcells = jbrik_cube.get_cross_rowcell_for_face(facetosolve)

    stop = False
    while not stop:
        nochangecount = 0
        for crossrowcell in oppfacecrossrowcells:
            if is_middle_rowcell_solved(crossrowcell, cube):
                nochangecount += 1
                continue
            pre = get_solved_count(cube)
            cube = perform_lr_solve_on_cross_rowcell(facetosolve, crossrowcell, cube)
            post = get_solved_count(cube)

            if pre == post:
                nochangecount += 1

        if are_all_middle_rowcells_solved(cube) or nochangecount == 4:
            stop = True

    return cube

def perform_lr_solve_on_cross_rowcell(facetosolve, crossrowcell, cube):
    crossrowcellcolor = cube.get_cell_val_by_rowcell(crossrowcell)
    adjrowcell = jbrik_cube.get_adjrowccell_for_rowcell(crossrowcell)
    adjrowcellcolor = cube.get_cell_val_by_rowcell(adjrowcell)
    adjrowcellcolorccolor = cube.get_center_color_for_rowcell(adjrowcell)

    # if this rowcell is already aligned with adjacent color same as center color
    if adjrowcellcolor == adjrowcellcolorccolor:
        adjrowcell = jbrik_cube.get_adjrowccell_for_rowcell(crossrowcell)
        lrrowcells = jbrik_cube.get_oppface_centerrowcell_lr_middle_destcells(crossrowcell)
        lcrossrowcell = lrrowcells.split(" ")[0]
        rcrossrowcell = lrrowcells.split(" ")[1]

        lcrossccolor = cube.get_center_color_for_rowcell(lcrossrowcell)
        rcrossccolor = cube.get_center_color_for_rowcell(rcrossrowcell)

        if crossrowcellcolor == lcrossccolor:
            log_utils.log("Perform an L cross solve on: " + crossrowcell)
            solutionlist = get_lrcross_solution_list(facetosolve, lcrossrowcell, adjrowcell, "L")

            for lmove in solutionlist:
                cube = jbrik_solver_move_lib.perform_rotation_str(lmove, cube)

            if not is_middle_rowcell_solved(lcrossrowcell, cube):
                cube = swap_backwards_oriented_mid_rowcell(facetosolve, lcrossrowcell, "swap", cube)

        elif crossrowcellcolor == rcrossccolor:
            log_utils.log("Perform a R cross solve on: " + crossrowcell)
            solutionlist = get_lrcross_solution_list(facetosolve, rcrossrowcell, adjrowcell, "R")

            for rmove in solutionlist:
                cube = jbrik_solver_move_lib.perform_rotation_str(rmove, cube)

            if not is_middle_rowcell_solved(rcrossrowcell, cube):
                cube = swap_backwards_oriented_mid_rowcell(facetosolve, rcrossrowcell, "swap", cube)

    return cube

def get_lrcross_solution_list(facetosolve, rotfacerowcell, frontfacerowcell, dir):
    tface = facetosolve.__str__()
    rotface = jbrik_cube.get_face_for_rowcell(rotfacerowcell).__str__()
    fface = jbrik_cube.get_face_for_rowcell(frontfacerowcell).__str__()

    if dir == "R":
        solutionlist = [tface + "CW1", rotface + "CW1", tface + "CC1", rotface + "CC1", tface + "CC1", fface + "CC1", tface + "CW1", fface + "CW1"]
    else:
        solutionlist = [tface + "CC1", rotface + "CC1", tface + "CW1", rotface + "CW1", tface + "CW1", fface + "CW1", tface + "CC1", fface + "CC1"]

    return solutionlist
