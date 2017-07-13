#!/usr/bin/env python

# cube consists of one or two lists depending on its size:
#   size 2 --> only corners
#   size 3 --> corners and edges
# all cubies are identified by a number
# corner locations are indicated by the location of the cubie in the list
# corner rotations are:
#  - 0 if up or down sticker in up or down face
#  - 1 if up or down sticker left with up or down face up
#  - 2 if up or down sticker right with up or down face up
# edge locations are indicated by the location of the cubie in the list
# edge rotations are:
#  - 1 if sticker adjacent to own or opposite center
#  - 0 if sticker not adjacent to own or opposite center

# when solved, the cube looks like this:
# corners: order, location, rotation:
# "ubl", "ubr", "ufr", "ufl", "dbl", "dbr", "dfr", "dfl"
#   0      1      2      3      4      5      6      7
#   0      0      0      0      0      0      0      0
# edges: order, location, rotation:
# "bl", "br", "fr", "fl", "ul", "ur", "dr", "dl", "ub", "uf", "df", "db"
#  0     1     2     3     4     5     6     7     8     9     10    11
#  1     1     1     1     1     1     1     1     1     1      1     1

# moves are numbered 0 to 17:
#  U  U2  Uc     D  D2  Dc     F  F2  Fc     B  B2  Bc     L  L2  Lc     R  R2  Rc
#  0   1   2     3   4   5     6   7   8     9  10  11    12  13  14    15  16  17

import numpy
import string

# matrices used for relocating cubies (both kinds) in lists
matrix1 = [[0, 0, 0, 1], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]
matrix2 = numpy.dot(matrix1, matrix1)
matrix3 = numpy.dot(matrix2, matrix1)
matlist = [matrix1, matrix2, matrix3]


# works
def reposition(k, indices, depth):  # repositions cubies on indices in k with amount of turns depth
    m = [k[i] for i in indices]
    newm = numpy.dot(matlist[depth], m)
    for i in range(len(indices)):
        k[indices[i]] = newm[i]
    return k


def crot(cube, axis, indices, depth):  # rotate corners if not in up or down face
    if depth != 1 and axis != 0:
        for i in range(0, len(indices), 2):
            cube.cr[indices[i]] = (cube.cr[indices[i]] + 2) % 3
        for i in range(1, len(indices), 2):
            cube.cr[indices[i]] = (cube.cr[indices[i]] + 1) % 3
    return cube


def erot(cube, axis, indices, depth):  # rotate edges
    if depth != 1:
        a = 0 + 4 * axis
        b = 4 + 4 * axis
        m = [cube.ep[i] for i in indices]
        for cubie in range(a, b):
            if cubie in m:
                i = cube.ep.index(cubie)
                cube.er[i] = not cube.er[i]
    return cube


# not necessary
def cpos(cube, indices, depth):  # reposition corners
    for i in [cube.cp, cube.cr]:
        repos(i, indices, depth)
    return cube

# not necessary
def epos(cube, indices, depth):  # reposition edges
    for i in [cube.ep, cube.er]:
        repos(i, indices, depth)
    return cube

#difficult version of reposition when I still worked with bools, now not necessary
# relocates items in list i on indices k with
def relocate(i, indices, depth):
    ind = [i[k] for k in indices]
    temp = numpy.transpose(numpy.dot(matlist[depth], ind))
    if type(i[0]) == bool:
        new = []
        for x in temp:
            new.append(bool(x))
    else:
        new = temp
    for y in range(len(indices)):
        i[indices[y]] = new[y]
    return i


# imput moves with space in between
def parse_moves(movestring):
    moves = movestring.lower().split()
    print moves
    faces = ["f", "b", "u", "d", "l", "r"]
    numlist = []
    for m in moves:
        num = 3 * faces.index(m[0])
        if len(m) > 1:
            if m[1] == "2":
                num += 1
            elif m[1] == "c" or m[1] == "'":
                num += 2
        numlist.append(num)
    return numlist


def present_moves(numlist):
    faces = ["F", "B", "U", "D", "L", "R"]
    movelist = []
    for num in numlist:
        m = ""
        m += faces[num / 3]
        if num % 3 == 1:
            m += "2"
        elif num % 3 == 2:
            m += "'"
        movelist.append(m)
    moves = " ".join(movelist)
    return moves

# not necessary
def testmove(movenums):
    cube = Cube(3)
    if not type(movenums) == list:
        movenums = [movenums]
    for m in movenums:
        depth = m % 3
        face = m / 3
        axis = m / 6
        # rotating cubies that need a rotation (doesn't relocate said rotated cubies)
        crot(cube, axis, Cube.table[face][0], depth)
        erot(cube, axis, Cube.table[face][1], depth)
        # relocating items in ALL lists
        cubelist = [cube.cp, cube.cr, cube.ep, cube.er]
        for i in range(4):
            reposition(cubelist[i], Cube.table[face][i / 2], depth)
    return cube

def printit(cube):  # print cube
    for i in [cube.cp, cube.cr, cube.ep, cube.er]:
        print i


class Cube(object):
    def __init__(self, size):
        self.size = size
        self.cp = [i for i in range(8)]
        self.cr = [0] * 8
        if size == 3:
            self.ep = [i for i in range(12)]
            self.er = [1 for i in range(12)]

    # table[moves][corners, edges]
    table = [[[0, 1, 2, 3], [8, 5, 9, 4]],
             [[7, 6, 5, 4], [10, 6, 11, 7]],
             [[3, 2, 6, 7], [9, 2, 10, 3]],
             [[1, 0, 4, 5], [8, 0, 11, 1]],
             [[0, 3, 7, 4], [4, 3, 7, 0]],
             [[2, 1, 5, 6], [5, 1, 6, 2]]]

    def move(self, movenums):
        if not type(movenums) == list:
            movenums = [movenums]
        for m in movenums:
            depth = m % 3
            face = m / 3
            axis = m / 6
            # rotating cubies that need a rotation (doesn't relocate said rotated cubies)
            crot(self, axis, Cube.table[face][0], depth)
            erot(self, axis, Cube.table[face][1], depth)
            # relocating items in ALL lists
            cubelist = [self.cp, self.cr, self.ep, self.er]
            for i in range(4):
                repos(cubelist[i], Cube.table[face][i/2], depth)
        return self

    def __repr__(self):
        s = "cp " + str(self.cp) + "\n"
        s += "cr " + str(self.cr) + "\n"
        s += "ep " + str(self.ep) + "\n"
        s += "er " + str(self.er)
        return s


# cube input:
# - All the stickers on the cube have a color and those colours are represented by the first
#   letter of that color. "red" becomes r, "blue" is b, "green" is g, "yellow" is y, "white" is w
#   and "orange" is o.
# - Choose a face to solve to: for instance, if white has already partially been solved,
#   take white as top face. Then type the letter of that color, followed by the letter of the
#   front face and the letter of the left face, followed by a whitespace.
# - Start with the top face by typing the letters representing the colors. Type in a circle,
#   starting with the top left corner (which is adjacent to the back and left face) and going
#   clockwise. All letters must be typed without whitespaces in between. End with a whitespace to
#   distinguish this face from other faces to come. The middle sticker isn't needed, so you
#   should now have three characters, a whitespace, eight characters and then another whitespace.
# - The next face is the bottom face. Again start with the top left corner (adjacent to the front
#   and left face) and continue clockwise. Again don't use whitespaces until the end.
# - Now do the front and back faces (in that order) starting with the top left corners adjacent
#   to top and left faces and top and right faces, respectively. Circle clockwise and use
#   whitespaces to distinguish the faces.
# - Finally, input the left and right faces (again in order) starting with the top left corners
#   adjacent to the top and back faces and the top and front faces, respectively. Use a
#   whitespace to distinguish the two faces from each other but since no further input is needed,
#   don't type a whitespace at the end.

trans = "wybgro"
c_table = [[[6, 2, 0], [4, 2, 0], [2, 2, 0], [0, 2, 0],  # stickernumbers
            [0, 6, 4], [2, 6, 4], [4, 6, 4], [6, 6, 4]],
           [[0, 4, 2], [0, 2, 5], [0, 5, 3], [0, 3, 4],  # facenumbers
            [1, 2, 4], [1, 5, 2], [1, 3, 5], [1, 4, 3]]]
e_table = [[[7, 1], [3, 1], [3, 5], [7, 5],
            [7, 3], [3, 7], [7, 3], [3, 7],
            [5, 1], [1, 1], [5, 5], [1, 5]],
           [[0, 4], [0, 5], [1, 5], [1, 4],
            [2, 4], [2, 5], [3, 5], [3, 4],
            [0, 2], [0, 3], [1, 3], [1, 2]]]
corners = ['ufl', 'ufr', 'ubr', 'ubl', 'dfl', 'dfr', 'dbr', 'dbl']
edges = ['ul', 'ur', 'dr', 'dl', 'fl', 'fr', 'br', 'bl', 'uf', 'ub', 'db', 'df']


def counter(num):
    return num + 1 - (num % 2) * 2


def sort(letters, order="udfblr"):
    return "".join(sorted(letters, key=lambda x: order.index(x)))


# input cube as per instructions
def input_cube(arg=None):
    # inputting cube, splitting cube into faces, splitting settings from cube
    if arg is None:
        arg = raw_input("Input your cube as per instructions \n")
    facelist = arg.lower().split()
    ind = facelist.pop(0)
    print facelist

    # translating input to face names
    u = d = f = b = l = r = []
    for i in range(6):
        if ind[0] == trans[i]:
            u = ind[0]
            d = trans[counter(trans.index(u))]
        if ind[1] == trans[i]:
            f = ind[1]
            b = trans[counter(trans.index(f))]
        if ind[2] == trans[i]:
            l = ind[2]
            r = trans[counter(trans.index(l))]
    faces = u + d + f + b + l + r
    tab = string.maketrans(faces, "udfblr")
    newarg = []
    for i in facelist:
        newarg.append(i.translate(tab))
    print newarg

    # creating lists with cubienames
    cornernames = []
    for i in range(8):
        name = ""
        for j in range(3):
            name += newarg[c_table[1][i][j]][c_table[0][i][j]]
        cornernames.append(name)
    edge_list = []
    for i in range(12):
        name = ""
        for j in range(2):
            name += newarg[e_table[1][i][j]][e_table[0][i][j]]
        edge_list.append(name)
    print cornernames
    print edge_list

    # creating lists with cubienumbers
    corner_numbers = []
    for i in cornernames:
        corner_numbers.append(corners.index(sort(i)))
    edge_numbers = []
    for i in edge_list:
        edge_numbers.append(edges.index(sort(i)))

    # corner rotations
    corner_rot = []
    for i in cornernames:
        x = list(i)
        corner_rot.append(x.index("u" or "d"))

    # edge rotations
    edge_rot = []

    return
