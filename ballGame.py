import cv2
import numpy as np
import math
import itertools
from random import randint, choice

from ball import Ball

class BallGame:
    def __init__(self, h, w):
        self.balls = []

        # used to keep balls inside window
        self.height = h # y
        self.width = w # x

        # thresholding values
        self.LEN_THRESH = 100
        self.AREA_THRESH = 1000

        self.lower = np.array([65, 150, 150]) # blue
        self.upper = np.array([138, 255, 255])

    # initalizes balls with random velocities
    def initBalls(self, numOfBalls, radius):
        for i in range(numOfBalls):
            # start green ball with specified radius, random location on the screen
            ball = Ball(radius,
                    [randint(radius, self.width-radius), randint(radius, self.height-radius)],
                    color=(0,255,0))
            # start balls in random direction
            x = choice([(-30, -20), (20, 30)])
            y = choice([(-30, -20), (20, 30)])
            ball.setVelocity([randint(*x), randint(*y)])
            self.balls.append(ball)

    # reverse ball direction if it's out image boundaries
    def keepBallsInBoundaries(self):
        # print (self.height, self.width)
        for ball in self.balls:
            # bounce off top or bottom
            if ball.center[1] + ball.radius + ball.velocity[1] > self.height \
                    or ball.center[1] - ball.radius + ball.velocity[1] < 0:
                ball.bounceY()
            # bounce off left or right boundaries
            if ball.center[0] + ball.radius + ball.velocity[0] > self.width \
                    or ball.center[0] -ball.radius + ball.velocity[0] < 0:
                ball.bounceX()

    # bounces ball off other balls
    def bounceBallsOffBalls(self):
        for ball, ball2 in itertools.combinations(self.balls, 2):
            if ball.collideWithBall(ball2):
                # some math to calculate collision trajectories
                deltaY = (ball.center[1] - ball2.center[1])
                deltaX = (ball.center[0] - ball2.center[0])
                if deltaX == 0: # avoid divide by 0
                    deltaX = 1
                slope = deltaY / deltaX
                mag = (ball.hypotenuse + ball2.hypotenuse) / 2
                # scale factor
                scalar = mag / math.sqrt(1**2 + (slope)**2)

                vX1, vY1 = 1 * scalar, slope * scalar
                vX2, vY2 = 1 * scalar, slope * scalar

                # calculate directions balls goes
                if deltaX < 0:
                    vX1 *= -1
                else:
                    vX2 *= -1

                if deltaY < 0:
                    vY1 *= -1
                else:
                    vY2 *= -1

                ball.setVelocity([vX1, vY1])
                ball2.setVelocity([vX2, vY2])

    # finds blue objects
    # returns a list of contours(list of points)
    # if no contours, returns empty list
    def find_cnts(self, img):
        im_copy = img.copy()

        hsv = cv2.cvtColor(im_copy, cv2.COLOR_BGR2HSV)
        thresh = cv2.inRange(hsv, self.lower, self.upper) # blue
        # cv2.imshow("thresh", thresh)
        # cv2.waitKey(10)
        eroded = cv2.erode(thresh, (3,3), iterations=3)
        dilated = cv2.dilate(eroded, (3,3), iterations=3)
        m = cv2.moments(dilated)

#        cv2.imshow("dilated", dilated)
#        cv2.waitKey(10)
        _, contours, _ = cv2.findContours(dilated, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_SIMPLE)

        # filter contours
        goodContours = []
        for c in contours:
            # print ("len = ", len(c))
            # print ("area = ", cv2.contourArea(c))
            if len(c) > self.LEN_THRESH and cv2.contourArea(c) > self.AREA_THRESH:
                goodContours.append(c)

        return goodContours

    # Bounce all balls off any contours they collide with
    # contours = list of contours(list of points)
    def bounceBallsOffContours(self, cnts):
        if len(cnts) is 0:
            return

        cnts = np.array(cnts)
        resized_cnts = [] # reshape all cnts (Array of Array [1, 2] points)
                          # to Array of [N, 2], where N is the number of points in that cnt
        for c in cnts:
            resized_cnts.append(c.reshape(-1, 2).astype(np.int32))

        # check all contours for contact with ball
        for c in resized_cnts:
            for ball in self.balls:
                pos = ball.collideWithContour(c)
                #return pos
                if pos is not None:
                    ball.bounceOffContour(c, pos)
