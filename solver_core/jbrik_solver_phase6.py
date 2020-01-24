from utils import log_utils
import jbrik_cube
import jbrik_solver_move_lib


# oppface corners corners positioned https://ruwix.com/the-rubiks-cube/how-to-solve-the-rubiks-cube-beginners-method/step-6-position-yellow-corners/
def position_oppface_corners(cube):
    log_utils.log("Positioning oppface corners.")
    facetosolve = 3

    solved = False
    while not solved:
        positionedrowcell = ""
        cornercelladjfacelist = []

        # identify a corner thats positioned correctly, 3 face colors sorted = 3 center colors sorted
        for cornerrowcell in jbrik_cube.get_cornercell_rowcells_for_face(facetosolve):
            if is_corner_positioned(cornerrowcell, cube):
                log_utils.log("Rowcell: " + cornerrowcell + " is positioned correctly.")
                positionedrowcell = cornerrowcell
                break

        # orient so that this corner is front top right, we can map this,
        # nothing is positioned do algo on any random corner
        cornercelladjfacelist = jbrik_cube.OPPFACE_CELL_FACE_MAP.get("7.1")
        if positionedrowcell != "":
            # otherwise do it the positioned corner
            cornercelladjfacelist = jbrik_cube.OPPFACE_CELL_FACE_MAP[positionedrowcell]
            log_utils.log("Adjacent faces for " + positionedrowcell + ": " + cornercelladjfacelist.__str__())

        # if 7.1 f=2, t=3, l=5, r=6
        tface = facetosolve.__str__()
        fface = cornercelladjfacelist[0].__str__()
        lface = cornercelladjfacelist[2].__str__()
        rface = cornercelladjfacelist[3].__str__()

        # perform this algorith
        # URU'L'UR'U'L
        movelist =  [tface + "CW1", rface + "CW1", tface + "CC1", lface + "CC1", tface + "CW1", rface + "CC1", tface + "CC1", lface + "CW1"]
        log_utils.log("Constructed movelist: " + movelist.__str__())

        for rmove in movelist:
            cube = jbrik_solver_move_lib.perform_rotation_str(rmove, cube)

        # will only take 3 cycles because only 2 possible states
        # no corner positioned = 2 cycles
        # 1 corner positioned = 1 cycles
        # 4 corners positioned = no cycles
        if are_all_corners_positioned(facetosolve, cube):
            solved = True

    cube.finalize_solve_phase(6,)
    log_utils.log("Opposite face corners positioned")
    return cube

def is_corner_positioned(cornerrowcell, cube):
    cornerrowcellface = jbrik_cube.get_face_for_rowcell(cornerrowcell)

    # get adjrowcelllist for corner
    rowcellfaceorbitscells = jbrik_cube.CELLADJENCIES[cornerrowcellface]
    for orbitcells in rowcellfaceorbitscells:
        celllist = orbitcells.split(" ")
        cornercellcolors = []
        cornercellccolors = []
        if len(celllist) != 3:
            continue

        if celllist[0] == cornerrowcell or celllist[1] == cornerrowcell or celllist[2] == cornerrowcell:
            for rowcell in celllist:
                cornercellccolors.append(cube.get_center_color_for_rowcell(rowcell))
                cornercellcolors.append(cube.get_cell_val_by_rowcell(rowcell))

            cornercellcolors.sort()
            cornercellccolors.sort()
            if cornercellcolors == cornercellccolors:
                return True

    return False

def are_all_corners_positioned(facetosolve, cube):
    for cornerrowcell in jbrik_cube.get_cornercell_rowcells_for_face(facetosolve):
        if not is_corner_positioned(cornerrowcell, cube):
            return False

    return True
