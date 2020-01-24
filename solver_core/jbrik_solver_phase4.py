from utils import log_utils
import jbrik_cube
import jbrik_solver_move_lib


# oppface cross faces https://ruwix.com/the-rubiks-cube/how-to-solve-the-rubiks-cube-beginners-method/step-4-yellow-cross/
def face_oppface_cross(cube):
    log_utils.log("Positioning opposite face cross.")
    facetosolve = 3
    ccolor = cube.get_center_color_for_facenum(facetosolve)

    faced = False
    while not faced:
        #determine count of faced crosscells
        facedcelllist = []
        crosscells = jbrik_cube.get_cross_rowcell_for_face(facetosolve)
        for crosscell in crosscells:
            if cube.get_cell_val_by_rowcell(crosscell) == ccolor:
                facedcelllist.append(crosscell)

        if facedcelllist.__len__() == 4:
            faced = True
            break

        alignmenttype = "0"
        tface = facetosolve.__str__()
        fface = "6"
        rface = "4"

        if facedcelllist.__len__() > 1:
            facedcelllist.sort()
            log_utils.log("Solved cells: " + facedcelllist.__str__())
            solvedcells = facedcelllist[0] + " " + facedcelllist[1]

            facemap = jbrik_cube.OPPFACECELL_RFACE_CENTER_ALIGN_MAP[solvedcells]
            alignmenttype = facemap.split(" ")[0]
            tface = facetosolve.__str__()
            fface = facemap.split(" ")[1].__str__()
            rface = facemap.split(" ")[2].__str__()

        # start anywhere with 0 or line
        if alignmenttype != "V":
            log_utils.log("Performing line movelist.")
            # F R U R' U' F'
            movelist = [fface + "CW1", rface + "CW1", tface + "CW1", rface + "CC1", tface + "CC1", fface + "CC1"]

        else:
            # align v to left/top for frontface
            log_utils.log("Performing shortcut V movelist.")
            # F U R U' R' F'
            movelist = [fface + "CW1", tface + "CW1", rface + "CW1", tface + "CC1", rface + "CC1", fface + "CC1"]

        for rmove in movelist:
            cube = jbrik_solver_move_lib.perform_rotation_str(rmove, cube)

    cube.finalize_solve_phase(4,)
    log_utils.log("Opposite face cross positioned")
    return cube

#def is_crosscell_faced
