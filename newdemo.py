#!usr/bin/env python

import pygame
import random
import time
import OpenGL
import math
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from joppeb import *
from joppes import *

def main():
    pygame.init()
    display = (600, 600)
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

main()