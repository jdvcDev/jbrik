import log_utils
import move_lib
import jbrik_cube


def solvecroscorners(cube):
    log_utils.log("Solving cross corners")
    ccolor = cube.get_cell_val_by_rowcell("2.2")
    facetosolve = 1
    oppface = jbrik_cube.oppositefaces[facetosolve]
    oppfaceadjring = jbrik_cube.faceadjacencies[oppface]

    # identify first, if any rowcells that are centercolor on opp face ring
    log_utils.log("Looking for " + ccolor + " rowcel on opp face adjacent ring")
    for rowcell in oppfaceadjring:
        if cube.get_cell_val_by_rowcell(rowcell) == ccolor:
            log_utils.log(rowcell + " is on opp face adjacent ring and is " + ccolor)

    log_utils.log("No rowcell found on opp face adjacent ring with color " + ccolor)
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




'''rotate until color adj to white corner is matched to center color
rotate on axis of matched color to move unsolved face corner to adj matched face
rotate oppface so that original matched corner is back into pos where matched
unwind faced axis move
'''