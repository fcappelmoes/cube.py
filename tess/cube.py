#!/usr/bin/env python

# cube consists of two lists: corners and edges
# all cubies are identified by a number
# corner positions are indicated by the position of the cubie in the list
# corner rotations are:
#  - 0 if up or down sticker in up or down face
#  - 1 if up or down sticker left with up or down face up
#  - 2 if up or down sticker right with up or down face up
# edge positions are indicated by the position of the cubie in the list
# edge rotations are:
#  - True if sticker adjacent to own or opposite center
#  - False if sticker not adjacent to own or opposite center

# corners: order, position, rotation:
# "ufl", "ufr", "ubr", "ubl", "dfl", "dfr", "dbr", "dbl"
#   0      1      2      3      4      5      6      7
#   0      0      0      0      0      0      0      0
# edges: order, position, rotation:
# "ul", "ur", "dr", "dl", "uf", "ub", "db", "df", "fl", "fr", "br", "bl"
#  0     1     2     3     4     5     6     7     8     9     10    11
# True  True  True  True  True  True  True  True  True  True  True  True

#moves are numbered 0 to 17:
#  F  F2  Fc     B  B2  Bc     U  U2  Uc     D  D2  Dc     L  L2  Lc     R  R2  Rc
#  0   1   2     3   4   5     6   7   8     9  10  11    12  13  14    15  16  17

def circ(k, indices):  # circulate cubies on indices
    temp = k[indices[-1]]
    for i in range(len(indices) - 1)[::-1]:
        k[indices[i + 1]] = k[indices[i]]
    k[indices[0]] = temp
    return k


def crot(cube, indices):  # rotate corners if not in up or down face
    for i in range(0, len(indices), 2):
        cube.cr[indices[i]] = (cube.cr[indices[i]] + 2) % 3
    for i in range(1, len(indices), 2):
        cube.cr[indices[i]] = (cube.cr[indices[i]] + 1) % 3
    return cube


def erot(cube, axis, indices):  # rotate edges
    a = 0 + 4 * axis
    b = 4 + 4 * axis
    m = [cube.ep[i] for i in indices]
    for cubie in range(a, b):
        if cubie in m:
            i = cube.ep.index(cubie)
            cube.er[i] = not cube.er[i]
    return cube


def cpos(cube, indices):  # reposition corners
    for i in [cube.cn, cube.cp, cube.cr]:
        circ(i, indices)
    return cube


def epos(cube, indices):  # reposition edges
    for i in [cube.en, cube.ep, cube.er]:
        circ(i, indices)
    return cube

def move(cube, l):
    # table[moves][axis, corners, edges]
    table = [[[0, 1, 5, 4], [8, 5, 11, 4]],
             [[2, 3, 7, 6], [9, 7, 10, 6]],
             [[3, 2, 1, 0], [9, 1, 8, 0]],
             [[4, 5, 6, 7], [11, 2, 10, 3]],
             [[3, 0, 4, 7], [0, 4, 3, 7]],
             [[1, 2, 6, 5], [1, 6, 2, 5]]]
    if not type(l) == list:
        l = [l]
    for m in l:
        depth = m % 3 + 1
        face = m / 3
        axis = face / 2
        for j in range(depth):
            if axis != 1:
                crot(cube, table[face][0])
            erot(cube, axis, table[face][1])
            cpos(cube, table[face][0])
            epos(cube, table[face][1])
    return cube


def printit(cube):  # print cube
    for i in [cube.cn, cube.cp, cube.cr, cube.en, cube.ep, cube.er]:
        print i


class Cube(object):
    def __init__(self, size):
        self.size = size
        self.cn = ["ufl", "ufr", "ubr", "ubl", "dfl", "dfr", "dbr", "dbl"]
        self.cp = [i for i in range(8)]
        self.cr = [0] * 8
        if size == 3:
            self.en = ["ul", "ur", "dr", "dl", "fl", "fr", "br", "bl", "uf", "ub", "db", "df"]
            self.ep = [i for i in range(12)]
            self.er = [True for i in range(12)]


