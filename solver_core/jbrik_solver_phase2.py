from utils import log_utils
import jbrik_solver_move_lib
import jbrik_cube

def solvecrosscorners(cube):
    log_utils.log("Solving cross corners")
    ccolor = cube.get_cell_val_by_rowcell("2.2")
    facetosolve = 1
    oppface = jbrik_cube.oppositefaces[facetosolve]

    cube = move_oppfaceorbit_rowcells_into_o2_and_solve(cube, oppface, ccolor)

    cube = move_solveface_orbitcells_to_oppface(cube, facetosolve, ccolor)
    cube = move_oppface_corner_into_oppfaceorbit(cube, oppface, ccolor)
    cube = move_oppfaceorbit_rowcells_into_o2_and_solve(cube, oppface, ccolor)

    cube = deface_unsolved_faced_corner(cube, facetosolve, ccolor)

    while not are_all_crosscorners_solved(cube, facetosolve):
        cube = solvecrosscorners(cube)

    log_utils.log("All cross corners solved.")
    if cube.get_current_solve_move_list().__len__() > 0:
        cube.finalize_solve_phase()

    return cube

def deface_unsolved_faced_corner(cube, facetosolve, ccolor):
    cornerrowcells = jbrik_cube.get_cornercell_rowcells_for_face(facetosolve)
    for cornerrowcell in cornerrowcells:
        if cube.get_cell_val_by_rowcell(cornerrowcell) == ccolor and not is_crosscorner_solved((cube, cornerrowcell)):
            log_utils.log(cornerrowcell + " is faced but not solved")
            defacemovestrset = jbrik_cube.get_solveface_corner_oppfaceorbit_trans(cornerrowcell)
            defacemove = defacemovestrset.split(" ")[0]
            defaceunwindmove = jbrik_solver_move_lib.reversetransition(defacemove)
            o2move = defacemovestrset.split(" ")[1]

            log_utils.log("Moving: " + defacemove + " to move " + cornerrowcell + " off solve face.")
            cube = jbrik_solver_move_lib.perform_rotation_str(defacemove, cube)

            log_utils.log("Moving: " + o2move + " to move " + cornerrowcell + " out of unwind move")
            cube = jbrik_solver_move_lib.perform_rotation_str(o2move, cube)

            log_utils.log("Moving: " + defaceunwindmove)
            cube = jbrik_solver_move_lib.perform_rotation_str(defaceunwindmove, cube)

            break

    return cube

def move_solveface_orbitcells_to_oppface(cube, solveface, ccolor):
    solvefaceorbits = jbrik_cube.faceorbits[solveface]
    for orbitrowcell in solvefaceorbits:
        log_utils.log("Checking solveface orbit rowcell: " + orbitrowcell + " for needed transitions.")
        if cube.get_cell_val_by_rowcell(orbitrowcell) == ccolor:
            rotfacedir = jbrik_cube.get_solvefacefaceorbit_o2_trans(orbitrowcell)
            rotface = rotfacedir[0]
            rotdir = rotfacedir[1:3]
            rotstr = rotfacedir + "1"
            unwindmove = jbrik_solver_move_lib.reversetransition(rotstr)

            log_utils.log("Rotate face: " + rotface.__str__() + " " + rotdir + " to move it to opposite solve face.")
            cube = jbrik_solver_move_lib.perform_rotation_str(rotstr, cube)

            oppface = jbrik_cube.oppositefaces[solveface]
            rotstr = oppface.__str__() + "CW1"
            log_utils.log("Rotate oppface: " + rotstr + " to move target cell<???> out of the way of unwind")
            cube = jbrik_solver_move_lib.perform_rotation_str(rotstr, cube)

            log_utils.log("Performing unwind: " + unwindmove)
            cube = jbrik_solver_move_lib.perform_rotation_str(unwindmove, cube)
            break

    return cube


def move_oppfaceorbit_rowcells_into_o2_and_solve(cube, oppface, ccolor):
    oppfaceorbit = jbrik_cube.faceorbits[oppface]

    # identify first, if any rowcells are solvable on oppface orbit
    log_utils.log("Looking for " + ccolor + " rowcell on opp face orbit")
    for rowcell in oppfaceorbit:
        if cube.get_cell_val_by_rowcell(rowcell) == ccolor:
            log_utils.log(rowcell + " is on opp face orbit and is " + ccolor)
            rotstr = get_movestr_to_move_rowcell_to_o2_solve_pos(cube, rowcell, oppface)

            destrowcell = rowcell

            if rotstr != "":
                destradjowcell = jbrik_cube.get_non_oppface_adj_rowcell_for_corner(destrowcell, oppface)
                destrowcell = jbrik_cube.get_dest_pos_for_face_rotation(destradjowcell, rotstr)

                destradjowcell = jbrik_cube.get_non_oppface_adj_rowcell_for_corner(destrowcell, oppface)
                cube = jbrik_solver_move_lib.perform_rotation_str(rotstr, cube)

                log_utils.log(destradjowcell + " is in 2nd order solve position.")
                cube = solvecrosscorner_o2(cube, destradjowcell, oppface)

            else:
                log_utils.log(destrowcell + " is in 2nd order solve position.")
                cube = solvecrosscorner_o2(cube, destrowcell, oppface)

            # recurse
            cube = move_oppfaceorbit_rowcells_into_o2_and_solve(cube, oppface, ccolor)

    return cube

def move_oppface_corner_into_oppfaceorbit(cube, oppface, ccolor):
    # we know solveface is one because we're solving the cross, could dynamically figure out though using oppface
    solveface = 1

    oppfaceorbit = jbrik_cube.faceorbits[oppface]
    oppfacecornerrowcells = jbrik_cube.get_cornercell_rowcells_for_face(oppface)
    solvefacecornerrowcells = jbrik_cube.get_cornercell_rowcells_for_face(solveface)

    unsolvedcorner = ""
    unsolvedadjfaces = []
    # identify first unsolved corner on solveface
    for solverowcell in solvefacecornerrowcells:
        if not is_crosscorner_solved((cube, solverowcell)):
            log_utils.log(solverowcell + " is not solved")
            unsolvedcorner = solverowcell
            solverowcelladjcells = jbrik_cube.get_adjrowccell_for_rowcell(solverowcell)
            for solveadjrowcell in solverowcelladjcells:
                unsolvedadjfaces.append(jbrik_cube.get_face_for_rowcell(solveadjrowcell))

            unsolvedadjfaces.sort()

        if unsolvedcorner != "":
            break

    # get first cccolor cell on oppface
    for rowcell in oppfacecornerrowcells:
        if cube.get_cell_val_by_rowcell(rowcell) == ccolor:
            log_utils.log("Move : " + rowcell + " to opposite face orbit.")
            adjcell = jbrik_cube.get_non_oppface_adj_rowcell_for_corner(rowcell, oppface)

            # before determining rotface move rowcell to under unsolved corner
            # rotate oppface unit rowcell shares the same adjfaces as solveadjrowcell
            for oppfacecornerrowcell in oppfacecornerrowcells:
                destrowcelladjfaces = []
                destrowcelladjrowcells = jbrik_cube.get_adjrowccell_for_rowcell(oppfacecornerrowcell)
                for destrowcelladjrowcell in destrowcelladjrowcells:
                    destrowcelladjfaces.append(jbrik_cube.get_face_for_rowcell(destrowcelladjrowcell))

                destrowcelladjfaces.sort()
                if destrowcelladjfaces == unsolvedadjfaces:
                    break

            log_utils.log("Rotate face: " + oppface.__str__() + " until " + oppfacecornerrowcell + " is color: " + ccolor)
            rotcount = 0
            destrowcell = rowcell
            while destrowcell != oppfacecornerrowcell:
                destrowcell = jbrik_cube.get_next_pos_for_face_rotation(oppface, destrowcell)
                rotcount +=1

            rotstr = oppface.__str__() + "CW" + rotcount.__str__()
            if rotcount > 0:
                cube = jbrik_solver_move_lib.perform_rotation_str(rotstr, cube)

            # pick a face to rotate, doesn't matter which because oppfacecornerrowcell is under an unsolved rowcell
            rotface = unsolvedadjfaces[0]

            # rotface need to be the face that puts the unsolved corner onto the orbit
            rotdir = "CW"
            # try CW rotation
            destrowcell = jbrik_cube.get_next_pos_for_face_rotation(rotface, oppfacecornerrowcell)
            if not oppfaceorbit.__contains__(destrowcell):
                rotdir = "CC"

            rotstr = rotface.__str__() + rotdir + "1"
            unwindmove = jbrik_solver_move_lib.reversetransition(rotstr)
            log_utils.log("Rotate face: " + rotstr + " to put target<??> into position for 2nd order solve.")
            cube = jbrik_solver_move_lib.perform_rotation_str(rotstr, cube)

            log_utils.log("Rotate face: " + oppface.__str__()
                          + " 180 to move target<??> out of the way of the unwind move: " + unwindmove)
            rotstr = oppface.__str__() + rotdir + "2"
            cube = jbrik_solver_move_lib.perform_rotation_str(rotstr, cube)

            log_utils.log("Performing unwind: " + unwindmove)
            cube = jbrik_solver_move_lib.perform_rotation_str(unwindmove, cube)

    return cube


def solvecrosscorner_o2(cube, solverowcell, oppface):
    log_utils.log("Performing 2nd order crosscorner solve for: " + solverowcell)

    rotmstrset = jbrik_cube.get_oppfaceorbit_o2_trans(solverowcell)
    rotstr1 = rotmstrset.split(" ")[0]
    rotstr2 = rotmstrset.split(" ")[1]

    log_utils.log("Rotate face: " + rotstr1 + " to put " + solverowcell + " into position to align with solveface.")
    cube = jbrik_solver_move_lib.perform_rotation_str(rotstr1, cube)
    unwindmove1 = jbrik_solver_move_lib.reversetransition(rotstr1)

    log_utils.log("Rotate face: " + rotstr2 + " to put " + solverowcell + " to align with solveface.")
    cube = jbrik_solver_move_lib.perform_rotation_str(rotstr2, cube)
    unwindmove2 = jbrik_solver_move_lib.reversetransition(rotstr2)

    log_utils.log("Rotate face: " + unwindmove1 + " to unwind first transition")
    cube = jbrik_solver_move_lib.perform_rotation_str(unwindmove1, cube)

    log_utils.log("Rotate face: " + unwindmove2 + " to unwind second transition")
    cube = jbrik_solver_move_lib.perform_rotation_str(unwindmove2, cube)

    return cube

def get_movestr_to_move_rowcell_to_o2_solve_pos(cube, rowcell, oppface):
    log_utils.log("Moving rowcell: " + rowcell + " into position for an order 2 solve.")
    adj = jbrik_cube.get_non_oppface_adj_rowcell_for_corner(rowcell, oppface)
    adjcolor = cube.get_cell_val_by_rowcell(adj)
    adjface = jbrik_cube.get_face_for_rowcell(adj)
    log_utils.log(adj + " is the adjacent rowcell that shares the opposite to solve face is on"
                        " face: " + adjface.__str__() + " and has color: " + adjcolor)
    # rotate while adj color does not match its current location center color
    rotcount = 0
    destrowcell = adj
    while cube.get_center_color_for_rowcell(destrowcell) != adjcolor:
        rotcount += 1
        log_utils.log("perform 90 CW rotation of face: " + oppface.__str__())
        # rotate here and update adj rowcell
        destrowcell = jbrik_cube.get_next_pos_for_face_rotation(oppface, destrowcell)

    if rotcount == 0:
        return ""

    log_utils.log("Rotate opposite to solve face: " + oppface.__str__() + " CW " +
                  rotcount.__str__() + " times to make center color: " +
                  cube.get_center_color_for_rowcell(destrowcell) + " match at " + destrowcell)
    rotstr = oppface.__str__() + "CW" + rotcount.__str__()

    return rotstr

def are_all_crosscorners_solved(cube, facenum):
    cornerrowcells = jbrik_cube.get_cornercell_rowcells_for_face(facenum)

    for rowcell in cornerrowcells:
        if not is_crosscorner_solved((cube, rowcell)):
            return False
    return True

def is_crosscorner_solved((cube, rowcell)):
    facenum = jbrik_cube.get_face_for_rowcell(rowcell)

    ccolor = cube.get_center_color_for_facenum(facenum)
    if cube.get_cell_val_by_rowcell(rowcell) != ccolor:
        return False

    adjrowcells = jbrik_cube.get_adjrowccell_for_rowcell(rowcell)
    for adjrowcell in adjrowcells:
        if cube.get_cell_val_by_rowcell(adjrowcell) != cube.get_center_color_for_rowcell(adjrowcell):
            return False

    return True
