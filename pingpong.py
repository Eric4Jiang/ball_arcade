import cv2
import numpy as np
import math

from ballGame import BallGame

class PingPong(BallGame):
    def __init__(self, img):
        super().__init__(img)

    # Start game
    # Ball will bounce off objects with certain color
    # @returns processed image with balls drawn
    def run(self, img):
        im_copy = img.copy()
       
        for ball in self.balls:
            super().keepBallInBoundaries(ball, img)
            ball.setCenter((ball.center[0] + ball.velocity[0], 
                           ball.center[1] + ball.velocity[1]))
            # Display ball moving visually
            cv2.circle(im_copy, ball.center, ball.radius, ball.color, thickness=-1)

        return im_copy
