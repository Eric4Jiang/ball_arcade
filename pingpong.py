import cv2
import numpy as np
import math

from ballGame import BallGame

class PingPong(BallGame):
    def __init__(self, img):
        super().__init__(img)
    
    # finds blue objects
    def proc_img(self, img):
        im_copy = img.copy()

        hsv = cv2.cvtColor(im_copy, cv2.COLOR_BGR2HSV)
        thresh = cv2.inRange(hsv, np.array([110,50,50]), np.array([130,255,255]))
        eroded = cv2.erode(thresh, (3,3), iterations=3)
        dilated = cv2.dilate(eroded, (3,3), iterations=3)
        _, contours, _ = cv2.findContours(dilated, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_SIMPLE)
      
        # filter contours
        goodContours = []
        LEN_THRESH = 1000
        AREA_THRESH = 10000
        for c in contours:
            if len(c) > LEN_THRESH and cv2.contourArea(c) > AREA_THRESH:
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
        cnts = self.proc_img(img)
        cv2.drawContours(im_copy, cnts, -1, (0,255,0), thickness=3)

        super().bounceBallsOffBalls()
        #super().bounceBallsOffContours(cnts)
        super().keepBallsInBoundaries()
    
        for ball in self.balls:
            # Move balls
            ball.setCenter((ball.center[0] + ball.screenVelocity[0], 
                           ball.center[1] + ball.screenVelocity[1]))
            # Display ball moving visually
            cv2.circle(im_copy, ball.center, ball.radius, ball.color, thickness=-1)
            #cv2.putText(im_copy, str(ball.center[0] - re[0][0] - ball.radius), ball.center, cv2.FONT_HERSHEY_PLAIN, 4, color=(0,255,0), thickness=2)

        return im_copy
