import cv2 as cv
import mediapipe as mp
import numpy as np
import math
class handTraking():
    def __init__(self):
        # initializing the mediapipe
        self.mp_drawing = mp.python.solutions.drawing_utils
        self.mp_hands = mp.python.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.7,min_tracking_confidence=0.7)
        self.numOfHands = 0
        self.hieght,self.width = 100,100
        self.xPosition,self.yPosition = 550,60
        self.color = 255,255,255

# Tracking hands of user
    def trakHands(self,cam,frame):
        self.frame = cv.flip(frame,1)
        self.frame = cv.cvtColor(self.frame, cv.COLOR_BGR2RGB)
        self.frame.flags.writeable = True
        if cam.isOpened():
            self.results = self.hands.process(self.frame)
            coord =self.co_ordinate()
            #print(coord)
            self.drawLandmarks() #drawing realtime hand landmarks
            self.drawRect() #making earser
            if coord is not None:
                #self.distance(coord[1][0],coord[2][0])
                #print(self.dis_I_T,self.dis_M_I)
               # for j in range(self.numOfHands):
                    #drawing circle on index finger
                    #self.frame = cv.circle(self.frame, coord[1][j], 10, (123, 255, 0), 2)
                    #checking distance between index and middle finger is les tha 0.06
                if self.dis_M_I < 0.06:
                    #checking position of finger is inside or ouside the eraser
                    if  self.checkInside(coord[1]):
                        self.xPosition = coord[1][0][0]
                        self.yPosition = coord[1][0][1]
                        #setting color of eraser little darker 
                        self.color = 225,255,248
                else:
                    self.color =255,255,255
            self.frame = cv.cvtColor(self.frame, cv.COLOR_RGB2BGR)   
            return {'frame':self.frame,'erase':[self.xPosition,self.yPosition]}
#option for drawing hand land marks
    def drawLandmarks(self):
        if self.results.multi_hand_landmarks:
                for hand_landmarks in self.results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(self.frame,hand_landmarks,self.mp_hands.HAND_CONNECTIONS
                                              ,self.mp_drawing.DrawingSpec(color=(0,0,255)),
                                              self.mp_drawing.DrawingSpec(color=(0,255,0)))
#locate the coordinates of index ,middle and thumb
    def co_ordinate(self):
        if self.results.multi_hand_landmarks:
            landmarks_index =[]
            landmarks_thumb =[]
            landmarks_middle = []
            coordIndex = []
            coordThumb = []
            coordMiddle = []
            self.numOfHands = len(self.results.multi_hand_landmarks)
            for i in range(self.numOfHands):
                landmarks_index.append(self.results.multi_hand_landmarks[i].landmark[8])
                landmarks_thumb.append(self.results.multi_hand_landmarks[i].landmark[4])
                landmarks_middle.append(self.results.multi_hand_landmarks[i].landmark[12])
            
            self.dis_M_I = self.distance(landmarks_middle[0],landmarks_index[0])
            #self.dis_I_T = self.distance(landmarks_index[0],landmarks_thumb[0])
            for i in range(self.numOfHands): 
                coordIndex.append(tuple(np.multiply(np.array((landmarks_index[i].x,landmarks_index[i].y)),[self.frame.shape[1],self.frame.shape[0]]).astype(int)))
                coordThumb.append(tuple(np.multiply(np.array((landmarks_thumb[i].x,landmarks_thumb[i].y)),[self.frame.shape[1],self.frame.shape[0]]).astype(int)))
                coordMiddle.append(tuple(np.multiply(np.array((landmarks_middle[i].x,landmarks_middle[i].y)),[self.frame.shape[1],self.frame.shape[0]]).astype(int)))
           # dis = math.sqrt((coord_i[0]-coord_t[0])**2 + (coord_i[1]-coord_t[1])**2)
            fingerPositions = [coordThumb,coordIndex,coordMiddle]
            return fingerPositions
            
            #print(coord)
            #frame = cv2.circle(frame, coord, 10, (0, 255, 0), 2)

            #print(results.multi_hand_landmarks[0].landmark[8])
#finding distance between two coordinate
    def distance(self,coord1,coord2):
       dis = math.sqrt((coord1.x-coord2.x)**2 + (coord1.y-coord2.y)**2)
       return dis
#drawing eraser
    def drawRect(self):
        x1 = self.xPosition-self.width//2
        y1 = self.yPosition-self.hieght//2
        x2 = self.xPosition+self.width//2
        y2 = self.yPosition+self.hieght//2
        self.frame = cv.rectangle(self.frame,(x1,y1),(x2,y2),self.color,cv.FILLED)
        self.frame = cv.putText(self.frame,'Eraser', (self.xPosition-30,self.yPosition), cv.FONT_HERSHEY_PLAIN,
                       1, (0,0,0), 2, cv.LINE_AA)
#cheking coordinate is inside the eraser
    def checkInside(self,coord):
        x1, y1 = self.xPosition-self.width//2,self.yPosition-self.hieght//2
        x2, y2 = self.xPosition+self.width//2,self.yPosition+self.hieght//2
        if x1 < coord[0][0] < x2 and y1 < coord[0][1] < y2:
            return True
        else:
            return False