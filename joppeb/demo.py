import math
import pygame
import random
import time

from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

f = ["r", "r", "r", "r"]
b = ["o", "o", "o", "o"]
u = ["w", "w", "w", "w"]
d = ["y1", "y2", "y4", "y3"]
l = ["g", "g", "g", "g"]
r = ["b", "b", "b", "b"]

cube = [f, b, u, d, l, r]

s_length = []

dif = 0.00001
axis = 0

vertices = (
    (1.0, -1.0, -1.0),
    (1.0, 1.0, -1.0),
    (-1.0, 1.0, -1.0),
    (-1.0, -1.0, -1.0),
    (1.0, -1.0, 1.0),
    (1.0, 1.0, 1.0),
    (-1.0, 1.0, 1.0),
    (-1.0, -1.0, 1.0)
)


class Surface(object):
    def __init__(self, surface, color, ):
        self.color = color
        self.surface = surface


surfaces = (
    Surface((3, 2, 1, 0), (1, 0.3, 0)),
    Surface((7, 6, 2, 3), (0, 0.6, 0)),
    Surface((4, 5, 6, 7), (0.8, 0, 0)),
    Surface((0, 1, 5, 4), (0, 0, 0.6)),
    Surface((5, 1, 2, 6), (1, 1, 1)),
    Surface((0, 4, 7, 3), (0.8, 0.8, 0))
)


class Cuby(object):
    def __init__(self, position):
        self.points = [[vertices[v][0] + position[0], vertices[v][1] + position[1],
                        vertices[v][2] + position[2]] for v in range(8)]

    def reset(self, c):
        for v in range(8):
            for xyz in range(3):
                self.points[v][xyz] = vertices[c][xyz] + vertices[v][xyz]


vcube = [Cuby(vertices[v]) for v in range(8)]


def reset():
    for v in range(8):
        vcube[v].reset(v)


def printCube():
    for v in range(8):
        print vcube[v].points


def rotatePoint(point, xi, yi, hr):
    x = point[xi]
    y = point[yi]
    # hb = math.atan(x/y)
    # h = hb+hr
    # r = (x**2+y**2)**0.5
    # x = math.cos(h)*r
    # y = math.sin(h)*r

    point[xi] = x * math.cos(hr) - y * math.sin(hr)
    point[yi] = x * math.sin(hr) + y * math.cos(hr)


def mustSnap(point, xi, yi):
    x = math.fabs(point[xi])
    y = math.fabs(point[yi])
    return (math.fabs(2 - x) < dif or math.fabs(0 - x) < dif) and (math.fabs(2 - y) < dif or math.fabs(0 - y) < dif)


def rotateCuby(cuby, xi, yi, hr):
    for point in cuby.points:
        rotatePoint(point, xi, yi, hr)

    if len([p for p in cuby.points if mustSnap(p, xi, yi)]) == 8:
        for point in cuby.points:
            x = math.fabs(point[xi])
            y = math.fabs(point[yi])
            if math.fabs(2 - x) < dif:
                if point[xi] < 0:
                    point[xi] = -2.0
                else:
                    point[xi] = 2.0
            if math.fabs(0 - x) < dif:
                point[xi] = 0.0
            if math.fabs(2 - y) < dif:
                if point[yi] < 0:
                    point[yi] = -2.0
                else:
                    point[yi] = 2.0
            if math.fabs(0 - y) < dif:
                point[yi] = 0.0


def rotateCube(xyz, a, hr, b):
    if xyz == 0:
        xi = 2
        yi = 1
    elif xyz == 1:
        xi = 0
        yi = 2
    elif xyz == 2:
        xi = 1
        yi = 0
    if b == False:
        hr = -hr
    for cuby in [cuby for cuby in vcube if
                 len([p for p in cuby.points if (a and p[xyz] >= 0) or (not a and p[xyz] <= 0)]) == 8]:
        rotateCuby(cuby, xi, yi, hr)


def rotateComplete():
    for cuby in vcube:
        for point in cuby.points:
            for xyz in point:
                abs = math.fabs(xyz)
                if abs != 0 and abs != 2:
                    return False
    return True


def draw(cuby):
    glPushMatrix()

    glBegin(GL_QUADS)
    for surface in surfaces:
        glColor3fv(surface.color)
        for vertex in surface.surface:
            glVertex3fv(cuby.points[vertex])
    glEnd()

    glLineWidth(10)
    glScale(1.01, 1.01, 1.01)
    glColor3f(0.1, 0.1, 0.1)
    for surface in surfaces:
        glBegin(GL_LINE_LOOP)
        for vertex in surface.surface:
            glVertex3fv(cuby.points[vertex])
        glEnd()

    glPopMatrix()


def main():
    pygame.init()
    display = (1000, 1000)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    rotate = False
    clockwise = True
    frontBack = True
    moved = []
    n = 0
    Shift = False
    MousePressed = False
    sol = False
    shuf = False
    xrot = 0.0
    yrot = 0.0
    xpre = 0.0
    ypre = 0.0
    s_length = []
    speed = math.radians(3)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearDepth(1.0)  # Set background depth to farthest
    glEnable(GL_DEPTH_TEST)  # Enable depth testing for z-culling
    glDepthFunc(GL_LEQUAL)  # Set the type of depth-test
    glShadeModel(GL_SMOOTH)  # Smooth shading
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)  # Perspective correction

    while True:
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        gluLookAt(0.0, 0.0, 15.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if MousePressed == False:
                    dx, dy = pygame.mouse.get_pos()
                    xpre = xrot
                    ypre = yrot
                MousePressed = True

            elif event.type == pygame.MOUSEBUTTONUP:
                MousePressed = False

            elif event.type == pygame.KEYUP:
                if event.key == K_LSHIFT:
                    Shift = False

            elif event.type == pygame.KEYDOWN:
                if event.key == K_LSHIFT:
                    Shift = True
                elif event.key == K_x:
                    speed += math.radians(3)
                    print math.degrees(speed)
                elif event.key == K_z:
                    speed += -math.radians(3)
                    print math.degrees(speed)
                elif event.key == K_r:
                    if Shift == False:
                        moved.append("R")
                        moves[n_moves.index("R")](cube)
                    else:
                        moved.append("R'")
                        moves[n_moves.index("R'")](cube)
                elif event.key == K_l:
                    if Shift == False:
                        moved.append("L")
                        moves[n_moves.index("L")](cube)
                    else:
                        moved.append("L'")
                        moves[n_moves.index("L'")](cube)
                elif event.key == K_u:
                    if Shift == False:
                        moved.append("U")
                        moves[n_moves.index("U")](cube)
                    else:
                        moved.append("U'")
                        moves[n_moves.index("U'")](cube)
                elif event.key == K_d:
                    if Shift == False:
                        moved.append("D")
                        moves[n_moves.index("D")](cube)
                    else:
                        moved.append("D'")
                        moves[n_moves.index("D'")](cube)
                elif event.key == K_f:
                    if Shift == False:
                        moved.append("F")
                        moves[n_moves.index("F")](cube)
                    else:
                        moved.append("F'")
                        moves[n_moves.index("F'")](cube)
                elif event.key == K_b:
                    if Shift == False:
                        moved.append("B")
                        moves[n_moves.index("B")](cube)
                    else:
                        moved.append("B'")
                        moves[n_moves.index("B'")](cube)
                elif event.key == K_q:
                    reset()
                    moved = []
                    s_length = []
                    n = 0
                elif event.key == K_p:
                    print moved
                    print cube
                    printCube()
                    print s_length
                elif event.key == K_s:
                    shuf = True
                elif event.key == K_o:
                    sol = True

        mx, my = pygame.mouse.get_pos()

        if not rotate and n != len(moved):
            rotate = True
            if moved[n] == "R":
                axis = 0
                frontBack = True
                clockwise = True
            if moved[n] == "L'":
                axis = 0
                frontBack = False
                clockwise = True
            if moved[n] == "U":
                axis = 1
                frontBack = True
                clockwise = True
            if moved[n] == "D'":
                axis = 1
                frontBack = False
                clockwise = True
            if moved[n] == "F":
                axis = 2
                frontBack = True
                clockwise = True
            if moved[n] == "B'":
                axis = 2
                frontBack = False
                clockwise = True

            if moved[n] == "R'":
                axis = 0
                frontBack = True
                clockwise = False
            if moved[n] == "L":
                axis = 0
                frontBack = False
                clockwise = False
            if moved[n] == "U'":
                axis = 1
                frontBack = True
                clockwise = False
            if moved[n] == "D":
                axis = 1
                frontBack = False
                clockwise = False
            if moved[n] == "F'":
                axis = 2
                frontBack = True
                clockwise = False
            if moved[n] == "B":
                axis = 2
                frontBack = False
                clockwise = False
            n += 1

        if rotate:
            rotateCube(axis, frontBack, speed, clockwise)
            if rotateComplete():
                rotate = False

        if MousePressed == True:
            xrot = xpre + (mx - dx) / 10.0
            yrot = ypre + (my - dy) / 10.0

        if shuf == True:
            shuffle(cube, 10, moved)
            shuf = False

        if sol == True:
            solve(cube, moved)
            sol = False

        if yrot != 0.00:
            glRotatef(yrot, 1.0, 0.0, 0.0)

        if xrot != 0.00:
            glRotatef(xrot, 0.0, 1.0, 0.0)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for cuby in vcube:
            draw(cuby)

        pygame.display.flip()
        pygame.time.wait(20)
        glPopMatrix()


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


main()
