import random
import time
import math



f = ["r", "r", "r", "r"]
b = ["o", "o", "o", "o"]
u = ["w", "w", "w", "w"]
d = ["y1", "y2", "y4", "y3"]
l = ["g", "g", "g", "g"]
r = ["b", "b", "b", "b"]

cube = [f, b, u, d, l, r]

s_length = []

#main

def i_cube(cube):
    i = [str(x) for x in raw_input("How's your cube? ")]
    for item in i:
        if item == " ":
            i.remove(item)
    for item in i:
        for m in range(5):
            if item == str(m):
                for n in range(len(i)):
                    if i[n] == item:
                        i[n - 1] = "y" + str(m)
                i.remove(item)
    print i
    for x in range(4):
        f[x], b[x], u[x], d[x], l[x], r[x] = i[x], i[x + 4], i[x + 8], i[x + 12], i[x + 16], i[x + 20]
    cube = [f, b, u, d, l, r]
    return cube


# I couldn't figure out a more effective way to do this. It was hard to let him remember the cube you gave as input.

def faceturn(x):
    x[0], x[1], x[2], x[3] = x[2], x[0], x[3], x[1]


# After writing the turning defs I figured this could be done easier, by putting Fc(cube) equal to 3 times F(cube)
# I've chosen not to define double turns and just see them as two turns
def F(cube):
    u[2], u[3], d[0], d[1], l[1], l[3], r[0], r[2] = l[3], l[1], r[2], r[0], d[0], d[1], u[2], u[3]
    faceturn(f)
    return cube


def Fc(cube):
    for i in range(3):
        F(cube)
    return cube


def B(cube):
    u[0], u[1], d[2], d[3], l[0], l[2], r[1], r[3] = r[1], r[3], l[0], l[2], u[1], u[0], d[3], d[2]
    faceturn(b)
    return cube


def Bc(cube):
    for i in range(3):
        B(cube)
    return cube


def U(cube):
    f[0], f[1], b[0], b[1], l[0], l[1], r[0], r[1] = r[0], r[1], l[0], l[1], f[0], f[1], b[0], b[1]
    faceturn(u)
    return cube


def Uc(cube):
    for i in range(3):
        U(cube)
    return cube


def D(cube):
    f[2], f[3], b[2], b[3], l[2], l[3], r[2], r[3] = l[2], l[3], r[2], r[3], b[2], b[3], f[2], f[3]
    faceturn(d)
    return cube


def Dc(cube):
    for i in range(3):
        D(cube)
    return cube


def L(cube):
    f[0], f[2], b[1], b[3], u[0], u[2], d[0], d[2] = u[0], u[2], d[2], d[0], b[3], b[1], f[0], f[2]
    faceturn(l)
    return cube


def Lc(cube):
    for i in range(3):
        L(cube)
    return cube


def R(cube):
    f[1], f[3], b[0], b[2], u[1], u[3], d[1], d[3] = d[1], d[3], u[3], u[1], f[1], f[3], b[2], b[0]
    faceturn(r)
    return cube


def Rc(cube):
    for i in range(3):
        R(cube)
    return cube


moves = [F, Fc, B, Bc, U, Uc, D, Dc, L, Lc, R, Rc]
n_moves = ["F", "F'", "B", "B'", "U", "U'", "D", "D'", "L", "L'", "R", "R'"]


def shuffle(cube, x, moved):
    s = []
    while len(s) < x:
        m = random.randint(0, 11)
        s.append(m)
        if len(s) > 1:
            if s[-1] == s[-2]:
                x += 1
            if m % 2 == 0:
                if s[-2] == m + 1:
                    s.remove(s[-2])
            elif m % 2 == 1:
                if s[-2] == m - 1:
                    s.remove(s[-2])
        if len(s) > 2:
            if s[-1] / 4 == s[-2] / 4 == s[-3] / 4:
                s.remove(s[-3])
    for n in s:
        moves[n](cube)
        moved.append(n_moves[n])
        cube = [f, b, u, d, l, r]
    return cube


# Shuffle didn't work completely. It often switched two colours. It appeared that there was a mistake in def R(cube)


def solve_fl(x):
    cube = [f, b, u, d, l, r]
    s2 = []
    s2_2 = []
    for m in range(6):
        for n in range(4):
            if cube[m][n] == x:
                if m == 0:
                    if n == 0:
                        s2.extend([5, 9, 4, 8])
                    elif n == 1:
                        s2.extend([5, 0, 4, 4, 1])
                    elif n == 2:
                        s2.extend([9, 4, 8, 5, 9, 4, 8])
                    elif n == 3:
                        s2.extend([10, 5, 11, 5, 0, 4, 4, 1])
                elif m == 1:
                    if n == 0:
                        s2.extend([9, 4, 4, 8])
                    elif n == 1:
                        s2.extend([0, 5, 1])
                    elif n == 2:
                        s2.extend([11, 4, 10, 9, 4, 4, 8])
                    elif n == 3:
                        s2.extend([8, 5, 9, 0, 5, 1])
                elif m == 2:
                    if n == 0:
                        s2.extend([5, 9, 4, 8, 0, 4, 4, 1])
                    elif n == 1:
                        s2.extend([4, 4, 9, 4, 8, 0, 4, 4, 1])
                    elif n == 2:
                        s2.extend([9, 4, 8, 0, 4, 4, 1])
                    elif n == 3:
                        s2.extend([4, 9, 4, 8, 0, 4, 4, 1])
                elif m == 3:
                    if n == 0:
                        pass
                    elif n == 1:
                        s2.extend([10, 4, 4, 11, 0, 5, 1])
                    elif n == 2:
                        s2.extend([8, 4, 9, 0, 4, 4, 1])
                    elif n == 3:
                        s2.extend([11, 4, 10, 0, 4, 4, 1])
                elif m == 4:
                    if n == 0:
                        s2.extend([4, 4, 9, 4, 8])
                    elif n == 1:
                        s2.extend([4, 0, 5, 1])
                    elif n == 2:
                        s2.extend([8, 8, 1])
                    elif n == 3:
                        s2.extend([0, 5, 1, 1, 8, 0, 9])
                elif m == 5:
                    if n == 0:
                        s2.extend([9, 4, 8])
                    elif n == 1:
                        s2.extend([0, 4, 4, 1])
                    elif n == 2:
                        s2.extend([1, 4, 0, 9, 4, 8])
                    elif n == 3:
                        s2.extend([2, 5, 3, 0, 4, 4, 1])
    s2.extend([7])
    cube = [f, b, u, d, l, r]
    for item in s2:
        moves[item](cube)
        s_length.extend([n_moves[item]])


# It was hard to link a colour to its place on the cube, so that you can go over the cube to find it

def oll(cube):
    cube = [f, b, l, r, u, d]
    s3 = []
    for m in range(4):
        if cube[4].count("w") == 2:
            if cube[2][0] == "w" and cube[2][1] == "w":
                s3.extend([0, 10, 4, 11, 5, 1])
                break
            elif cube[2][0] == "w" and cube[0][1] == "w":
                s3.extend([1, 10, 4, 11, 5, 11, 0, 10])
                break
            elif cube[0][0] == "w" and cube[1][1] == "w":
                s3.extend([10, 4, 11, 5, 11, 0, 10, 1])
                break
            else:
                moves[4](cube)
                s_length.extend(n_moves[4])
        elif cube[4].count("w") == 0:
            if cube[0][0] == "w" and cube[0][1] == "w" and cube[1][0] == "w" and cube[1][1] == "w":
                s3.extend([10, 10, 4, 4, 10, 4, 4, 10, 10])
                break
            elif cube[3][0] != "w" and cube[3][1] != "w":
                s3.extend([0, 10, 4, 11, 5, 10, 4, 11, 5, 1])
                break
            else:
                moves[4](cube)
                s_length.extend(n_moves[4])
        elif cube[4].count("w") == 1:
            if cube[0][1] == "w" and cube[1][1] == "w" and cube[3][1] == "w":
                s3.extend([10, 4, 11, 4, 10, 4, 4, 11])
                break
            elif cube[0][0] == "w" and cube[2][0] == "w" and cube[3][0] == "w":
                s3.extend([10, 4, 4, 11, 5, 10, 5, 11])
                break
            else:
                moves[4](cube)
                s_length.extend(n_moves[4])
    cube = [f, b, u, d, l, r]
    for item in s3:
        moves[item](cube)
        s_length.extend([n_moves[item]])
    return cube


# Sometimes he is able to recognise the case; sometimes he gives the right alg, but 4 times; sometimes he doesn't even
# recognise the case at all.

def pll(cube):
    s4 = []
    cube = [f, b, l, r, u, d]
    if cube[0][0] == cube[0][1] and cube[1][0] == cube[1][1]:
        pass
    elif cube[0][0] == cube[1][1] and cube[0][1] == cube[1][0]:
        s4.extend([0, 10, 5, 11, 5, 10, 4, 11, 1, 10, 4, 11, 5, 11, 0, 10, 1])
    else:
        for k in range(4):
            if cube[0][0] == cube[0][1]:
                s4.extend([10, 3, 10, 0, 0, 11, 2, 10, 1, 1, 10, 10])
                break
            else:
                moves[4](cube)
                s_length.extend(n_moves[4])
    cube = [f, b, u, d, l, r]
    for item in s4:
        moves[item](cube)
        s_length.extend([n_moves[item]])
        # In the pll def he often gave multiple algs. It took a lot of improvement to fix it


def last_turns(cube):
    for n in range(3):
        if cube[0][0] == "r":
            break
        else:
            moves[4](cube)
            s_length.extend([n_moves[4]])


def reducer(cube, moved):
    s_r = []
    for m in range(2):
        s_r.append(s_length[m])
    for n in range(2, len(s_length) + 1):
        if s_r[-1] == s_r[-2]:
            if "'" in s_r[-1]:
                s_r[-2] = s_r[-2].strip("'") + "2"
            else:
                s_r[-2] += "2"
            s_r.pop()
        elif s_r[-1] + "2" == s_r[-2]:
            s_r[-2] = s_r[-2].strip("2")
            if "'" not in s_r[-1]:
                s_r[-2] += "'"
            s_r.pop()
        if n <= len(s_length) - 1:
            s_r.append(s_length[n])
    for item in s_r:
        if item.endswith("2"):
            item = item[0:len(item) - 1]
            moved.append(item)
        moved.append(item)
    return len(s_r)


def solve(cube, moved):
    global s_length
    s_length = []
    solve_fl("y1"), solve_fl("y2"), solve_fl("y3"), solve_fl("y4"), oll(cube), pll(cube), last_turns(cube)
    print reducer(cube, moved)
