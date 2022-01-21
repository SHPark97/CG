import glfw
from OpenGL.GL import *
import numpy as np

M = np.linspace(0,360,13)
M = M * np.pi / 180
cos = np.cos(M)
sin = np.sin(M)
global a
a = 0
global b
b = 1

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(GL_LINE_LOOP)
    
    for x in range(0,13) :
       glVertex2f(cos[x], sin[x])
    glEnd()

    glBegin(GL_LINES)
    glVertex(0.0, 0.0)
   
    glVertex(a, b)
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global a
    global b
    if key==glfw.KEY_1:
        if action==glfw.PRESS:
            a = cos[2]
            b = sin[2]

    elif key==glfw.KEY_2:
        if action==glfw.PRESS:
            a = cos[1]
            b = sin[1]

    elif key==glfw.KEY_3:
        if action==glfw.PRESS:
            a = cos[0]
            b = sin[0]

    elif key==glfw.KEY_4:
        if action==glfw.PRESS:
            a = cos[-2]
            b = sin[-2]

    elif key==glfw.KEY_5:
        if action==glfw.PRESS:
            a = cos[-3]
            b = sin[-3]

    elif key==glfw.KEY_6:
        if action==glfw.PRESS:
            a = cos[-4]
            b = sin[-4]

    elif key==glfw.KEY_7:
        if action==glfw.PRESS:
            a = cos[-5]
            b = sin[-5]

    elif key==glfw.KEY_8:
        if action==glfw.PRESS:
            a = cos[-6]
            b = sin[-6]

    elif key==glfw.KEY_9:
        if action==glfw.PRESS:
            a = cos[-7]
            b = sin[-7]

    elif key==glfw.KEY_0:
        if action==glfw.PRESS:
            a = cos[-8]
            b = sin[-8]

    elif key==glfw.KEY_Q:
        if action==glfw.PRESS:
            a = cos[-9]
            b = sin[-9]

    elif key==glfw.KEY_W:
        if action==glfw.PRESS:
            a = cos[-10]
            b = sin[-10]

def main():
    if not glfw.init():
        return

    window = glfw.create_window(480,480,"2017029634", None,None)

    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)

    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
