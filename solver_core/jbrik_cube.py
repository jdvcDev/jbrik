import log_utils
import jbrik_solver_phase1
import copy

# for reverse transition read transition chain backwards
facetransitions = {
    1: ["1.3", "2.3", "3.3"],
    2: ["1.2", "2.2", "3.2"],
    3: ["1.1", "2.1", "3.1"]
}
transitions = {
    1: ["4.1 16.3", "4.2. 17.3", "4.3 18.3", "16.3 12.3", "17.3 12.2", "18.3 12.1", "12.1 13.1", "12.2 14.1", "12.3 15.1", "13.1 4.3", "14.1 4.2", "15.1 4.1"],
    2: ["7.1 18.3", "7.2 18.2", "7.3 18.1", "18.1 3.1", "18.2 3.2", "18.3 3.3", "3.1 15.1", "3.2 15.2", "3.3 15.3", "15.1 7.3", "15.2 7.2", "15.3 7.1"],
    3: ["10.1 18.1", "10.2 17.1", "10.3 16.1", "16.1 6.1", "17.1 6.2", "18.1 6.3", "6.1 15.3", "6.2 14.3", "6.3 13.3", "13.3 10.1", "14.3 10.2", "15.3 10.3"],
    4: ["1.1 16.1", "1.2 16.2", "1.3 16.3", "16.1 9.3", "16.2 9.2", "16.3 9.1", "9.1 13.3", "9.2 13.2", "9.3 13.1", "13.1 1.1", "13.2 1.2", "13.3 1.3"],
    5: ["4.3 1.3", "5.3 2.3", "6.3 3.3", "1.3 10.3", "2.3 11.3", "3.3 12.3", "10.3 7.3", "11.3 8.3", "12.3 9.3", "7.3 4.3", "8.3 5.3", "9.3 6.3"],
    6: ["4.1 7.1", "5.1 8.1", "6.1 9.1", "7.1 10.1", "8.1 11.1", "9.1 12.1", "10.1 1.1", "11.1 2.1", "12.1 3.1", "1.1 4.1", "2.1 5.1", "3.1 6.1"]
}
celladjacencies = {
    1: ["1.1 12.1 16.3", "1.2 12.2", "1.3 12.3 13.1" , "2.1 17.3", "2.2 X", "2.3 14.1", "3.1 4.1 18.3", "3.2 4.2", "3.3 4.3 15.1"],
    2: ["4.1 3.1 18.3", "4.2 3.2", "4.3 3.3 15.1", "5.1 18.2", "5.2 X", "5.3 15.2", "6.1 7.1 18.1", "6.2 7.2", "6.3 7.3 15.3"],
    3: ["7.1 6.1 18.1", "7.2 6.2", "7.3 6.3 15.3", "8.1 17.1", "8.2 X", "8.3 14.3", "9.1 10.1 16.1", "9.2 10.2", "9.3 10.3 13.3"],
    4: ["10.1 9.1 16.1", "10.2 9.2", "10.3 9.3 13.3", "11.1 16.2", "11.2 X", "11.3 13.2", "12.1 1.1 16.3", "12.2 1.2", "12.3 1.3 13.1"],
    5: ["13.1 1.2 12.3", "13.2 11.1", "13.3 9.3 10.3", "14.1 2.3", "14.2 X", "14.3 8.3", "15.1 3.3 4.3", "15.2 5.3", "15.3 6.3 7.3"],
    6: ["16.1 9.1 10.1", "16.2 11.1", "16.3 1.1 12.1", "17.1 8.1", "17.2 X", "17.3 2.1", "18.1 7.1 6.1", "18.2 5.1", "18.3 3.1 4.1"]
}
faceadjacencies = {
    1: ["4.1", "4.2", "4.3", "12.1", "12.2", "12.3", "13.1", "14.1", "15.1", "16.3", "17.3", "18.3"],
    2: ["3.1", "3.2", "3.3", "7.1", "7.2", "7.3", "15.1", "15.2", "15.3", "18.1", "18.2", "18.3"],
    3: ["6.1", "6.2", "6.3", "10.1", "10.2", "10.3", "13.3", "14.3", "15.3", "16.1", "17.1", "18.1"],
    4: ["1.1", "1.2", "1.3", "9.1", "9.2", "9.3", "13.1", "13.2", "13.3", "16.1", "16.2", "16.3"],
    5: ["1.3", "2.3", "3.3", "4.3", "5.3", "6.3", "7.3", "8.3", "9.3", "10.3", "11.3", "12.3"],
    6: ["1.1", "2.1", "3.1", "4.1", "5.1", "6.1", "7.1", "8.1", "9.1", "10.1", "11.1", "12.1"]
}
# ordered by CW rotation
centeradjacencies = {
    1: ["4.2","14.1","12.2","17.3"],
    2: ["3.2", "18.2","7.2","15.2"],
    3: ["6.2","17.1","10.2","14.3"],
    4: ["1.2","13.2","9.2","16.2"],
    5: ["2.3","5.3","8.3","11.3"],
    6: ["2.1", "11.1", "8.1", "5.1"]
}
oppositefaces = {
    1: 3,
    2: 4,
    3: 1,
    4: 2,
    5: 6,
    6: 5
}

class JbrikCube(object):
    def __init__(self, cubestatestr, cubeholder=[], currentsolvelist=[], solvedcells=[], solvemap={}):
        log_utils.log("Initializing JBrikCube")
        self.cubeStateStr = cubestatestr

        self.cubeHolder = cubeholder

        if cubeholder.__len__() == 0:
            log_utils.log("Loading state string: " + cubestatestr)
            self.load_cubestatestr()

        self.currentSolveList = currentsolvelist

        self.solveMap = solvemap

        self.solvedCells = solvedcells

        log_utils.log("Initialization complete.")
        self.print_cube("", True)

    def load_cubestatestr(self):
        if self.cubeStateStr.__len__() != 54:
            #explode
            print("###cube string error - length ###")
            exit(1)

        colorcount = {
            "g": 0,
            "r": 0,
            "y": 0,
            "b": 0,
            "w": 0,
            "o": 0
        }

        chariter = 0
        for r in range(18):
            row = []
            for c in range(3):
                row.append(self.cubeStateStr[chariter])
                colorcount[self.cubeStateStr[chariter]] = colorcount[self.cubeStateStr[chariter]] + 1
                chariter = chariter + 1
            self.cubeHolder.append(row)

        for color in colorcount:
            if colorcount[color] != 9:
                # explode
                print("###cube string error - count [" + color + "]###")
                exit(1)

    def print_cube(self, cubename = "", printmovelist = False):
        # faces 6 - 1 - 5
        linestr = "\n\n" + cubename + "\n    -- 6 --     -- 1 --      -- 5 -- \n"
        linestr += (16).__str__() + ": " + self.get_line_str(self.cubeHolder[15])
        linestr += "  " + (1).__str__() + ": " + self.get_line_str(self.cubeHolder[0])
        linestr += "  " + (13).__str__() + ": " + self.get_line_str(self.cubeHolder[12])

        linestr += "\n" + (17).__str__() + ": " + self.get_line_str(self.cubeHolder[16])
        linestr += "  " + (2).__str__() + ": " + self.get_line_str(self.cubeHolder[1])
        linestr += "  " + (14).__str__() + ": " + self.get_line_str(self.cubeHolder[13])

        linestr += "\n" + (18).__str__() + ": " + self.get_line_str(self.cubeHolder[17])
        linestr += "  " + (3).__str__() + ": " + self.get_line_str(self.cubeHolder[2])
        linestr += "  " + (15).__str__() + ": " + self.get_line_str(self.cubeHolder[14])

        linestr += "\n\n                -- 2 --\n"

        frontspace = "             "

        # face 2
        for row in range(4, 7):
            linestr += frontspace + row.__str__() + ": " + self.get_line_str(self.cubeHolder[row-1]) + "\n"

        linestr += "\n                -- 3 --\n"

        # face 3
        for row in range(7, 10):
            linestr += frontspace + row.__str__() + ": " + self.get_line_str(self.cubeHolder[row-1]) + "\n"

        linestr += "\n                -- 4 --\n"

        frontspace = "            "

        # face 4
        for row in range(10, 13):
            linestr += frontspace + row.__str__() + ": " + self.get_line_str(self.cubeHolder[row-1]) + "\n"

        if printmovelist:
            linestr += "\nSolve list[" + self.currentSolveList.__len__().__str__() + "]: " + self.currentSolveList.__str__() + "\n"

        log_utils.log(linestr + "\n")

    def print_solvemap(self):
        linestr = "\n\nPhase Solutions\n---------------\n"
        for phase in self.solveMap:
            linestr += "Phase " + phase.__str__() + " [" + self.solveMap[phase].__len__().__str__() +  "]: " + self.solveMap[phase].__str__() + "\n"
            #linestr += "Phase: " + phase.__str__() + "\n"

        log_utils.log(linestr + "\n")

    def print_face(self, facenum, cubeholder):
        start = facenum*3-3
        end = facenum*3

        linestr = ""
        for row in range(start, end):
            linestr += (row + 1).__str__() + ": " + self.get_line_str(self.cubeHolder[row]) + "\n"

        log_utils.log(linestr)
        return linestr

    def get_line_str(self, cuberow):
        linestr = "|"
        for cell in cuberow:
            linestr += cell + "|"

        return linestr

    def get_cell_val_by_rowcell(self, rowcell):
        row = rowcell.split(".")[0]
        cell = rowcell.split(".")[1]

        return self.cubeHolder[int(row)-1][int(cell)-1]

    def get_cell_val_by_row_cell(self, row, cell):
        return self.cubeHolder[int(row) - 1][int(cell) - 1]

    def set_cell_val(self, row, cell, val):
        self.cubeHolder[int(row) - 1][int(cell) - 1] = val

    def get_adjcell_color_for_center_rowcell(self, rowcell):
        face = get_face_for_row(int(rowcell.split(".")[0]))
        faceadj = celladjacencies[face]
        adjcellcolor = ""
        for cell in faceadj:
            if cell.split(" ")[0] == rowcell:
                adjcell = cell.split(" ")[1]
                adjcellcolor = self.get_cell_val_by_rowcell(adjcell)
                print("Adjacent cell: " + adjcell + " has color: " + adjcellcolor)
                return adjcellcolor

    def get_current_solve_move_list(self):
        return self.currentSolveList

    def finalize_solve_phase(self, simplifylist=True):
        currentphase = self.solveMap.__len__() + 1
        if simplifylist:
            self.solveMap[currentphase] = reducemovelist(self.currentSolveList)
        else:
            self.solveMap[currentphase] = self.currentSolveList

    def get_center_color_for_rowcell(self, rowcell):
        rownum = rowcell.split(".")[0]
        facenum = get_face_for_row(int(rownum))
        return self.get_cell_val_by_rowcell(((facenum * 3) - 1).__str__() + ".2")

# Static methods
def get_adj_face_for_rowcell(rowcell):
    for adjface in centeradjacencies:
        if centeradjacencies[adjface].__contains__(rowcell):
            return adjface

def get_adjcell_for_rowcell(rowcell):
    faceadj = celladjacencies[1]
    adjcellcolor = ""
    for cell in faceadj:
        if cell.split(" ")[0] == rowcell:
            adjcell = cell.split(" ")[1]
            return adjcell

def get_face_for_row(row):
    if row % 3 == 0:
        #        print("row: " + row.__str__() + " is on face: " + (row/3).__str__())
        return row / 3
    else:
        #        print("row: " + row.__str__() + " is on face: " + (row/3 + 1).__str__())
        return row / 3 + 1

def get_face_for_rowcell(rowcell):
    return get_face_for_row(int(rowcell.split(".")[0]))

def get_transitions_for_face(facenum, dir):
    if dir == "CW":
        return transitions[facenum]
    else:
        retlist = []
        revlist = transitions[facenum][::-1]
        for elm in revlist:
            first = elm.split(" ")[0]
            sec = elm.split(" ")[1]
            retlist.append(sec + " " + first)
        return retlist

def get_transitions_for_frontface( facenum, dir):
    ftranslist = []

    frowend = facenum * 3  # 3
    frowstart = frowend - 3  # 0

    for i in range(1, 4):
        rownum = frowstart + i
        ftransraw = facetransitions[i]
        for trans in ftransraw:
            sourcepos = rownum.__str__() + "." + trans.split(".")[0]
            targetrow = frowstart + int(trans.split(".")[0])
            targetpos = targetrow.__str__() + "." + trans.split(".")[1]

            ftranslist.append(sourcepos + " " + targetpos)

    if dir == "CW":
        return ftranslist
    else:
        retlist = []
        revlist = ftranslist[::-1]
        for elm in revlist:
            first = elm.split(" ")[0]
            sec = elm.split(" ")[1]
            retlist.append(sec + " " + first)

        return retlist

def get_cross_rowcell_for_face(facenum):
    crosscells = ["2", "1", "3", "2"]

    startrow = (facenum * 3) - 2
    crossrowcell = []
    crossrowcell.append(startrow.__str__() + "." + crosscells[0])
    crossrowcell.append((startrow + 1).__str__() + "." + crosscells[1])
    crossrowcell.append((startrow + 1).__str__() + "." + crosscells[2])
    crossrowcell.append((startrow + 2).__str__() + "." + crosscells[3])

    return crossrowcell

def get_next_pos_for_face_rotation(facenum, currentpos):
    translist = transitions[facenum]
    for trans in translist:
        if trans.split(" ")[0] == currentpos:
            return trans.split(" ")[1]




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

    return dedupedlist

def simplifymovelist(movelist):
    simplifiedlist = []
    for move in movelist:
        dir = "W"
        if move[3] == "3":
            if move[2] == "W":
                dir = "C"
            simplifiedlist.append(move[:2] + dir + "1")
        elif int(move[3])%4 == 0:
            continue
        elif int(move[3]) > 4 and int(move[3])%4 != 0:
            simplifiedlist.append(move[:2] + move[2] + (int(move[3])%4).__str__())
        else:
            simplifiedlist.append(move)

    return simplifiedlist

# static
def reducemovelist(movelist):
    explodedlist = explodemovelist(movelist)

    collaplsedlist = collapsemovelist(explodedlist)

    dedupelist = dedupemovelist(collaplsedlist)

    simpllist = simplifymovelist(dedupelist)

    if simpllist.__len__() < movelist.__len__():
        simpllist = reducemovelist(simpllist)

    return simpllist