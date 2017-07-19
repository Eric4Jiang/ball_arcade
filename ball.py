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
    # *obj = list of points (x ,y) of the object 
    # @returns - pos of point in contour that ball hit 
    def collideWithContour(self, cnt):
        self.CNT_LEN_THRESH = 4
        cnt_len = len(cnt)
        if cnt_len < self.CNT_LEN_THRESH:
            print ("cnt too small")
            return None

        distX_ball_to_cnt = self.center[0] - cnt[0][0] - self.radius
        distY_ball_to_cnt = self.center[1] - cnt[0][1] - self.radius

        # make sure ball is within max range of contour
        if not (len(cnt) > distX_ball_to_cnt and len(cnt) > distY_ball_to_cnt): 
            print ("cnt too far")
            return None
#        h = np.linalg.norm(cnt[1] - cnt[0])
#        w = np.linalg.norm(cnt[2] - cnt[1])
#        hyp = math.hypot(h, w)
#        #print ("hyp = {}".format(hyp))
#        if not (hyp > distX_ball_to_cnt and hyp > distY_ball_to_cnt):
#            print ("cnt too far")
#            return None
#        
#        # check if ball lies on any of the contours edges(which are striaght lines)
#        # https://stackoverflow.com/questions/17692922/check-is-a-point-x-y-is-between-two-points-drawn-on-a-straight-line
#        for i in range(cnt_len):
#            a = None
#            b = None
#            # check line formed by last point and first point
#            if i == (cnt_len - 1):
#                a = cnt[cnt_len - 1]
#                b = cnt[0]
#            else:
#                a = cnt[i]
#                b = cnt[i + 1]
#            DIST_THRESH = 3
#            # distance of ca + cb = ab
#            dist_ab = math.sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2)
#            dist_to_a = self.distToPoint(a)
#            dist_to_b = self.distToPoint(b)
#            #DIST_THRESH = math.hypot(dist_ab, self.radius) + self.radius
#            dist_ac_bc = abs(dist_ab - (dist_to_a + dist_to_b))
#            if dist_ac_bc <= DIST_THRESH:
#                #print ("Threshold = {}".format(DIST_THRESH))
#                #print("ab = {}, ac = {}, bc = {} -> {}".format(dist_ab, dist_to_a, dist_to_b, dist_ac_bc))
#                #print ("hit contour {}, {}".format(i, i + 1))
#                return i
            #else:
             #   print ("NOOOOOOOOOOOOOOOOOOOOOOO")
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
        #p1 = cnt[pos]
        #p2 = None
        #if (len(cnt) - 1) != pos:
        #    p2 = cnt[pos+1]
        #else:
        #    p2 = cnt[0]
        
        # find slope of line formed by p1, p2 
        #m, b = np.polyfit(p1, p2, 1)
        m, b = np.polyfit([cnt[pos-1][0], cnt[pos][0], cnt[pos+1][0]],
                            [cnt[pos-1][1], cnt[pos][1], cnt[pos+1][1]],
                            1)
        # find N
        angle = math.atan(m)
        print ("angle = ", angle)
        # take negative reciprocal (sin(x)/cos(x) -> -cos(x)/sin(x)) for perpendicular sloepe
        nX = math.sin(angle)
        nY = -1 * math.cos(angle)
        
        # determine which side contour we're bouncing off of
        #mid_point = ((p1[0] + p2[0])/2, (p1[1]+ p2[1])/2)
        #ball_to_left_and_slope_pos = self.center[0] < mid_point[0] and m > 0
        #ball_to_right_and_slope_neg = self.center[0] > mid_point[0] and m < 0
    
        ball_to_left_and_slope_pos = self.center[0] < cnt[pos][0] and m > 0
        ball_to_right_and_slope_neg = self.center[0] > cnt[pos][0] and m < 0
        #ball_below_cnt = self.center[1] < m * self.center[0] + (p1[1] - m * p1[0])
        
        if ball_to_left_and_slope_pos or ball_to_right_and_slope_neg:
        #if ball_below_cnt:
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
    #   *radius = r, the radius of the  ball
    #   *center = [x, y] of center of ball
    #   *color = (B, G, R) color of ball
    def __init__(self, radius, center, color):
        self.setRadius(radius)
        self.setCenter(center)
        self.setColor(color)
