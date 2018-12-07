import numpy as np
import cv2
import tensorflow as tf
from datetime import datetime


# сделать staticmethod/classmethod?
def mouse_drawing(event, x, y, flags, detector):
    if event == cv2.EVENT_LBUTTONDOWN:
        detector.points.append((x, y))
    elif event == cv2.EVENT_RBUTTONDOWN:
        if len(detector.points) > 0:
            detector.points.pop()
    elif event == cv2.EVENT_MOUSEMOVE:
        detector.next_point = (x, y)


def in_region(x, y, xp, yp):
    c = False
    for i in range(len(xp)):
        if (((yp[i] <= y and y < yp[i - 1]) or (yp[i - 1] <= y and y < yp[i])) and \
                (x > (xp[i - 1] - xp[i]) * (y - yp[i]) / (yp[i - 1] - yp[i]) + xp[i])):
            c = not c
    return c


class BorderDetector:
    def __init__(self):
        # сделать points изначально np.ndarray чтобы каждый раз не превращать в np_points?
        self.points = []
        self.next_point = None
        self.is_drawing = False
        self.has_regions = False
        self.window_id = None

    def draw_regions(self, frame, color, thickness):
        #regions_frame = np.copy(frame)
        np_points = None
        if self.is_drawing and self.next_point is not None:
            if len(self.points) > 0:
                np_points = np.append(self.points, [self.next_point], axis=0)
            else:
                np_points = np.array([self.next_point])
        else:
            np_points = np.array(self.points)

        """for center_position in self.points:
            cv2.circle(regions_frame, center_position, 2, (0, 0, 255), -1)"""

        cv2.polylines(frame, np.int32([np_points]), True, color, thickness)
        """stencil = np.zeros(regions_frame.shape).astype(regions_frame.dtype)
        stencil[:] = (255, 255, 255) # далее белым по белому?
        if len(np_points) >= 3:
            cv2.fillPoly(stencil, np.int32([np_points]), (255, 255, 255))
            regions_frame = cv2.bitwise_and(regions_frame, stencil)"""
        return frame

    def are_rectangles_in_regions(self, rectangles):
        np_points = np.array(self.points)
        result = []
        for i in range(len(rectangles)):
            result.append(in_region((rectangles[i][1] + rectangles[i][3]) / 2,
                                    (rectangles[i][0] + rectangles[i][2]) / 2,
                                    np_points[:, 0],
                                    np_points[:, 1]))
        return result



    def clear_points(self):
            self.points = []
            self.has_regions = False

    def start_selecting_region(self, window_id):
        self.is_drawing = True
        self.window_id = window_id
        cv2.namedWindow(self.window_id)
        cv2.setMouseCallback(self.window_id, mouse_drawing, param=self)

    def end_selecting_region(self):
        self.next_point = None
        self.is_drawing = False
        self.has_regions = len(self.points) >= 3
        if not self.has_regions:
            self.clear_points()
        cv2.destroyWindow(self.window_id)
        self.window_id = None
