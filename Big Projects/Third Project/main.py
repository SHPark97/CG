##### [Class Assignment 3 - 2017029634 박성환] #####
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

########### Class Assignment 1 용 변수 ############
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

###########################
gH = 0
gS = 0
gRA = 0
gRFA = 0
gRH = 0
gLA = 0
gLFA = 0
gLH = 0
gRUL = 0
gRL = 0
gRF = 0
gLUL = 0
gLL = 0
gLF = 0

class Anima :
    def __init__(self) :
        self.did = 0
        self.Varray = [ ]
        self.VNarray = [ ]

Head = Anima()
Spine = Anima()
RightArm = Anima()
RightForeArm = Anima()
RightHand = Anima()
LeftArm = Anima()
LeftForeArm = Anima()
LeftHand = Anima()
RightUpLeg = Anima()
RightLeg = Anima()
RightFoot = Anima()
LeftUpLeg = Anima()
LeftLeg = Anima()
LeftFoot = Anima()

########### Class Assignment 3 용 변수 ############
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
gFrames = 0
gFrameTime = 0.
gTime = 0.
gFPS = 0
gJointArchitecture = [ ]
gPos = [ ]
gRM = [ ]
gZ = 0
gParsing = 0

gWFrames = 0
gWFrameTime = 0.
gWFPS = 0
gWTime = 0.
gWJointArchitecture = [ ]
gWPos = [ ]
gWRM = [ ]

class Joint_Arch :
    def __init__(self, name, parent) :
        # 자기 자신에 대한 정보
        self.name = name
        self.offset_list = [ ]
        self.channel_list = [ ]
        self.num_of_channels = 0
        self.channel_order_list = [ ]
        self.position_list = [ ]
        self.RM_list = [ ]

        # 부모에 대한 정보
        self.parent = parent

    def set_num_of_channels(self, num_of_channels) :
        self.num_of_channels = num_of_channels

    def get_name(self) :
        return self.name

    def get_offset_list(self) :
        return self.offset_list

    def get_channel_list(self) :
        return self.channel_list

    def get_num_of_channels(self) :
        return self.num_of_channels

    def get_channel_order_list(self) :
        return self.channel_order_list

    def get_parent(self) :
        return self.parent

    def get_position(self) :
        return self.position_list

    def get_RM(self) :
        return self.RM_list

    def append_offset(self, offset) :
        self.offset_list.append(offset)

    def append_channel(self, channel) :
        self.channel_list.append(channel)

    def append_channel_order(self, channel_order) :
        self.channel_order_list.append(channel_order)

    def append_position(self, positions) :
        self.position_list.append(positions)

    def append_RM(self, RMs) :
        self.RM_list.append(RMs)


###################################
##########     Render 구현     ##########
###################################
def render():
    global gAzimuth
    global gElevation
    global Backward_or_Forward
    global gPerspective
    global gTime, gFrames, gFPS, gPos, gZ, gParsing
    global gWTime, gWFrames, gWFPS, gWPos

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glLoadIdentity()
    
    if (gZ == 1) :
        glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )
    else :
        glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )

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



    
    # Class Assignment 1
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

    objectColor = (1., 1., 1., 1.)
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)


    ##### Class Assignment 1   #####
    ##### Grid와 Frame을 그림 #####
    drawGrid()
    drawFrame()

    ##### Class Assignment 3   #####

    # Object Animation..
    if (gZ == 1) :
        if (gParsing == 0) :
            WalkParse()
            gParsing = 1

        if ( animation_on == 0 ) :
            glPushMatrix()
            glScalef(0.1, 0.1, 0.1)

            cur_joint = Joint_Arch("No", 0)
            for temp in gWJointArchitecture :
                if (temp.get_name() == "{") :
                    glPushMatrix()

                    temp_parent = cur_joint.get_parent()

                    # Root가 아닌 경우에만 진행
                    if (temp_parent != None) :
                        M = np.identity(4)
                        M[3, 0:3] = [cur_joint.get_offset_list()[0], cur_joint.get_offset_list()[1], cur_joint.get_offset_list()[2] ]
                        glMultMatrixf(M)

                        glPushMatrix()
                        objectColor = (1., 1., 0., 1.)
                        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, objectColor)
                        glMaterialfv(GL_FRONT, GL_SHININESS, 10)
                
                        Name = cur_joint.get_name()
                        if (Name == "Head") :
                            drawH()
                        elif (Name == "Spine") :
                            drawS()
                        elif (Name == "RightArm") :
                            drawRA()
                        elif (Name == "RightForeArm") :
                            drawRFA()
                        elif (Name == "RightHand") :
                            drawRH()
                        elif (Name == "LeftArm") :
                            drawLA()
                        elif (Name == "LeftForeArm") :
                            drawLFA()
                        elif (Name == "LeftHand") :
                            drawLH()
                        elif (Name == "RightUpLeg") :
                            drawRUL()
                        elif (Name == "RightLeg") :
                            drawRL()
                        elif (Name == "RightFoot") :
                            drawRF()
                        elif (Name == "LeftUpLeg") :
                            drawLUL()
                        elif (Name == "LeftLeg") :
                            drawLL()
                        elif (Name == "LeftFoot") :
                            drawLF()
                        glPopMatrix()

                elif (temp.get_name() == "}") :
                    glPopMatrix()

                else :
                    cur_joint = temp

            glPopMatrix()



        else :

            # time 설정 (FPS 및 Frame 설정)
            t = glfw.get_time() - gTime
            t = int (t * gWFPS)
            t = t % gWFrames

            glPushMatrix()

            if gWPos :
                M = np.identity( 4 )
                M[3, 0:3] = [ gWPos[t][0], gWPos[t][1], gWPos[t][2] ]
                glMultMatrixf( M )
                glMultMatrixf( gWRM[t] )

            cur_joint = Joint_Arch("No", 0)
            for temp in gWJointArchitecture :
                if (temp.get_name() == "{") :
                    glPushMatrix()

                    temp_parent = cur_joint.get_parent()

                    # Root가 아닌 경우에만 진행
                    if (temp_parent != None) :
                        RM = cur_joint.get_RM()[t] if cur_joint.get_RM() else np.identity(4)
                        glMultMatrixf(RM)

                        glPushMatrix()
                        glScalef(0.1, 0.1, 0.1)

                        objectColor = (1., 1., 0., 1.)
                        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, objectColor)
                        glMaterialfv(GL_FRONT, GL_SHININESS, 10)

                        Name = cur_joint.get_name()
                        if (Name == "Spine") :
                            drawS()
                            drawH()
                            drawRA()
                            drawRFA()
                            drawRH()
                            drawLA()
                            drawLFA()
                            drawLH()
                        elif (Name == "RightUpLeg") :
                            drawRUL()
                        elif (Name == "RightLeg") :
                            drawRL()
                            drawRF()
                        elif (Name == "LeftUpLeg") :
                            drawLUL()
                        elif (Name == "LeftLeg") :
                            drawLL()
                            drawLF()
                        glPopMatrix()


                elif (temp.get_name() == "}") :
                    glPopMatrix()

                else :
                    cur_joint = temp

            glPopMatrix()

    # 움직이지 않는 bvh
    elif (animation_on == 0) :
        glPushMatrix()
        #glScalef(0.025, 0.025, 0.025)

        cur_joint = Joint_Arch("No", 0)
        for temp in gJointArchitecture :
            if (temp.get_name() == "{") :
                glPushMatrix()

                temp_parent = cur_joint.get_parent()

                # Root가 아닌 경우에만 진행
                if (temp_parent != None) :
                    M = np.identity(4)
                    M[3, 0:3] = [cur_joint.get_offset_list()[0], cur_joint.get_offset_list()[1], cur_joint.get_offset_list()[2] ]
                    glMultMatrixf(M)

                    glPushMatrix()
                    objectColor = (0., 0., 1., 1.)
                    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, objectColor)
                    glMaterialfv(GL_FRONT, GL_SHININESS, 10)

                    point = ( np.linalg.inv(M).T @ np.array( [0., 0., 0., 1.] ) )[:-1]
                
                    glBegin(GL_LINES)
                    glColor3ub(0, 0, 255)
                    glVertex3f(0, 0, 0)
                    glVertex3fv(point)
                    glEnd()
                    glPopMatrix()

            elif (temp.get_name() == "}") :
                glPopMatrix()

            else :
                cur_joint = temp

        glPopMatrix()

    # 움직이는 bvh
    else :
        # time 설정 (FPS 및 Frame 설정)
        t = glfw.get_time() - gTime
        t = int (t * gFPS)
        t = t % gFrames

        glPushMatrix()
        #glScalef(0.025, 0.025, 0.025)

        if gPos :
            M = np.identity( 4 )
            M[3, 0:3] = [ gPos[t][0], gPos[t][1], gPos[t][2] ]
            glMultMatrixf( M )
            glMultMatrixf( gRM[t] )

        cur_joint = Joint_Arch("No", 0)
        for temp in gJointArchitecture :
            if (temp.get_name() == "{") :
                glPushMatrix()

                temp_parent = cur_joint.get_parent()

                # Root가 아닌 경우에만 진행
                if (temp_parent != None) :
                    M = np.identity(4)
                    M[3, 0:3] = [cur_joint.get_offset_list()[0], cur_joint.get_offset_list()[1], cur_joint.get_offset_list()[2] ]
                    glMultMatrixf(M)

                    RM = cur_joint.get_RM()[t] if cur_joint.get_RM() else np.identity(4)
                    glMultMatrixf(RM)

                    point = ( np.linalg.inv(RM).T @ np.linalg.inv(M).T @ np.array( [0., 0., 0., 1.] ) )[:-1]

                    glPushMatrix()
                    objectColor = (0., 0., 1., 1.)
                    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, objectColor)
                    glMaterialfv(GL_FRONT, GL_SHININESS, 10)

                
                    glBegin(GL_LINES)
                    glColor3ub(0, 0, 255)
                    glVertex3f(0, 0, 0)
                    glVertex3fv(point)
                    glEnd()
                    glPopMatrix()

            elif (temp.get_name() == "}") :
                glPopMatrix()

            else :
                cur_joint = temp

        glPopMatrix()


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
def drawH() :
    global gH, Head
    gH = draws(gH, Head, 'head.obj')

def drawS() :
    global gS, Spine
    gS = draws(gS, Spine, 'spine.obj')

def drawRA() :
    global gRA, RightArm
    gRA = draws(gRA, RightArm, 'right_arm.obj')

def drawRFA() :
    global gRFA, RightForeArm
    gRFA = draws(gRFA, RightForeArm, 'right_fore_arm.obj')

def drawRH() :
    global gRH, RightHand
    gRH = draws(gRH, RightHand, 'right_hand.obj')

def drawLA() :
    global gLA, LeftArm
    gLA = draws(gLA, LeftArm, 'left_arm.obj')

def drawLFA() :
    global gLFA, LeftForeArm
    gLFA = draws(gLFA, LeftForeArm, 'left_fore_arm.obj')

def drawLH() :
    global gLH, LeftHand
    gLH = draws(gLH, LeftHand, 'left_hand.obj')

def drawRUL() :
    global gRUL, RightUpLeg
    gRUL = draws(gRUL, RightUpLeg, 'right_up_leg.obj')

def drawRL() :
    global gRL, RightLeg
    gRL = draws(gRL, RightLeg, 'right_leg.obj')

def drawRF() :
    global gRF, RightFoot
    gRF = draws(gRF, RightFoot, 'right_foot.obj')

def drawLUL() :
    global gLUL, LeftUpLeg
    gLUL = draws(gLUL, LeftUpLeg, 'left_up_leg.obj')

def drawLL() :
    global gLL, LeftLeg
    gLL = draws(gLL, LeftLeg, 'left_leg.obj')

def drawLF() :
    global gLF, LeftFoot
    gLF = draws(gLF, LeftFoot, 'left_foot.obj')

def draws(g, part, path):
    if (g == 0) :
        fd = open(path, "r", encoding='utf-8', errors = 'ignore')
        Parsing(fd, part.Varray, part.VNarray)

    if (part == None) :
        print(g)
    part.Varray = np.array(part.Varray, "float32")
    part.VNarray = np.array(part.VNarray, "float32")
    drawAnimationObject(part.Varray, part.VNarray)
    return 1

#######	    Animation Draw 	#######
def drawAnimationObject(Varray, VNarray):
    varr = Varray
    narr = VNarray

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
    global animation_on
    global gTime, gZ

    if action==glfw.PRESS or action==glfw.REPEAT:
        ###### Class Assignment 3 #####
        if key==glfw.KEY_SPACE :
            # Animate the loaded motion
            if animation_on == 1 :
                animation_on = 0
            else :
                animation_on = 1
                gTime = glfw.get_time()
        elif key==glfw.KEY_Z :
            if gZ == 1 :
                gZ = 0
            else :
                gZ = 1
                gTime = glfw.get_time()


#######     Class Assignment 3 	#######
#######	       5. 드랍 콜백 구현 	#######
def drag_drop_callback(window, path):
    global gFrames, gFrameTime
    global gJointArchitecture
    global gPos, gFPS, gRM
    read_lines = [ ]
    line_sep = [ ]
    num_of_joints = 0
    name_of_joints = [ ]
    cur_joint = None
    cur_parent = None
    end_0_or_continue_1 = 1
    gJointArchitecture = [ ]
    gRM = [ ]
    gPos = [ ]

    fd = open(path[0], "r", encoding='utf-8', errors = 'ignore')

    ######## Text File Parsing #########
    hierarchy_1_or_motion_2 = 1
    read_lines = fd.readlines()
    for str in read_lines:
        line_sep = str.split()

        # Motion 부분 처리
        if (hierarchy_1_or_motion_2 == 2) :
            num_list = list(map(float, line_sep))
            index = 3
            gPos.append(num_list[0:3])
            for temp_joint in gJointArchitecture :
                num_of_channels = temp_joint.get_num_of_channels()
                if (num_of_channels != 0) :
                    temp_joint.append_channel(num_list[index : index + num_of_channels])
                    temp_joint.append_position(num_list[0:3])
                    index += num_of_channels

        elif (line_sep[0] == "Frames:") :
            gFrames = int(line_sep[1])

        elif (line_sep[0] == "Frame" and line_sep[1] == "Time:") :
            hierarchy_1_or_motion_2 = 2
            gFrameTime = float(line_sep[2])
        
        # Hierarchy 부분 처리
        elif (line_sep[0] == "ROOT") :
            # 출력용 변수 처리
            name_of_joint = line_sep[1]
            name_of_joints.append(name_of_joint)
            num_of_joints += 1    

            # Joint Architecture에 넣어서 진행
            cur_joint = Joint_Arch(name_of_joint, None)
            gJointArchitecture.append(cur_joint)

        elif (line_sep[0] == "OFFSET") :
            line_sep = line_sep[1:]
            offset_list = list(map(float, line_sep))
            for offsets in offset_list :
                cur_joint.append_offset(offsets)

        elif (line_sep[0] == "CHANNELS") :
            line_sep = line_sep[2:]
            num = 0
            for str in line_sep :
                if ("rotation" in str.lower()) :
                    cur_joint.append_channel_order(str)
                    num += 1
            cur_joint.set_num_of_channels(num)

        elif (line_sep[0] == "JOINT") :
            # 출력용 변수 처리
            name_of_joint = line_sep[1]
            name_of_joints.append(name_of_joint)
            num_of_joints += 1    

            # Joint Architecture에 넣어서 진행
            cur_joint = Joint_Arch(name_of_joint, parent)
            gJointArchitecture.append(cur_joint)

        elif (line_sep[0] == "End" and line_sep[1] == "Site") :
            # Joint Architecture에 넣어서 진행
            cur_joint = Joint_Arch("End Site", parent)
            gJointArchitecture.append(cur_joint)

            # End Site 표현
            end_0_or_continue_1 = 0

        elif (line_sep[0] == "{") :
            # 괄호가 열린 경우 기존의 joint가 새로운 부모가 되든지 유지함
            if (end_0_or_continue_1 == 1) :
                parent = cur_joint
            gJointArchitecture.append(Joint_Arch("{", None))

        elif (line_sep[0] == "}") :
            # 괄호가 닫힌 경우 기존의 joint로 돌아오든지 위의 단계로 감
            if (end_0_or_continue_1 == 0) :
                # 유지
                end_0_or_continue_1 = 1
            else :
                # 위의 단계로 감
                cur_joint = cur_joint.get_parent()
                parent = cur_joint.get_parent()
            gJointArchitecture.append(Joint_Arch("}", None))

    for temp in gJointArchitecture : 
        if (temp.get_num_of_channels() != 0) :
            for channel in temp.get_channel_list() :
                num = len(channel)
                M = np.identity(4)
                
                for index in range(num) :
                    channel_order = temp.get_channel_order_list()
                    th = np.radians( -channel[index] )
                    cos = np.cos(th)
                    sin = np.sin(th)

                    if (channel_order[index].lower() == "xrotation") :
                        Rotation = np.array( [ [1., 0., 0., 0., ],
					[0., cos, -sin, 0.],
					[0., sin, cos, 0.],
					[0., 0., 0., 1.] ] )
                        M = Rotation @ M

                    elif (channel_order[index].lower() == "yrotation") :
                        Rotation = np.array( [ [cos, 0., sin, 0., ],
					[0., 1., 0., 0.],
					[-sin, 0., cos, 0.],
					[0., 0., 0., 1.] ] )
                        M = Rotation @ M

                    elif (channel_order[index].lower() == "zrotation") :
                        Rotation = np.array( [ [cos, -sin, 0., 0., ],
					[sin, cos, 0., 0.],
					[0., 0., 1., 0.],
					[0., 0., 0., 1.] ] )
                        M = Rotation @ M            
                   
                temp.append_RM(M)

    gRM = gJointArchitecture[0].get_RM()


    fd.close()

    print("")
    # Print out Information of the obj file to stdout (console)
    print("1. File name = ", path[0])
    print("2. Number of Frames = ", gFrames)
    gFPS = int(1 / gFrameTime)
    print("3. FPS (which is 1/FrameTime) = ", gFPS)
    print("4. Number of joints (including root) = ", num_of_joints)
    print("5. List of all joint names")
    index = 1
    for names in name_of_joints :
        print(" [", index, "] = ", names)
        index += 1
    print("")


######
# 추가함수
######
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



##################################
def WalkParse():
    global gWFrames, gWFrameTime
    global gWJointArchitecture
    global gWPos, gWFPS, gWRM
    read_lines = [ ]
    line_sep = [ ]
    num_of_joints = 0
    name_of_joints = [ ]
    cur_joint = None
    cur_parent = None
    end_0_or_continue_1 = 1
    gWJointArchitecture = [ ]
    gWRM = [ ]
    gWPos = [ ]

    fd = open('sample-walk.bvh', "r", encoding='utf-8', errors = 'ignore')

    ######## Text File Parsing #########
    hierarchy_1_or_motion_2 = 1
    read_lines = fd.readlines()
    for str in read_lines:
        line_sep = str.split()

        # Motion 부분 처리
        if (hierarchy_1_or_motion_2 == 2) :
            num_list = list(map(float, line_sep))
            index = 3
            gWPos.append(num_list[0:3])
            for temp_joint in gWJointArchitecture :
                num_of_channels = temp_joint.get_num_of_channels()
                if (num_of_channels != 0) :
                    temp_joint.append_channel(num_list[index : index + num_of_channels])
                    temp_joint.append_position(num_list[0:3])
                    index += num_of_channels

        elif (line_sep[0] == "Frames:") :
            gWFrames = int(line_sep[1])

        elif (line_sep[0] == "Frame" and line_sep[1] == "Time:") :
            hierarchy_1_or_motion_2 = 2
            gWFrameTime = float(line_sep[2])
        
        # Hierarchy 부분 처리
        elif (line_sep[0] == "ROOT") :
            # 출력용 변수 처리
            name_of_joint = line_sep[1]
            name_of_joints.append(name_of_joint)
            num_of_joints += 1    

            # Joint Architecture에 넣어서 진행
            cur_joint = Joint_Arch(name_of_joint, None)
            gWJointArchitecture.append(cur_joint)

        elif (line_sep[0] == "OFFSET") :
            line_sep = line_sep[1:]
            offset_list = list(map(float, line_sep))
            for offsets in offset_list :
                cur_joint.append_offset(offsets)

        elif (line_sep[0] == "CHANNELS") :
            line_sep = line_sep[2:]
            num = 0
            for str in line_sep :
                if ("rotation" in str.lower()) :
                    cur_joint.append_channel_order(str)
                    num += 1
            cur_joint.set_num_of_channels(num)

        elif (line_sep[0] == "JOINT") :
            # 출력용 변수 처리
            name_of_joint = line_sep[1]
            name_of_joints.append(name_of_joint)
            num_of_joints += 1    

            # Joint Architecture에 넣어서 진행
            cur_joint = Joint_Arch(name_of_joint, parent)
            gWJointArchitecture.append(cur_joint)

        elif (line_sep[0] == "End" and line_sep[1] == "Site") :
            # Joint Architecture에 넣어서 진행
            cur_joint = Joint_Arch("End Site", parent)
            gWJointArchitecture.append(cur_joint)

            # End Site 표현
            end_0_or_continue_1 = 0

        elif (line_sep[0] == "{") :
            # 괄호가 열린 경우 기존의 joint가 새로운 부모가 되든지 유지함
            if (end_0_or_continue_1 == 1) :
                parent = cur_joint
            gWJointArchitecture.append(Joint_Arch("{", None))

        elif (line_sep[0] == "}") :
            # 괄호가 닫힌 경우 기존의 joint로 돌아오든지 위의 단계로 감
            if (end_0_or_continue_1 == 0) :
                # 유지
                end_0_or_continue_1 = 1
            else :
                # 위의 단계로 감
                cur_joint = cur_joint.get_parent()
                parent = cur_joint.get_parent()
            gWJointArchitecture.append(Joint_Arch("}", None))

    for temp in gWJointArchitecture : 
        if (temp.get_num_of_channels() != 0) :
            for channel in temp.get_channel_list() :
                num = len(channel)
                M = np.identity(4)
                
                for index in range(num) :
                    channel_order = temp.get_channel_order_list()
                    th = np.radians( -channel[index] )
                    cos = np.cos(th)
                    sin = np.sin(th)

                    if (channel_order[index].lower() == "xrotation") :
                        Rotation = np.array( [ [1., 0., 0., 0., ],
					[0., cos, -sin, 0.],
					[0., sin, cos, 0.],
					[0., 0., 0., 1.] ] )
                        M = Rotation @ M

                    elif (channel_order[index].lower() == "yrotation") :
                        Rotation = np.array( [ [cos, 0., sin, 0., ],
					[0., 1., 0., 0.],
					[-sin, 0., cos, 0.],
					[0., 0., 0., 1.] ] )
                        M = Rotation @ M

                    elif (channel_order[index].lower() == "zrotation") :
                        Rotation = np.array( [ [cos, -sin, 0., 0., ],
					[sin, cos, 0., 0.],
					[0., 0., 1., 0.],
					[0., 0., 0., 1.] ] )
                        M = Rotation @ M            
                   
                temp.append_RM(M)

    gWRM = gWJointArchitecture[0].get_RM()


    fd.close()
    gWFPS = int(1 / gWFrameTime)


###################################
##########      main 함수       ##########
###################################
def main():
    if not glfw.init():
        return
    window = glfw.create_window(1000,1000,'ClassAssignment3', None, None)
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
    glfw.make_context_current(window)
    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
