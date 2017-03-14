import cv2 
import numpy as np
import math
import itertools
from random import randint

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
            ball.setVelocity([randint(-20,20), randint(-20,20)])
            self.balls.append(ball)

    # reverse ball direction if it's out image boundaries
    def keepBallInBoundaries(self, ball, image):
        height, width, channels = image.shape
        # bounce off top or bottom
        if ball.center[1] + ball.radius + ball.velocity[1] > self.height \
                or ball.center[1] - ball.radius + ball.velocity[1] < 0:
            ball.bounceY()
        # bounce off left or right boundaries
        if ball.center[0] + ball.radius + ball.velocity[0] > self.width \
                or ball.center[0] -ball.radius + ball.velocity[0] < 0:
            ball.bounceX()

    # bounces ball off other balls
    def bounceOffBalls(self, img):
        for ball, ball2 in itertools.combinations(self.balls, 2):
            if ball.collideWithBall(ball2):
                # some math to calculate collision trajectories
                deltaY = (ball.center[1] - ball2.center[1])
                deltaX = (ball.center[0] - ball2.center[0])
                if deltaX == 0:
                    deltaX = 1
                slope = deltaY / deltaX
                magnitude = (ball.getMagnitude() + ball2.getMagnitude()) / 2
                # scale factor
                scalar = magnitude / math.sqrt(1**2 + (slope)**2)

                vX1, vY1 = max(10, 1 * scalar), max(10, slope * scalar)
                vX2, vY2 = max(10, 1 * scalar), max(10, slope * scalar)

                # calculate directions balls goes
                if deltaX < 0:
                    vX1 *= -1
                else:
                    vX2 *= -1

                if deltaY < 0:
                    vY1 *= -1
                else:
                    vY2 *= -1

                ball.setVelocity([int(vX1), int(vY1)])
                ball2.setVelocity([int(vX2), int(vY2)])

