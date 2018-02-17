#!/usr/bin/python

import cv2
import numpy as np
import time
import math
import sys
from random import randint

from pingpong import PingPong

if len(sys.argv) != 4:
    print ("Arguments: -gameMode(PingPong or Slide), -radius, -numOfBalls")
    sys.exit(0)

if __name__ == "__main__":
    gameMode = sys.argv[1]
    radius = int(sys.argv[2])
    numOfBalls = int(sys.argv[3])

    cap = cv2.VideoCapture(0)

    print("set width = ", cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640))
    print("set height = ", cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480))
    _, frame = cap.read()
    windowH, windowW, channels = frame.shape

    game = None
    if gameMode == "PingPong":
        game = PingPong(windowH, windowW)
        game.initBalls(numOfBalls, radius)
        print ("PingPong")

    while True:
        ret, frame = cap.read()
        out = game.run(frame)
        out = cv2.flip(out, 1)

        cv2.imshow(gameMode, out)
        cv2.waitKey(1)

        # pause
        if cv2.waitKey(50) & 0xFF == ord('p'):
            cv2.waitKey(0)

cap.release()
cv2.destroyAllWindows()
