import cv2
import numpy as np
import math

from ballGame import BallGame

class PingPong(BallGame):
    def __init__(self, img):
        super().__init__(img)
        self.LEN_THRESH = 1000
        self.AREA_THRESH = 10000
    
    # finds blue objects
    # returns a list of contours(list of points)
    def find_cnts(self, img):
        im_copy = img.copy()

        hsv = cv2.cvtColor(im_copy, cv2.COLOR_BGR2HSV)
        thresh = cv2.inRange(hsv, np.array([105,65,50]), np.array([130,255,255])) # blue
        eroded = cv2.erode(thresh, (3,3), iterations=3)
        dilated = cv2.dilate(eroded, (3,3), iterations=3)
        _, contours, _ = cv2.findContours(dilated, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_SIMPLE)
      
        # filter contours
        goodContours = []
        for c in contours:
            if len(c) > self.LEN_THRESH and cv2.contourArea(c) > self.AREA_THRESH:
                goodContours.append(c)

        return goodContours

    # Start game
    # Ball will bounce off objects with certain color
    # Balls will bounce off other balls
    # @returns processed image with balls drawn
    def run(self, img):
        im_copy = img.copy()

       # # diagonal 
       # line = [[x, self.height/self.width*x] for x in range(self.width//4)]
       # cnt = np.array(line).reshape((-1,1,2)).astype(np.int32)
       # 
       # re = cnt.reshape(-1,2).astype(np.int32)

       # cv2.drawContours(im_copy, cnt, -1, (0,255,0), thickness=3)
       # cv2.putText(im_copy, str((self.width//4)), (self.width//8, self.height//8), cv2.FONT_HERSHEY_PLAIN, 8, color=(0,0,0), thickness=3)
        cnts = self.find_cnts(img)
        #cnts_approx = [] # for each cnt estimate a polygon to fit it
        #hulls = []
        #boxes = []
        #for cnt in cnts:
        #    epsilon = 0.02*cv2.arcLength(cnt,True)
        #    approx = cv2.approxPolyDP(cnt,epsilon,True) #    cnts_approx.append(approx)
        #
        #    hull = cv2.convexHull(cnt)
        #    hulls.append(hull)
        #    rect = cv2.minAreaRect(cnt)
        #    box = cv2.boxPoints(rect)
        #    box = np.int0(box)
        #    boxes.append(box)
        #cv2.drawContours(im_copy, boxes, -1, (0,255,0), thickness=3);

        cv2.drawContours(im_copy, cnts, -1, (0,255,0), thickness=3)

        # hull = list of points
        # box = list of points
        # drawContours(img, list of list of points, color, thickness)

        super().bounceBallsOffBalls()
        #pos = super().bounceBallsOffContours(boxes)
        super().bounceBallsOffContours(cnts)
        super().keepBallsInBoundaries()
        #if len(boxes) != 0 and pos is not None:
        #    b = None
        #    a = tuple(boxes[0][pos])
        #    if (len(boxes[0]) - 1) != pos:
        #        b = tuple(boxes[0][pos+1])
        #    else:
        #        b = tuple(boxes[0][0])
        #    cv2.circle(im_copy, a, 25, (0,0,0), thickness=-1)
        #    cv2.circle(im_copy, b, 25, (255,0,255), thickness=-1)
        
        for ball in self.balls:
            # Move balls
            ball.setCenter((ball.center[0] + ball.screenVelocity[0], 
                           ball.center[1] + ball.screenVelocity[1]))
            # Display ball moving visually
            cv2.circle(im_copy, ball.center, ball.radius, ball.color, thickness=-1)
            #cv2.putText(im_copy, str(ball.center[0] - re[0][0] - ball.radius), ball.center, cv2.FONT_HERSHEY_PLAIN, 4, color=(0,255,0), thickness=2)

       
        return im_copy
