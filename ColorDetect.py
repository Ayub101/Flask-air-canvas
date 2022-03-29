import cv2 as cv
import numpy as np
color = {"blue":[[90,100,100],[120,255,255]],"yellow":[[22,93,0],[35,255,255]],"red":[[0,200,255],[20,255,255]],'orange':
[[12,200,255],[25,255,255]]}
class Pen:
    def __init__(self):
        self.lower = np.array(color['yellow'][0])
        self.upper = np.array(color['yellow'][1])
        self.kernel = np.ones((5,5),np.uint8)
        self.x1=0
        self.y1=0
        self.xe,self.ye = 550,60
        self.incanv = True
        self.canvas = None

    def write(self,frame,color,size):  
        self.frame = cv.cvtColor(frame,cv.COLOR_BGR2HSV)
        if self.incanv:
            self.canvas = np.zeros_like(frame)
            self.incanv = False
        mask = cv.inRange(self.frame,self.lower,self.upper)
        mask = cv.bitwise_and(self.frame,self.frame,mask=mask)
        # Erosion Eats away the white part while dilation expands it.
        mask = cv.erode(mask,self.kernel,iterations = 1)
        mask = cv.dilate(mask,self.kernel,iterations = 2)
        mask = cv.cvtColor(mask,cv.COLOR_HSV2BGR)
        gray = cv.cvtColor(mask,cv.COLOR_BGR2GRAY)
        contours, hierarchy = cv.findContours(gray,cv.RETR_TREE,cv.CHAIN_APPROX_NONE)
        if contours and cv.contourArea(max(contours,key = cv.contourArea)) > 200:
            max_area = max(contours,key = cv.contourArea)
            x,y,w,h = cv.boundingRect(max_area)
            if self.x1!=0 and self.y1!=0:
                #print(x,y,h,w)
                x2=x+(w//2)
                y2=y+(h//2) 
                cv.line(self.canvas,(self.x1,self.y1),(x2,y2),color,size)
                self.x1=x2
                self.y1=y2
            else:
                self.x1=x
                self.y1=y
                #cv.line(self.canvas,(200,100),(300,300),(0,255,0),20)
            # cv.rectangle(self.frame,(x,y),(x+w,y+h),(0,255,255),2)        
        else:
            self.x1=0
            self.y1=0
        self.frame = cv.cvtColor(self.frame,cv.COLOR_HSV2BGR)
        return cv.flip(self.canvas,1)

    def erase(self,frame,x,y):
        cv.line(frame,(self.xe,self.ye),(x,y),(0,0,0),70)
        self.xe,self.ye = x,y
        self.canvas = cv.flip(frame,1)
        return self.canvas
        


#cam = cv.VideoCapture(1)
# Creating A 5x5 kernel for morphological operations

# pen = Pen()
# if cam.isOpened():
#     while True:
#         _ ,frame = cam.read()
#         canvas = pen.write(frame,(0,255,0),3)
#         #sta = np.hstack(frame)
#         frame = cv.flip(frame,1)
#         frame = cv.add(canvas,frame)
#         cv.imshow("win",frame)
#         #cv.imshow('d',cv.resize(sta,None,fx=0.6,fy=0.6))
#         if cv.waitKey(5) & 0xFF == 27:
#             break



