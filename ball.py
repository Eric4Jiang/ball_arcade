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

    # bounce ball in x direction
    def bounceX(self):
        print ("SIDE")
        self.velocity[0] *= -1

    # bounce ball in y direction
    def bounceY(self):
        print ("TOP/BOTTOM")
        self.velocity[1] *= -1
