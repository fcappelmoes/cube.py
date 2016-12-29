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

import numpy


#matrices used for repositioning cubies (both kinds) in lists
matrix1 = [[0, 0, 0, 1], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]
matrix2 = numpy.dot(matrix1, matrix1)
matrix3 = numpy.dot(matrix2, matrix1)
mlist = [matrix1, matrix2, matrix3]

def repos(k, indices, depth): #repositions cubies on indices in k with amount of turns depth
    m = [k[i] for i in indices]
    newm = numpy.dot(mlist[depth], m)
    for i in range(len(indices)):
        k[indices[i]] = newm[i]
    return k


def crot(cube, axis, indices, depth):  # rotate corners if not in up or down face
    if depth != 1 and axis != 1:
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


def cpos(cube, indices, depth):  # reposition corners
    for i in [cube.cp, cube.cr]:
        repos(i, indices, depth)
    return cube


def epos(cube, indices, depth):  # reposition edges
    for i in [cube.ep, cube.er]:
        repos(i, indices, depth)
    return cube


def parse_moves(string):
    moves = string.lower().split()
    faces = ["f", "b", "u", "d", "l", "r"]
    facedict = {faces[i]: i for i in range(6)}
    numlist = []
    for m in moves:
        num = 0
        if m[0] in faces:
            num = facedict[m]
        if m == "2":
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
        m += faces[num/3]
        if num % 3 == 1:
            m += "2"
        elif num % 3 == 2:
            m += "'"
        movelist.append(m)
    moves = " ".join(movelist)
    return moves


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
            self.er = [True for i in range(12)]

    # table[moves][axis, corners, edges]
    table = [[[0, 1, 5, 4], [8, 5, 11, 4]],
             [[2, 3, 7, 6], [9, 7, 10, 6]],
             [[3, 2, 1, 0], [9, 1, 8, 0]],
             [[4, 5, 6, 7], [11, 2, 10, 3]],
             [[3, 0, 4, 7], [0, 4, 3, 7]],
             [[1, 2, 6, 5], [1, 6, 2, 5]]]

    def move(self, movenums):
        if not type(movenums) == list:
            movenums = [movenums]
        for m in movenums:
            depth = m % 3
            face = m / 3
            axis = face / 2
            crot(self, axis, Cube.table[face][0], depth)
            erot(self, axis, Cube.table[face][1], depth)
            cpos(self, Cube.table[face][0], depth)
            epos(self, Cube.table[face][1], depth)
        return self


