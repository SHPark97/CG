import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

Keys = []
keynum = 0

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    # draw cooridnates
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()

    glColor3ub(255, 255, 255)

    global Keys
    global keynum

    if keynum > 0 and Keys[keynum - 1] == 5:
        for i in range(keynum) :
            keynum = 0
            del Keys[0]

    for i in range(keynum) :
        if Keys[keynum - 1 - i] == 1:
            glTranslatef(-0.1, 0, 0)
        elif Keys[keynum - 1 - i] == 2:
            glTranslatef(0.1, 0, 0)
        elif Keys[keynum - 1 - i] == 3:
            glRotatef(10, 0, 0, 1)
        elif Keys[keynum - 1 - i] == 4:
            glRotatef(-10, 0, 0, 1)

    drawTriangle()

def drawTriangle():
    glBegin(GL_TRIANGLES)
    glVertex2fv(np.array([0.,.5]))
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([.5,0.]))
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global Keys
    global keynum

    # rotate the camera when 1 or 3 key is pressed or repeated
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_Q:
            Keys.insert(keynum, 1)
            keynum += 1
        elif key==glfw.KEY_E:
            Keys.insert(keynum, 2)
            keynum += 1
        elif key==glfw.KEY_A:
            Keys.insert(keynum, 3)
            keynum += 1
        elif key==glfw.KEY_D:
            Keys.insert(keynum, 4)
            keynum += 1
        elif key==glfw.KEY_1:
            Keys.insert(keynum, 5)
            keynum += 1

def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480, 'A', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()