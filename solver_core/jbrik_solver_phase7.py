from utils import log_utils
import jbrik_cube
import jbrik_solver_move_lib

# oppface corners solved https://ruwix.com/the-rubiks-cube/how-to-solve-the-rubiks-cube-beginners-method/orient-yellow-corners-how-to-solve-last-layer-corner/
def solve_oppface_corners(cube):
    log_utils.log("Solving opposite face corners.")
    facetosolve = 3
    ccolor = cube.get_center_color_for_facenum(facetosolve)

    solved = False
    while not solved:
        unsolvedcornerlist = []
        for cornerrowcell in jbrik_cube.get_cornercell_rowcells_for_face(facetosolve):
            if not is_corner_solved(cornerrowcell, ccolor, cube):
                unsolvedcornerlist.append(cornerrowcell)

        if unsolvedcornerlist.__len__() != 0:
            unsolvedcornerlist.sort()
            if unsolvedcornerlist.__len__() == 4:
                unsolvedcorners = unsolvedcornerlist[0] + " " + unsolvedcornerlist[1] + " " + unsolvedcornerlist[2] + " " + unsolvedcornerlist[3]
            elif unsolvedcornerlist.__len__() == 3:
                unsolvedcorners = unsolvedcornerlist[0] + " " + unsolvedcornerlist[1] + " " + unsolvedcornerlist[2]
            elif unsolvedcornerlist.__len__() == 2:
                unsolvedcorners = unsolvedcornerlist[0] + " " + unsolvedcornerlist[1]
            elif unsolvedcornerlist.__len__() == 1:
                print("investigate this case")

            # orient so that (top) oppface front right corner is unsolved (as well as the front left corner) if you can get both
            # find right hand face for solved rowcell combo
            tface = facetosolve.__str__()
            bface = "1"
            rface = jbrik_cube.oppfacecell_rface_corner_align_map[unsolvedcorners].split(" ")[0].__str__()
            cornertosolve = jbrik_cube.oppfacecell_rface_corner_align_map[unsolvedcorners].split(" ")[1]

            # special case where solved rows are opposites
            if unsolvedcorners == "7.1 9.3" or unsolvedcorners == "7.3 9.1":
                # rotate once to move unsolved corner into top/front/right
                cube = jbrik_solver_move_lib.perform_rotation_str(tface + "CW1", cube)

            # do this algo 2, check for solve
            # if not solved, 2 more times
            # rotate top until next unsolved corner is in front top right
            # (R' D' R D) x2/4 + u inbetween and after
            movelist = [rface + "CC1", bface + "CC1", rface + "CW1", bface + "CW1"]

            for i in range(0, unsolvedcornerlist.__len__()):
                # after 2 check for solve,
                attemptcount = 0
                '''
                while attemptcount < 2:
                    cube = attempt_corner_solve(movelist, cube)
                    attemptcount += 1
                if not is_corner_solved(cornertosolve, ccolor, cube):
                    attemptcount = 0
                    while attemptcount < 2:
                        cube = attempt_corner_solve(movelist, cube)
                        attemptcount += 1

                '''
                while not is_corner_solved(cornertosolve, ccolor, cube) and attemptcount < 2:
                    cube = attempt_corner_solve(movelist, cube)
                    attemptcount += 1

                # final rotation
                cube = jbrik_solver_move_lib.perform_rotation_str(tface + "CW1", cube)

                # rotate until next unsolved is in top/front/right, never more than 2 turns
                attemptcount = 0
                while is_corner_solved(cornertosolve, ccolor, cube) and attemptcount < 2:
                    cube = jbrik_solver_move_lib.perform_rotation_str(tface + "CW2", cube)
                    attemptcount += 1

        else:
            solved = True

    cube.finalize_solve_phase(7,)
    log_utils.log("Opposite face corners solved.")
    return cube

def attempt_corner_solve(movelist, cube):
    for i in range(0, 2):
        for rmove in movelist:
            cube = jbrik_solver_move_lib.perform_rotation_str(rmove, cube)

    return cube

def is_corner_solved(rowcell, ccolor, cube):
    if cube.get_cell_val_by_rowcell(rowcell) == ccolor:
        return True

    return False

def are_all_corners_solved(cube, facetosolve):
    ccolor = cube.et_center_color_for_facenum(facetosolve)

    for cornerrowcell in jbrik_cube.get_cornercell_rowcells_for_face(facetosolve):
        if not is_corner_solved(cornerrowcell, ccolor, cube):
            return False

    return True

