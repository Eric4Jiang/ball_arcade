#!/usr/bin/python

import cv2
import numpy as np
import time
import math
import sys
from random import randint

from pingpong import PingPong

if len(sys.argv) != 4:
    print ("Arguments: -gameMode, -radius, -numOfBalls")
    sys.exit(0) 

if __name__ == "__main__":
    gameMode = sys.argv[1]
    radius = int(sys.argv[2])
    numOfBalls = int(sys.argv[3])
    cap = cv2.VideoCapture(0)

    _, test = cap.read()
    game = None
    if gameMode == "PingPong":
        game = PingPong(test)
        game.initBalls(numOfBalls, radius)

    while True:
        ret, frame = cap.read()
        out = game.run(frame)
        
        cv2.imshow(gameMode, out)
        cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()

