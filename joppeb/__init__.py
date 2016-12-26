#!/usr/bin/env python
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
        self.points = [[vertices[v][0] + position[0], vertices[v][1] + position[1], vertices[v][2] + position[2]] for v
                       in range(8)]

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