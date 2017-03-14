import cv2 
import numpy as np
import math
from random import randint

from ball import Ball

class BallGame:
    def __init__(self, img):
        self.balls = []
        self.height, self.width, _ = img.shape

    # initalizes balls with random velocities
    def initBalls(self, numOfBalls, radius):    
        for i in range(numOfBalls):
            ball = Ball(radius, center=[self.width//2, self.height//2], color=(0,255,0))
            # start balls in random direction
            ball.setVelocity([randint(-20,20), randint(-20,20)])
            self.balls.append(ball)
   
   # reverse ball direction if it's out image boundaries
    def keepBallInBoundaries(self, ball, image):
        height, width, channels = image.shape
        # bounce off top or bottom
        if ball.center[1] + ball.radius + ball.velocity[1] > self.height \
                or ball.center[1] - ball.radius + ball.velocity[1] < 0:
            print (ball.velocity, ball.center, ball.radius, self.height)
            ball.bounceY()
        # bounce off left or right boundaries
        if ball.center[0] + ball.radius + ball.velocity[0] > self.width \
                or ball.center[0] -ball.radius + ball.velocity[0] < 0:
            ball.bounceX()
