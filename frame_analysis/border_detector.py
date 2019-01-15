import numpy as np
import cv2
import tensorflow as tf
from datetime import datetime


# сделать staticmethod/classmethod?
def mouse_drawing(event, x, y, flags, detector):
    if detector.curr_region is None:
        return

    if event == cv2.EVENT_LBUTTONDOWN:
        detector.curr_region.points.append((x, y))
    elif event == cv2.EVENT_RBUTTONDOWN:
        if len(detector.curr_region.points) > 0:
            detector.curr_region.points.pop()
    elif event == cv2.EVENT_MOUSEMOVE:
        detector.next_point = (x, y)


def in_region(x, y, xp, yp):
    c = False
    for i in range(len(xp)):
        if (((yp[i] <= y and y < yp[i - 1]) or (yp[i - 1] <= y and y < yp[i])) and \
                (x > (xp[i - 1] - xp[i]) * (y - yp[i]) / (yp[i - 1] - yp[i]) + xp[i])):
            c = not c
    return c


class Region:
    def __init__(self, name=''):
        self.name = name
        self.points = []

    def clear_points(self):
        self.points = []


class BorderDetector:
    def __init__(self):
        # сделать points изначально np.ndarray чтобы каждый раз не превращать в np_points?
        self.regions = []
        self.curr_region = None
        self.next_point = None
        self.is_drawing = False
        self.has_regions = False
        self.window_id = None

    def draw_regions(self, frame, color, thickness):
        #regions_frame = np.copy(frame)
        for region in self.regions:
            print(region)
            np_points = None
            if self.is_drawing and self.next_point is not None:
                if len(region.points) > 0:
                    np_points = np.append(region.points, [self.next_point], axis=0)
                else:
                    np_points = np.array([self.next_point])
            else:
                np_points = np.array(region.points)
            print('Hoba')

            """for center_position in self.points:
                cv2.circle(regions_frame, center_position, 2, (0, 0, 255), -1)"""

            cv2.polylines(frame, np.int32([np_points]), True, color, thickness)
            print('wtf')
            """stencil = np.zeros(regions_frame.shape).astype(regions_frame.dtype)
            stencil[:] = (255, 255, 255) # далее белым по белому?
            if len(np_points) >= 3:
                cv2.fillPoly(stencil, np.int32([np_points]), (255, 255, 255))
                regions_frame = cv2.bitwise_and(regions_frame, stencil)"""
        return frame

    def are_rectangles_in_regions(self, rectangles):
        result = []
        for region in self.regions:
            np_points = np.array(region.points)
            for i in range(len(rectangles)):
                result.append(in_region((rectangles[i][1] + rectangles[i][3]) / 2,
                                        (rectangles[i][0] + rectangles[i][2]) / 2,
                                        np_points[:, 0],
                                        np_points[:, 1]))
        return result

    def add_region(self, region):
        self.regions.append(region)

    def get_region_by_index(self, index):
        return self.regions[index]

    def remove_region_by_index(self, index):
        raise NotImplementedError("You have to implement this method! (нужно будет отделить управление регионами от самого детектора)")

    def start_selecting_region(self, region, window_id):
        self.curr_region = region
        self.is_drawing = True
        self.window_id = window_id
        cv2.namedWindow(self.window_id)
        cv2.setMouseCallback(self.window_id, mouse_drawing, param=self)

    def end_selecting_region(self):
        self.next_point = None
        self.is_drawing = False
        print('Ending')
        print(self.curr_region)
        print(self.curr_region.points)
        if len(self.curr_region.points) < 3:
            self.curr_region.clear_points()
        cv2.destroyWindow(self.window_id)
        self.window_id = None
        self.curr_region = None
