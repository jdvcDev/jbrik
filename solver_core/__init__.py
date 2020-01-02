from inspect import currentframe, getframeinfo
import jbrik_solver_phase1
import jbrik_cube
import log_utils
import move_lib

cubeStateStr = "gwboworygggybororbwwwyyoorybybrrgoooywrggbrbrwgybbygww"









def explodemovelist(movelist):
    explodedmovelist = []
    for move in movelist:
        if int(move[3]) > 1:
            for i in range(0, int(move[3])):
                explodedmovelist.append(move[:3] + "1")
        else:
            explodedmovelist.append(move)
    return explodedmovelist

def collapsemovelist(movelist):
    collapsedcount = 0
    collapsedlist = []
    prevmove = "0000"
    for move in movelist:
        if move[:1] == prevmove[:1] and move[1:3] != prevmove[1:3]:
            collapsedlist.pop(collapsedlist.__len__()-1)
            prevmove = collapsedlist[collapsedlist.__len__()-1]
            collapsedcount +=1
        else:
            collapsedlist.append(move)
            prevmove = move

    if collapsedcount > 0:
        collapsedlist = collapsemovelist(collapsedlist)

    return collapsedlist

def dedupemovelist(movelist):
    dupedcount = 0
    dedupedlist = []
    prevmove = movelist[0]
    iter = 0
    for move in movelist:
        if move == prevmove:
            dupedcount +=1
            prevmove = move
        else:
            dedupedlist.append(prevmove[:3] + dupedcount.__str__())
            prevmove = move
            if iter != movelist.__len__():
                dupedcount = 1
        iter +=1

        if iter == movelist.__len__():
            dedupedlist.append(prevmove[:3] + dupedcount.__str__())

    #    if dupecount > 0:
#        collapsedlist = collapsemovelist(collapsedlist)

    return dedupedlist


solvelist = ['2CW1', '4CC1', '3CW2', '4CW1', '2CC1', '3CW3', '2CW1', '4CW1', '3CW2', '4CW2', '5CW2', '2CW1', '3CW3', '2CC1', '2CW1', '2CC1', '2CC1', '3CW1', '2CW1', '2CC1', '3CW3', '2CW1', '6CW2', '1CW1', '4CW2', '3CC2', '2CW2', '3CC2', '4CW2']
explodedlist = explodemovelist(solvelist)

print("orig: " + solvelist.__len__().__str__() + " " + solvelist.__str__())
print("expl: " + explodedlist.__len__().__str__() + " " + explodedlist.__str__())

collaplsedlist = collapsemovelist(explodedlist)
print("coll: " + collaplsedlist.__len__().__str__() + " " + collaplsedlist.__str__())

dedupelist = dedupemovelist(collaplsedlist)
print("dedu: " + dedupelist.__len__().__str__() + " " + dedupelist.__str__())

#simplyfy list

#Cube = jbrik_cube.JbrikCube(cubeStateStr)
#raw_input("\nPress Enter to continue...\n")

#solvedCube = jbrik_solver_phase1.solvecross(Cube)
#print
#solvedCube.print_cube("", True)
#solvedCube.print_solvemap()

