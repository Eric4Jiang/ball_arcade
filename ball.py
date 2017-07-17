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

    def distToPoint(self, point):
        x, y = point
        return math.sqrt((self.center[0] - x)**2 + (self.center[1] - y)**2)
        # return (self.center[0] - x)**2 + (self.center[1] - y)**2

    # *point = (1, 2) dimension array
    # checks if point (x, y) is within the ball
    def containsPoint(self, point):
        return self.distToPoint(point) < self.radius

    # checks for collision with another ball
    # The distance between their centers must be between
    #   * the sum of their radii
    #   * the difference of their radii
    def collideWithBall(self, ball2):
        dist = self.distToPoint(ball2.center)
        return dist >= (self.radius - ball2.radius) \
                and dist <= (self.radius + ball2.radius)

    # checks for collosion with another object
    # *obj = list of points (x ,y) of the objec
    # @returns - pos of point in contour that ball hit 
    def collideWithContour(self, cnt):
        self.POINTS_THRESH = 4

        if len(cnt) < self.POINTS_THRESH:
            print ("cnt too small")
            return None

        # make sure ball is within max range of contour
        if not len(cnt) > self.center[0] - cnt[0][0] - self.radius \
                and len(cnt) > self.center[1] - cnt[0][1] - self.radius: 
            print ("cnt too far")
            return None

        # check if ball lies on any of the contours edges(which are striaght lines)
        # https://stackoverflow.com/questions/17692922/check-is-a-point-x-y-is-between-two-points-drawn-on-a-straight-line
       # for i in range(len(cnt) - 1):
       #     a = cnt[i]
       #     b = cnt[i+1]
       #     # distance of ca + cb = ab
       #     dist_ab = math.sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2)
       #     dist_to_a = self.distToPoint(a)
       #     dist_to_b = self.distToPoint(b)
       #     diff = dist_ab - (dist_to_a + dist_to_b)
       #     DIST_THRESH = math.sqrt(self.radius/2 + math.sqrt((self.radius/2)**2 + dist_ab**2))
       #     print ("Threshold = {}".format(DIST_THRESH))
       #     print("ab = {}, ac = {}, bc = {} -> {}".format(dist_ab, dist_to_a, dist_to_b, abs(diff)))
       #     if abs(diff) < DIST_THRESH:
       #         print ("hit contour {}, {}".format(i, i + 1))
       #         return i
        i = 0
        for point in cnt:
             if self.containsPoint(point):
                print ("hit")
                return i
             i += 1
        return None

    # Bounces ball off object
    # Vnew = -(2 * (V dot N)*N - V) -> http://www.3dkingdoms.com/weekly/weekly.php?a=2
    #   *V = velocity vector of ball
    #   *N = unit velocity vector of surface to bounce off (Normal force)
    # 
    # Argmuents:
    #   *p1, p2 = forms an edge that the ball will bounce off
    def bounceOffContour(self, cnt, pos):
        # find slope of line formed by p1, p2 
        #m, b = np.polyfit(p1, p2, 1)
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
        # mid_point = ((p1[0] + p2[0])/2, (p1[1]+ p2[1])/2)
        #ball_to_left_and_slope_pos = self.center[0] < mid_point[0] and m > 0
        #ball_to_right_and_slope_neg = self.center[0] > mid_point[0] and m < 0
        
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
