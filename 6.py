import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np


def render(th):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
   
    # draw cooridnate
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()

    glColor3ub(255, 255, 255)

    # calculate matrix M1, M2 using th
    # your implementation
    R = np.identity(3)
    R[:2,:2] = [ [np.cos(th), np.sin(th)],
		[-np.sin(th), np.cos(th)] ]

    T1 = np.identity(3)
    T1[:2,2] = [0.5, 0]

    T2 = np.identity(3)
    T2[:2,2] = [0, 0.5]

    M1 = R @ T1
    M2 = R @ T2
    

    # draw point p
    glBegin(GL_POINTS)
    # your implementation
    p1 = np.array( [0.5, 0, 1] )
    p2 = np.array( [0, 0.5, 1] )

    p1 = M1 @ p1
    p2 = M2 @ p2

    glVertex2fv(p1[:-1])
    glVertex2fv(p2[:-1])

    glEnd()

    # draw vector v
    glBegin(GL_LINES)

    # your implementation
    zero = np.array( [0, 0] )
    v1 = np.array( [0.5, 0, 0] )
    v2 = np.array( [0, 0.5, 0] )

    v1 = M1 @ v1
    v2 = M2 @ v2

    glVertex2fv(v1[:-1])
    glVertex2fv(zero)
    glVertex2fv(v2[:-1])
    glVertex2fv(zero)

    glEnd()

def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480, 'A', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        t = glfw.get_time()
        th = t
        render(th)
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()