import cv2 
import numpy as np
import math
import itertools
from random import randint, choice

from ball import Ball

class BallGame:
    def __init__(self, img):
        self.balls = []
        self.height, self.width, _ = img.shape

    # initalizes balls with random velocities
    def initBalls(self, numOfBalls, radius):    
        for i in range(numOfBalls):
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

    # Bounce all balls off any contours they collide with
    # contours = list of contours(list of points)
    def bounceBallsOffContours(self, cnts):
        if len(cnts) is 0:
            return

        cnts = np.array(cnts)
        resized_cnts = [] # convert cnt Array of Array of point to Array of points
        for c in cnts:
            resized_cnts.append(c.reshape(-1, 2).astype(np.int32))

        # check all contours for contact with ball
        for c in resized_cnts:
            for ball in self.balls:
                pos = ball.collideWithContour(c)
                if pos is not None:
                    # p1 = c[pos]
                    # p2 = c[pos+1]
                    # ball.bounceOffContour(p1, p2)
                    ball.bounceOffContour(c, pos)
