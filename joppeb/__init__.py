#!/usr/bin/env python
import math
import pygame
import random
import time

from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

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
    return (math.fabs(2 - x) < dif or math.fabs(0 - x) < dif)\
           and (math.fabs(2 - y) < dif or math.fabs(0 - y) < dif)


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
                 len([p for p in cuby.points if
                      (a and p[xyz] >= 0) or (not a and p[xyz] <= 0)]) == 8]:
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
