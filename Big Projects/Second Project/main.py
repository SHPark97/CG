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


gV_list = [ ]
gVN_list = [ ]
gF_list = [ ]
gVertexArray = [ ]
gNormalArray = [ ]
gFNormalArray = [ ]
WireFrame_0_or_Solid_1 = 0
Shading_0_or_Forced_1 = 0
draw_object_on = 0
animation_on = 0
draw_animation_object_on = 0


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
    glLoadIdentity()

    # Wire Frame 과 Solid Mode 구분
    if WireFrame_0_or_Solid_1 == 0 :
        glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
    else :
        glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )
  
    # Light 사용
    glEnable(GL_NORMALIZE)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHT2)
   
    # Light 0 적용
    glPushMatrix()
    lightPos = (0., 10., 0., 1.)
    lightColor = (1., 1., 1., 1.)
    ambientLightColor = (.5, .5, .5, 1.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    glPopMatrix()
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)


    # Light 1 적용
    glPushMatrix()
    lightPos = (10., -10., 0., 1.)
    lightColor = (1., .35, .35, 1.)
    ambientLightColor = (.5, .5, .5, 1.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    glPopMatrix()
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)

    # Light 2 적용
    glPushMatrix()
    lightPos = (-10., -10., 0., 1.)
    lightColor = (.35, 1., .35, 1.)
    ambientLightColor = (.5, .5, .5, 1.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    glPopMatrix()
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)
    

    # Matrial Color 적용
    objectColor = (1., 1., 1., 1.)
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    
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

    ##### Object를 그림          #####
    if draw_object_on == 1 and animation_on == 0 :
        objectColor = (1., 1., 1., 1.)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, objectColor)
        glMaterialfv(GL_FRONT, GL_SHININESS, 10)
        drawObject()

    ##### Animation을 그림 	     #####
    if animation_on == 1 :
        t = glfw.get_time()
        th = np.radians(t)

        # Level1 - Minion Body
        glPushMatrix()
        #glColor3ub(255, 255, 0)
        objectColor = (1., 1., 0., 1.)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, objectColor)
        glMaterialfv(GL_FRONT, GL_SHININESS, 10)

        glScalef(0.2, 0.2, 0.2)
        glRotatef(t* (180/np.pi), 0, 1, 0)
        glTranslatef(0, 3.1, 20)
        glRotatef(90, 0, 1, 0)
        drawMinion()

        # Level2 - Stick
        glPushMatrix()
        glRotatef(20 * np.sin(5 * t), 0, 1, 1)
        glTranslatef(0, 2.8, 7)

        #glColor3ub(210, 105, 30)
        objectColor = (.8235, .4117, .1176, 1.)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, objectColor)
        glMaterialfv(GL_FRONT, GL_SHININESS, 5)
       
        drawStick()

        # Level3 - Banana 1
        glPushMatrix()
        #glColor3ub(255, 255, 0)
        objectColor = (1., 1., 0., 1.)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, objectColor)
        glMaterialfv(GL_FRONT, GL_SHININESS, 10)

        glRotatef(30 * np.sin(7 * t), 0, 1, 1)
        glTranslatef(0, -1, 6.5)
        glScalef(0.1, 0.1, 0.1)
        drawBanana()
        glPopMatrix()

        # Level3 - Banana 2
        glPushMatrix()
        #glColor3ub(255, 255, 0)
        objectColor = (1., 1., 0., 1.)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, objectColor)
        glMaterialfv(GL_FRONT, GL_SHININESS, 10)

        glRotatef(40 * np.sin(5 * t), 0, 1, 1)
        glTranslatef(0, -1, 5.5)
        glScalef(0.1, 0.1, 0.1)
        drawBanana()
        glPopMatrix()

        # Level 2 Pop
        glPopMatrix() 

        # Level 2 - Minion Aura 1
        glPushMatrix()
        #glColor3ub(0, 0, 255)
        objectColor = (0., 0., 1., 1.)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, objectColor)
        glMaterialfv(GL_FRONT, GL_SHININESS, 10)

        glRotatef(3* t* (180/np.pi), 0, 1, 0)
        glTranslatef(0, -2.8, 1)
        glScalef(10, 10, 10)
        drawAura()
        glPopMatrix()

        # Level 2 - Minion Aura 2
        glPushMatrix()
        #glColor3ub(0, 255, 0)
        objectColor = (0., 1., 0., 1.)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, objectColor)
        glMaterialfv(GL_FRONT, GL_SHININESS, 10)

        glRotatef(240, 0, 1, 0)
        glRotatef(3* t* (180/np.pi), 0, 1, 0)
        glTranslatef(0, -2.8, 1)
        glScalef(10, 10, 10)
        drawAura()
        glPopMatrix()

        # Level 2 - Minion Aura 3
        glPushMatrix()
        #glColor3ub(255, 0, 0)
        objectColor = (1., 0., 0., 1.)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, objectColor)
        glMaterialfv(GL_FRONT, GL_SHININESS, 10)

        glRotatef(120, 0, 1, 0)
        glRotatef(3* t* (180/np.pi), 0, 1, 0)
        glTranslatef(0, -2.8, 1)
        glScalef(10, 10, 10)
        drawAura()
        glPopMatrix()
        
        
        # Level 1 Pop
        glPopMatrix()

        # Disable Light
        glDisable(GL_LIGHTING)


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
    #glColor3ub(255, 0, 0)
    objectColor = (1., 0., 0., 1.)
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([1.,0.,0.]))

    #glColor3ub(0, 255, 0)
    objectColor = (0., 1., 0., 1.)
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,1.,0.]))

    #glColor3ub(0, 0, 255)
    objectColor = (0., 0., 1., 1.)
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
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


#######	    3. Object Draw	 	#######
def drawObject():
    global gVertexArray, gNormalArray, gFNormalArray
    global Shading_0_or_Forced_1
    
    varr = gVertexArray
    narr = (gNormalArray) if (Shading_0_or_Forced_1 == 0) else (gFNormalArray)

    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 3 * varr.itemsize, narr)
    glVertexPointer(3, GL_FLOAT, 3 * varr.itemsize, varr)
    glDrawArrays(GL_TRIANGLES, 0, int(varr.size / 3))


#######	  4. Animation Object Draw	 #######
def drawStick():
    stick = open('STICK.obj', "r", encoding='utf-8', errors = 'ignore')
    stick_Varray = [ ]
    stick_VNarray = [ ]
    Parsing(stick, stick_Varray, stick_VNarray)

    stick_Varray = np.array(stick_Varray, "float32")
    stick_VNarray = np.array(stick_VNarray, "float32")
    drawAnimationObject(stick_Varray, stick_VNarray)

def drawMinion():
    minion = open('MINION.obj', "r", encoding='utf-8', errors = 'ignore')
    minion_Varray = [ ]
    minion_VNarray = [ ]

    Parsing(minion, minion_Varray, minion_VNarray)

    minion_Varray = np.array(minion_Varray, "float32")
    minion_VNarray = np.array(minion_VNarray, "float32")
    drawAnimationObject(minion_Varray, minion_VNarray)

def drawBanana():
    banana = open('BANANA.obj', "r", encoding='utf-8', errors = 'ignore')
    banana_Varray = [ ]
    banana_VNarray = [ ]
    Parsing(banana, banana_Varray, banana_VNarray)

    banana_Varray = np.array(banana_Varray, "float32")
    banana_VNarray = np.array(banana_VNarray, "float32")
    drawAnimationObject(banana_Varray, banana_VNarray)

def drawAura():
    temp = np.sqrt(3)
    aura_Varray = np.array( [ [-0.5, 0., -0.25*temp], [0.5, 0., -0.25*temp], [0., 0., 0.25*temp] ] )
    aura_Varray = np.array(aura_Varray, "float32")

    glEnableClientState(GL_VERTEX_ARRAY)
    varr = aura_Varray
    glVertexPointer(3, GL_FLOAT, 3 * varr.itemsize, varr)
    glDrawArrays(GL_TRIANGLES, 0, int(varr.size / 3))


#######	  5. Animation Draw 	#######
def drawAnimationObject(Varray, VNarray):
    global gFNormalArray
    global Shading_0_or_Forced_1
    
    varr = Varray
    narr = (VNarray) if (Shading_0_or_Forced_1 == 0) else (gFNormalArray)

    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 3 * varr.itemsize, narr)
    glVertexPointer(3, GL_FLOAT, 3 * varr.itemsize, varr)
    glDrawArrays(GL_TRIANGLES, 0, int(varr.size / 3))


   

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
    global WireFrame_0_or_Solid_1
    global Shading_0_or_Forced_1
    global animation_on

    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_V:
            if (gPerspective == True) :
                gPerspective = False
            else :
                gPerspective = True

        elif key==glfw.KEY_H :
            # Animating Hierarchical Model Rendering Mode
            # Animation은 Shading Force Shading이 아닌 경우에만 가능
            if animation_on == 1 :
                animation_on = 0
            elif animation_on == 0 and Shading_0_or_Forced_1 == 0 :
                animation_on = 1

        elif key==glfw.KEY_S :
            # Toggle [Shading using normal data in obj file] / [Force Smooth Shading]
            # Force Smoothing은 Animation이 아닌 경우에만 가능
            if Shading_0_or_Forced_1 == 0 and animation_on == 0 :
                Shading_0_or_Forced_1 = 1
            elif Shading_0_or_Forced_1 == 1 :
                Shading_0_or_Forced_1 = 0

        elif key==glfw.KEY_Z :
            # Toggle Wireframe / Solide Mode
            if WireFrame_0_or_Solid_1 == 1 :
                WireFrame_0_or_Solid_1 = 0
            elif WireFrame_0_or_Solid_1 == 0 :
                WireFrame_0_or_Solid_1 = 1


#######	       5. 드랍 콜백 구현 	#######
def drag_drop_callback(window, path):
    global gV_list, gVN_list, gF_list
    global gVertexArray, gNormalArray, gFNormalArray
    global draw_object_on
    gVertexArray = [ ]
    gNormalArray = [ ]
    gFNormalArray = [ ]
    read_lines = [ ]
    line_sep = [ ]
    v_mem_list = [ ]
    vn_mem_list = [ ]
    f_mem_list_temp = [ ]
    f_mem_list = [ ]
    f_vertex_list = [ ]
    Calculated_FNormal_Vector = [ ]
    f_normal_list = [ ]
    num_of_faces_3 = 0
    num_of_faces_4 = 0
    num_of_faces_more = 0
    num_of_faces_total = 0

    fd = open(path[0], "r", encoding='utf-8', errors = 'ignore')

    ######## Text File Parsing #########
    read_lines = fd.readlines()
    for str in read_lines:
        line_sep = str.split()

        if not line_sep :
            continue
        
        if line_sep[0] == 'v' :
            v_mem = np.array( [ float(line_sep[1]), float(line_sep[2]), float(line_sep[3]) ] )
            v_mem_list.append(v_mem)

        elif line_sep[0] == 'vn' :
            vn_mem = np.array( [ float(line_sep[1]), float(line_sep[2]), float(line_sep[3]) ] )
            vn_mem_list.append(vn_mem)

        elif line_sep[0] == 'f' :
            f_mem = [ ]
            for s in line_sep :
                if (s == 'f'):
                    continue
                f_mem.append(s)
            #f_mem_list_temp.append(f_mem)
            num_of_faces_total += 1

            #Triangle
            if len(line_sep) == 3 + 1 :
                num_of_faces_3 += 1
                f_mem_list_temp.append(f_mem)

            #Triangulation Algorithm 적용
            if len(line_sep) == 4 + 1 :
                num_of_faces_4 += 1
                f_mem.clear()
                for i in range(1, 3) :
                    f_mem.append(line_sep[1])
                    f_mem.append(line_sep[i + 1])
                    f_mem.append(line_sep[i + 2])
                f_mem_list_temp.append(f_mem)
                
            if len(line_sep) > 4 + 1 :
                num_of_faces_more += 1
                f_mem.clear()
                for i in range(1, len(line_sep) - 2) :
                    f_mem.append(line_sep[1])
                    f_mem.append(line_sep[i + 1])
                    f_mem.append(line_sep[i + 2])
                f_mem_list_temp.append(f_mem)

    ######## F 형태 Parsing #########
    for mem in f_mem_list_temp :
        temp_f = [ ]
        for str in mem :
            # 1. '/'를 포함한 F Format
            if "/" in str :
                str_sep = str.split('/')

                # (1) a/b 형식의 format => b는 texture로 사용하지 않음
                # a는 Vertex
                if len(str_sep) == 2 :
                    temp_str = np.array([ int(str_sep[0]) ])
                    temp_f.append(temp_str)
                    f_vertex_list.append( int( temp_str[0] ) )
                    gVertexArray.append( tuple( v_mem_list[ temp_str[0] - 1 ] ) )
                
                # (2) a/b/c 형식의 format => b는 texture로 사용하지 않음
                # a는 Vertex, c는 Normal
                elif len(str_sep) == 3 :
                    temp_str = np.array([ int(str_sep[0]), int(str_sep[2]) ])
                    temp_f.append(temp_str)
                    f_vertex_list.append( int( temp_str[0] ) )
                    gNormalArray.append( tuple( vn_mem_list[ temp_str[1] - 1 ] ) )
                    gVertexArray.append( tuple( v_mem_list[ temp_str[0] - 1 ] ) )

            # 2. '/'를 포함하지 않은 F Format
            else :
                str_sep = str.split()
                temp_str = [ ]
                for i in str_sep :
                    temp_str.append( np.array([ int(i) ]) )
                temp_f.append(temp_str)
                for i in temp_str :
                    f_vertex_list.append( int( temp_str[0] ) )
                    gVertexArray.append( tuple( v_mem_list[ temp_str[0] - 1 ] ) )

        f_mem_list.append(temp_f)

    gVertexArray = np.array(gVertexArray, "float32")
    gNormalArray = np.array(gNormalArray, "float32")
    f_vertex_list = np.array(f_vertex_list, "float32")
    f_vertex_list = f_vertex_list.reshape( int( f_vertex_list.size / 3 ), 3)

    for p in f_vertex_list :
        p0 = v_mem_list[int(p[0]) - 1]
        p1 = v_mem_list[int(p[1]) - 1]
        p2 = v_mem_list[int(p[2]) - 1]

        v1 = np.array(p1 - p0)
        v2 = np.array(p2 - p0)
        normal = np.cross(v1, v2) / np.sqrt( np.dot( np.cross(v1, v2), np.cross(v1, v2) ) )
        Calculated_FNormal_Vector.append(normal)

    for vertex_index in range( len( v_mem_list ) ) :
        i = 0
        sum = 0
        vertex_index = vertex_index + 1

        for f_vertex_index in f_vertex_list :
            for p in f_vertex_index :
                if (p == vertex_index) :
                    sum += Calculated_FNormal_Vector[i]
                    break
            i += 1
        f_normal_list.append(sum / np.sqrt( np.dot( sum, sum ) ) )

    for index in f_vertex_list :
        for p in index :
            gFNormalArray.append( f_normal_list[int(p) - 1] )

    gFNormalArray = np.array(gFNormalArray, "float32")

    fd.close()
    draw_object_on = 1

    # Print out Information of the obj file to stdout (console)
    print("File name = ", path[0])
    print("File Total number of faces = ", num_of_faces_total)
    print("File number of faces with 3 vertices = ", num_of_faces_3)
    print("File number of faces with 4 vertices = ", num_of_faces_4)
    print("File number of faces with more than 4 vertices = ", num_of_faces_more)
    print("")


###################################
##########      추가 함수       ##########
###################################
#######	       1. Parsing 구현 	######
def Parsing(fd, Varray, VNarray):
    read_lines = [ ]
    line_sep = [ ]
    v_mem_list = [ ]
    vn_mem_list = [ ]
    f_mem_list_temp = [ ]
    f_mem_list = [ ]

    read_lines = fd.readlines()
    for str in read_lines:
        line_sep = str.split()

        if not line_sep :
            continue
        
        if line_sep[0] == 'v' :
            v_mem = np.array( [ float(line_sep[1]), float(line_sep[2]), float(line_sep[3]) ] )
            v_mem_list.append(v_mem)

        elif line_sep[0] == 'vn' :
            vn_mem = np.array( [ float(line_sep[1]), float(line_sep[2]), float(line_sep[3]) ] )
            vn_mem_list.append(vn_mem)

        elif line_sep[0] == 'f' :
            f_mem = [ ]
            for s in line_sep :
                if (s == 'f'):
                    continue
                f_mem.append(s)
            f_mem_list_temp.append(f_mem)

    ######## F 형태 Parsing #########
    for mem in f_mem_list_temp :
        temp_f = [ ]
        for str in mem :
            # 1. '/'를 포함한 F Format
            if "/" in str :
                str_sep = str.split('/')

                # (1) a/b 형식의 format => b는 texture로 사용하지 않음
                # a는 Vertex
                if len(str_sep) == 2 :
                    temp_str = np.array([ int(str_sep[0]) ])
                    temp_f.append(temp_str)
                    Varrary.append( tuple( v_mem_list[ temp_str[0] - 1 ] ) )
                
                # (2) a/b/c 형식의 format => b는 texture로 사용하지 않음
                # a는 Vertex, c는 Normal
                elif len(str_sep) == 3 :
                    temp_str = np.array([ int(str_sep[0]), int(str_sep[2]) ])
                    temp_f.append(temp_str)
                    VNarray.append( tuple( vn_mem_list[ temp_str[1] - 1 ] ) )
                    Varray.append( tuple( v_mem_list[ temp_str[0] - 1 ] ) )

            # 2. '/'를 포함하지 않은 F Format
            else :
                str_sep = str.split()
                temp_str = [ ]
                for i in str_sep :
                    temp_str.append( np.array([ int(i) ]) )
                temp_f.append(temp_str)
                for i in temp_str :
                    Varray.append( tuple( v_mem_list[ temp_str[0] - 1 ] ) )


    Varray = np.array(Varray, "float32")
    VNarray = np.array(VNarray, "float32")
    fd.close()


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
    glfw.set_drop_callback(window, drag_drop_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()