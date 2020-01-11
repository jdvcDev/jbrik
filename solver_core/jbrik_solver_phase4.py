from utils import log_utils
import jbrik_cube
import jbrik_solver_move_lib


# oppface cross faces https://ruwix.com/the-rubiks-cube/how-to-solve-the-rubiks-cube-beginners-method/step-4-yellow-cross/
def face_oppface_cross(cube):
    log_utils.log("Positioning opposite face cross.")
    facetosolve = 3
    ccolor = cube.get_center_color_for_facenum(facetosolve)

    solved = False
    while not solved:
        #determine count of faced crosscells
        solvedcelllist = []
        crosscells = jbrik_cube.get_cross_rowcell_for_face(facetosolve)
        for crosscell in crosscells:
            if cube.get_cell_val_by_rowcell(crosscell) == ccolor:
                solvedcelllist.append(crosscell)

        if solvedcelllist.__len__() == 4:
            solved = True
            break

        alignmenttype = "0"
        tface = facetosolve.__str__()
        fface = "6"
        rface = "4"

        if solvedcelllist.__len__() != 0:
            solvedcelllist.sort()
            log_utils.log("Solved cells: " + solvedcelllist.__str__())
            solvedcells = solvedcelllist[0] + " " + solvedcelllist[1]

            facemap = jbrik_cube.oppfacecell_rface_center_align_map[solvedcells]
            alignmenttype = facemap.split(" ")[0]
            tface = facetosolve.__str__()
            fface = facemap.split(" ")[1].__str__()
            rface = facemap.split(" ")[2].__str__()

        # start anywhere with 0 or line
        if alignmenttype != "V":
            log_utils.log("Performing line movelist.")
            # F R U R' U' F'
            movelist = [fface + "CW1", rface + "CW1", tface + "CW1", rface + "CC1", tface + "CC1", fface + "CC1"]
#            for rmove in movelist:
#                cube = jbrik_solver_move_lib.perform_rotation_str(rmove, cube)

        else:
            # align v to left/top for frontface
            #if alignmenttype == "V":
            log_utils.log("Performing shortcut V movelist.")
            # F U R U' R' F'
            movelist = [fface + "CW1", tface + "CW1", rface + "CW1", tface + "CC1", rface + "CC1", fface + "CC1"]

        for rmove in movelist:
            cube = jbrik_solver_move_lib.perform_rotation_str(rmove, cube)

    cube.finalize_solve_phase()
    log_utils.log("Opposite face cross positioned")
    return cube

#def is_crosscell_faced
