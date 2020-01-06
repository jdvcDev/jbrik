import copy
import log_utils
import jbrik_cube
'''
def get_ninetydswap_targetcell(startrowcell, dir):
    solvingface = jbrik_cube.get_face_for_row(int(startrowcell.split(".")[0]))
    crossrowcells = jbrik_cube.get_cross_rowcell_for_face(solvingface)

    if dir == "CW":
        if crossrowcells.index(startrowcell) == 0:
            targetcell = crossrowcells[2]
        elif crossrowcells.index(startrowcell) == 1:
            targetcell = crossrowcells[0]
        elif crossrowcells.index(startrowcell) == 2:
            targetcell = crossrowcells[3]
        elif crossrowcells.index(startrowcell) == 3:
            targetcell = crossrowcells[1]
    else:
        if crossrowcells.index(startrowcell) == 0:
            targetcell = crossrowcells[1]
        elif crossrowcells.index(startrowcell) == 1:
            targetcell = crossrowcells[3]
        elif crossrowcells.index(startrowcell) == 2:
            targetcell = crossrowcells[0]
        elif crossrowcells.index(startrowcell) == 3:
            targetcell = crossrowcells[2]

    return targetcell

def get_oneeightydswap_targetcell(startrowcell):
    #solvingface = jbrik_cube.get_face_for_row(int(startrowcell.split(".")[0]))
    ninetydest = jbrik_cube.get_ninetydswap_targetcell(startrowcell, "CW")
    oneeightydes = jbrik_cube.get_ninetydswap_targetcell(ninetydest, "CW")

    return oneeightydes
'''
def ninetydswap(startrowcell, dir, cube):
    solvingface = jbrik_cube.get_face_for_row(int(startrowcell.split(".")[0]))
    rotationface = jbrik_cube.get_adj_face_for_rowcell(startrowcell)
    oppositeface = jbrik_cube.oppositefaces[solvingface]

    targetcell = jbrik_cube.get_ninetydswap_targetcell(startrowcell, dir)

    destface = jbrik_cube.get_adj_face_for_rowcell(targetcell)

    log_utils.log("Performing 90 degree " + dir + " swap with rowcell: " + startrowcell)

    # 180 the starting face
    cube = perform_rotation_str(rotationface.__str__() + "CW2", cube)

    # 90 the opposite face
    if dir == "CW":
        cube = perform_rotation_str(oppositeface.__str__() + "CC1", cube)
        unwind2 = oppositeface.__str__() + "CW1"
    else:
        cube = perform_rotation_str(oppositeface.__str__() + "CW1", cube)
        unwind2 = oppositeface.__str__() + "CC1"

    # 180 the dest face to swap rowcells
    cube = perform_rotation_str(destface.__str__() + "CW2", cube)

    # unwind the opposite face
    cube = perform_rotation_str(unwind2, cube)

    # unwind the starting face
    cube = perform_rotation_str(rotationface.__str__() + "CW2", cube)

    return cube

def oneeightydswap(startrowcell, cube):
    solvingface = jbrik_cube.get_face_for_row(int(startrowcell.split(".")[0]))
    rotationface = jbrik_cube.get_adj_face_for_rowcell(startrowcell)
    oppositeface = jbrik_cube.oppositefaces[solvingface]
    destface = jbrik_cube.oppositefaces[rotationface]

    log_utils.log("Performing 180 degree swap with rowcell: " + startrowcell)

    # 180 the starting face
    cube = perform_rotation_str(rotationface.__str__() + "CW2", cube)

    # 180 the opposite face
    cube = perform_rotation_str(oppositeface.__str__() + "CC2", cube)

    # 180 the dest face to swap rowcells
    cube = perform_rotation_str(destface.__str__() + "CW2", cube)

    # unwind the opposite face
    cube = perform_rotation_str(oppositeface.__str__() + "CC2", cube)

    # unwind the starting face
    cube = perform_rotation_str(rotationface.__str__() + "CW2", cube)

    return cube

def reversetransition(transstr):
    if "CW" in transstr:
        return transstr.split("CW")[0] + "CC" + transstr.split("CW")[1]
    else:
        return transstr.split("CC")[0] + "CW" + transstr.split("CC")[1]

# Do this for corners too
def move_center_rowcell_to_new_pos_onface(startpos, endpos,  rotationface, cube):
    if startpos == endpos:
        return cube

    startposcolor = cube.get_cell_val_by_rowcell(startpos)
    startposadjcolor = cube.get_adjcell_color_for_center_rowcell(startpos)

    rotcount = 0
    endposcolor = ""
    endposadjcolor = ""
    while startposcolor != endposcolor or startposadjcolor != endposadjcolor:
        rotcount = rotcount + 1
        cube = perform_rotation_str(rotationface.__str__() + "CW1", cube, False)
        endposcolor = cube.get_cell_val_by_rowcell(endpos)
        endposadjcolor = cube.get_adjcell_color_for_center_rowcell(endpos)
    if rotcount > 0:
        cube.get_current_solve_move_list().append(rotationface.__str__() + "CW" + rotcount.__str__())
        cube.print_cube("", True)

    return cube

# rotates a face
def perform_rotation(facenum, dir, oldcube):
    log_utils.log("Rotating facenum: " + facenum.__str__() + " " + dir)

    newcube = copy.deepcopy(oldcube)

    # front transitions
    ftranslist = jbrik_cube.get_transitions_for_frontface(facenum, dir)
    #log_utils.log("front rotations: " + ftranslist.__str__())
    perform_transitions(oldcube, newcube, ftranslist)

    # side transitions
    translist = jbrik_cube.get_transitions_for_face(facenum, dir)
    #log_utils.log("side rotations: " + translist.__str__())
    perform_transitions(oldcube, newcube, translist)
    #newcube.print_cube("", True)

    return newcube

def perform_rotation_str(rotstr, oldcube, writemove=True):
    log_utils.log("Performing rotation string: " + rotstr)
    facenum = rotstr[0]
    dir = rotstr[1] + rotstr[2]
    count = rotstr[3]

    for i in range(int(count)):
        oldcube = perform_rotation(int(facenum), dir, oldcube)

    if writemove:
        oldcube.get_current_solve_move_list().append(rotstr)
    oldcube.print_cube("", True)
    #raw_input("\nPress Enter to continue...\n")
    return oldcube

# update cube values for a string of moves
def perform_transitions(oldcube, newcube, translist):
    #    iter = 0;
    for trans in translist:
        startpos = trans.split(" ")[0]
        endpos = trans.split(" ")[1]
        val = oldcube.get_cell_val_by_rowcell(startpos)

        row = endpos.split(".")[0]
        cell = endpos.split(".")[1]

        #log_utils.log("transitioning: " + val + " in " + startpos + " to " + endpos)
        newcube.set_cell_val(row, cell, val)