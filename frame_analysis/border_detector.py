import numpy as np
import cv2
import tensorflow as tf
from datetime import datetime


# сделать staticmethod/classmethod?
def mouse_drawing(event, x, y, flags, circles):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Left click")
        circles.append((x, y))
        print(len(circles), 'circles')

class BorderDetector:
    def __init__(self):
        # сделать circles изначально np.ndarraym чтобы каждый раз не превращать в points?
        self.circles = []
        self.isPressMarkUpButton = False
        self.isPolyCreated = False
        self.windowId = None

    def get_frame_polygon(self, frame):
        polygon_frame = np.copy(frame)
        points = np.array(self.circles)
        for center_position in self.circles:
            cv2.circle(polygon_frame, center_position, 2, (0, 0, 255), -1)

        cv2.polylines(polygon_frame, np.int32([points]), not self.isPressMarkUpButton, (255, 255, 255), 3)
        self.isPolyCreated = True
        stencil = np.zeros(polygon_frame.shape).astype(polygon_frame.dtype)
        stencil[:] = (255, 255, 255) # далее белым по белому?
        if len(points) >= 3:
            cv2.fillPoly(stencil, np.int32([points]), (255, 255, 255))
            polygon_frame = cv2.bitwise_and(polygon_frame, stencil)
        return polygon_frame

    def clearCircles():
            self.circles = []
            self.isPolyCreated = False

    def start_selecting_region(self, windowId):
        self.isPressMarkUpButton = True
        self.windowId = windowId
        cv2.namedWindow(self.windowId)
        cv2.setMouseCallback(self.windowId, mouse_drawing, param=self.circles)

    def end_selecting_region(self):
        self.isPressMarkUpButton = False
        self.isPolyCreated = len(self.circles) >= 3
        if not self.isPolyCreated:
            self.clearCircles()
        cv2.destroyWindow(self.windowId)
        self.windowId = None
