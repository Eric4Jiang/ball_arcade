import cv2
import numpy as np
import math

class Ball:
    # minimum speed = 10, max speed = 25
    # velocity = true velocity of ball (float)
    # screenVelocity = int velocity to display
    def setVelocity(self, velocity):
        self.velocity = np.array(velocity)
        self.updateHypotenuse()
        
        self.screenVelocity = np.array([math.ceil(velocity[0]),
                                        math.ceil(velocity[1])])

    def updateHypotenuse(self):
        self.hypotenuse = math.sqrt(self.velocity[0]**2 + self.velocity[1]**2)

    def setCenter(self, center):
        self.center = center

    def setColor(self, color):
        self.color = color

    def setRadius(self, radius):
        self.radius = radius

    # bounce ball in x direction
    def bounceX(self):
        self.setVelocity([-self.velocity[0], self.velocity[1]])

    # bounce ball in y direction
    def bounceY(self):
        self.setVelocity([self.velocity[0], -self.velocity[1]])

    def distanceSqToPoint(self, point):
        x, y = point
        return (self.center[0] - x)**2 + (self.center[1] - y)**2

    # *point = (1, 2) dimension array
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

    # checks for collosion with another object
    # *obj = list of points (x ,y) of the object
    # @returns i, index of the point of collision
    def collideWithContour(self, cnt):
        if len(cnt) < 100:
            print ("contour too small")
            return None
        # make sure ball is within max range of contour
        if not len(cnt) > self.center[0] - cnt[0][0] - self.radius \
                and len(cnt) > self.center[1] - cnt[0][1] - self.radius: 
            return None

        i = 0
        for point in cnt:
             if self.containsPoint(point): # return True
                return i
            #i += 1
        return None

    # Bounces ball off object
    # Vnew = -(2 * (V dot N)*N - V) -> http://www.3dkingdoms.com/weekly/weekly.php?a=2
    #   *V = velocity vector of ball
    #   *N = unit velocity vector of surface to bounce off (Normal force)
    # 
    # Argmuents:
    #   *obj = thing ball is bouncing off
    #   *pos = point that hit ball
    def bounceOffContour(self, cnt, pos):
        # find slope at pos using neighbors
        m, b = np.polyfit([cnt[pos-1][0], cnt[pos][0], cnt[pos+1][0]],
                            [cnt[pos-1][1], cnt[pos][1], cnt[pos+1][1]],
                            1)
        print ("slope = {}".format(m))

        # find N
        angle = math.atan(m)
        print ("angle = ", angle)
        # take negative reciprocal (sin(x)/cos(x) -> -cos(x)/sin(x)) for perpendicular sloepe
        nX = math.sin(angle)
        nY = -1 * math.cos(angle)
        
        # determine which side contour we're bouncing off of
        ball_to_left_and_slope_pos = self.center[0] < cnt[pos][0] and m > 0
        ball_to_right_and_slope_neg = self.center[0] > cnt[pos][0] and m < 0
        if ball_to_left_and_slope_pos or ball_to_right_and_slope_neg:
            nX *= -1
            nY *= -1
        
        N = np.array([nX, nY])

        # plug into formula for output vector
        R = -1 * (2 * np.dot(self.velocity, N) * N - self.velocity)
        VN = np.dot(self.velocity, N)
        VNN = 2*VN*N
        VNNV = VNN - self.velocity
       
        print ("Velocity = {} N = {}".format(self.velocity, N))
        print ("(V . N) = ", VN)
        print ("2 * VN * N = ", VNN)
        print ("2VNN - velocity = ", VNNV)
        print ("New velocity = ", R)
        self.setVelocity(R)

    # Fields:
    #   *radius = determines size of ball
    #   *center = [x, y] of center of ball
    #   *color = (B, G, R) color of ball
    def __init__(self, radius, center, color):
        self.setRadius(radius)
        self.setCenter(center)
        self.setColor(color)

