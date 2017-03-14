import cv2
import numpy as np
import math

class Ball:
    # Fields:
    #   *radius = determines size of ball
    #   *center = [x, y] of center of ball
    #   *velocity = [x, y] where x is pixels to go horizontally
    #                      where y is pixels to go vertically
    #   *color = (B, G, R) color of ball
    def __init__(self, radius, center, color):
        self.radius = radius
        self.center = center
        self.velocity = [0, 0]
        self.color = color

    def setVelocity(self, velocity):
        self.velocity = velocity
        
    def setCenter(self, center):
        self.center = center

    def setColor(self, color):
        self.color = color

    def setRadius(self, radius):
        self.radius = radius

    def getMagnitude(self):
        return math.sqrt(self.velocity[0]**2 + self.velocity[1]**2)

    # bounce ball in x direction
    def bounceX(self):
        self.velocity[0] *= -1

    # bounce ball in y direction
    def bounceY(self):
        self.velocity[1] *= -1

    # checks if point (x, y) is within the ball
    def containsPoint(self, point):
        x, y = point
        return (x - self.center[0])**2 + (y - self.center[1])**2 < self.radius**2

    # checks for collision with another ball
    # The distance between their centers must be between
    #   * the sum of their radii
    #   * the difference of their radii
    def collideWithBall(self, ball2):
        distanceSq = (self.center[0] - ball2.center[0])**2 \
                      + (self.center[1] - ball2.center[1])**2
        return distanceSq >= (self.radius - ball2.radius)**2 \
                and distanceSq <= (self.radius + ball2.radius)**2
