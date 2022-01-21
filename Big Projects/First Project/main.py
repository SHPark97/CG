import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

##### Orbit용 변수 선언	#####
gAzimuth = 60
gElevation = 30
gPast_X = 0
gPast_Y = 0

##### Panning용 변수 선언	#####
gPanning_X = 0
gPanning_Y = 0

##### Zooming용 변수 선언	#####
Backward_or_Forward = 10

##### Callback용 변수 선언	#####
gLeft_Button_Pressed = False
gRight_Button_Pressed = False

##### Toggle용 변수 선언	#####
gPerspective = True


###################################
##########     Render 구현     ##########
###################################
def render():
    global gAzimuth
    global gElevation
    global Backward_or_Forward
    global gPerspective

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
    glLoadIdentity()

    Fovy = 45
    Aspect = 1
    Znear = 1
    Zfar = 100

    ##### Orthogonal / Perspective 취사 선택 #####
    if (gPerspective == True) :
        gluPerspective(Fovy, Aspect, Znear, Zfar)
    elif (gPerspective == False) :
        FH = np.tan(Fovy / 360 * np.pi) * Znear
        FW = FH * Aspect
        Left = -FW
        Right = FW
        Bottom = -FH
        Top = FH
        glOrtho(Left, Right, Bottom, Top, Znear, Zfar)


    # Orbit은 Camera->Target Point의 벡터에 대해 카메라를 돌리면 안되므로
    # myCamera() 함수를 돌리기 전 먼저 EYE(Camera) 좌표에 대해 회전을 진행함
    # 카메라는 반지름의 길이가 1인 구 상에서 움직인다고 가정
    EYE = np.array( [np.cos(np.radians(gAzimuth)) * np.cos(np.radians(gElevation)),
 		np.sin(np.radians(gElevation)),
		np.cos(np.radians(gElevation)) * np.sin(np.radians(gAzimuth)) ] )


    # Target Point는 (0, 0, 0)으로 설정
    AT = np.array( [0., 0., 0.] )
    UP = np.array( [0., 1., 0.] )


    # gElevation의 각도에 따라 UP 벡터의 방향을 반대로 해주어야 함
    if (gElevation < 90 or 270 <= gElevation) :
        myCamera(EYE, AT, UP)

    elif (90 <= gElevation and gElevation < 270) :
        myCamera(EYE, AT, -1 * UP)


    ##### Grid와 Frame을 그림 #####
    drawGrid()
    drawFrame()


###################################
##########     Camera 구현     ##########
###################################
def myCamera(eye, at, up) :
    global gPanning_X
    global gPanning_Y
    global Backward_or_Forward
   
    w = (eye-at) / np.sqrt( np.dot(eye-at, eye-at) )
    u = np.cross(up, w) / np.sqrt( np.dot(np.cross(up, w), np.cross(up, w)) )
    v = np.cross(w, u)

    Mv = np.array([ [u[0], u[1], u[2], -u@eye ],
		[v[0], v[1], v[2], -v@eye ],
		[w[0], w[1], w[2], -w@eye ],
		[0,     0,     0,     1]      ] )

    # np.linalg.inv() 함수는 역행렬을 구하는 함수
    # Mv_inv는 View Space -> World Space 변환 행렬
    Mv_inv = np.linalg.inv(Mv)

    # 마우스 우클릭으로 구한 Panning 값을 통한 Panning Matrix 생성 (u, v축 Translate)
    PanningView = np.identity(4)
    PanningView[:2, -1] = [ -0.01 * gPanning_X, 0.01 * gPanning_Y ]

    # 마우스 휠로 구한 Backward_or_Forward 값을 통한 Zooming Matrix 생성 (w축 Translate)
    ZoomingView = np.identity(4)
    ZoomingView[2, -1] = Backward_or_Forward

    # TotalTranslateView는 Panning Translate 행렬과 Zooming  Translate 행렬을 Combine한 최종 Translate 행렬
    TotalTranslateView = PanningView @ ZoomingView

    # gTotal_Matrix는 "TotalTranslateView로 바꾼 후 View Space -> World Space로 변환"한 행렬
    gTotal_Matrix = Mv_inv@TotalTranslateView

    # gTotal_Matrix_inv는 총 합 행렬의 역행렬을 구해 "World Space -> View Space"로의 변환을 하게 하는 행렬
    gTotal_Matrix_inv = np.linalg.inv(gTotal_Matrix)

    # glMultMatrixf() 함수는 Column-major 이므로 구한 최종 행렬의 Transpose를 사용
    glMultMatrixf(gTotal_Matrix_inv.T)
    

###################################
##########  Draw Frame 구현  ##########
###################################

#######	 1. 기존 XYZ Frame  	#######
def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([1.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,1.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,1.]))
    glEnd()


#######	 2. XZ 평면 상의 Grid 구현  	#######
def drawGrid():
    for i in range(21) :
        glPushMatrix()
        glColor3ub(255, 255, 255)
        glTranslatef(0.5*i, 0., -0.5*i)
        glBegin(GL_LINES)
        glColor3ub(255, 255, 255)
        glVertex3fv([0., 0., 10.])
        glVertex3fv([-10., 0., 0.])
        glEnd()
        glPopMatrix()

    for i in range(21) :
        glPushMatrix()
        glColor3ub(255, 255, 255)
        glTranslatef(-0.5*i, 0., -0.5*i)
        glBegin(GL_LINES)
        glVertex3fv([0., 0., 10.])
        glVertex3fv([10., 0., 0.])
        glEnd()
        glPopMatrix()

###################################
########## Callback 함수 구현 ##########
###################################

#######	 1. 마우스 클릭 콜백 구현 	#######
def mouse_click_callback(window, button, action, mod):
    # 마우스 버튼 움직임에 대한 Callback 함수
    global gLeft_Button_Pressed
    global gRight_Button_Pressed
   
    if button == glfw.MOUSE_BUTTON_LEFT:
        if action == glfw.PRESS:
            gLeft_Button_Pressed = True
        elif action == glfw.RELEASE:
            gLeft_Button_Pressed = False

    elif button == glfw.MOUSE_BUTTON_RIGHT:
        if action == glfw.PRESS:
            gRight_Button_Pressed = True            
        elif action == glfw.RELEASE:
            gRight_Button_Pressed = False


#######	 2. 마우스 휠 콜백 구현	#######
def mouse_scroll_callback(window, xoffset, yoffset):
    # 마우스 스크롤 움직임에 대한 Callback 함수
    # 마우스의 휠 움직임은 Camera를 w vector 방향으로 Translate
    global Backward_or_Forward
    
    Backward_or_Forward = Backward_or_Forward - yoffset
    
    if (Backward_or_Forward < 0) :
        Backward_or_Forward = 0


#######	 3. 마우스 커서 콜백 구현	#######
def mouse_cursor_callback(window, xpos, ypos):
    # 마우스 움직임에 대한 Callback 함수
    # mouse_click_callback과 함께 Orbit, Panning 구현

    global gLeft_Button_Pressed
    global gRight_Button_Pressed
    global gAzimuth
    global gElevation
    global gPast_X
    global gPast_Y
    global gPanning_X
    global gPanning_Y

    if (gLeft_Button_Pressed == True) :
        # Orbit 구현
        gAzimuth = (gAzimuth + xpos - gPast_X) % 360
        gElevation = (gElevation + ypos - gPast_Y) % 360

        # Euler Angle 적용시 세 축 중 두 축이 겹치는 현상을 방지
        # 중간 고리가 회전할 때는 안쪽 고리를 물고 회전하므로 생기는 부작용
        # 짐벌락은 해결할 수 없고 피해가야 함
        if (gElevation % 90 == 0) :
            gElevation = gElevation + 0.1

    if (gRight_Button_Pressed == True) :
        # Panning 구현
        # 마우스의 좌우 움직임은 Camera와 Target을 모두 u vector 방향으로 Translate
        # 마우스의 상하 움직임은 Camera와 Target을 모두 v vector 방향으로 Translate
        gPanning_X = gPanning_X + xpos - gPast_X
        gPanning_Y = gPanning_Y + ypos - gPast_Y

    gPast_X = xpos
    gPast_Y = ypos


#######	 4. 키 콜백 구현 		#######
def key_callback(window, key, scancode, action, mods):
    # 'v' 키가 눌리면 Toggle "Perspective Projection & Orthogonal Perspective Projection"
    global gPerspective

    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_V:
            if (gPerspective == True) :
                gPerspective = False
            else :
                gPerspective = True


###################################
##########      main 함수       ##########
###################################
def main():
    if not glfw.init():
        return
    window = glfw.create_window(1000,1000,'A', None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    # 콜백함수 등록
    glfw.set_key_callback(window, key_callback)
    glfw.set_cursor_pos_callback(window, mouse_cursor_callback)
    glfw.set_mouse_button_callback(window, mouse_click_callback)
    glfw.set_scroll_callback(window, mouse_scroll_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()