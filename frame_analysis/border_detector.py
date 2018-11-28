import numpy as np
import cv2
import tensorflow as tf
from datetime import datetime

# from .i_frame_analyzer import IFrameAnalyzer


# сделать staticmethod/classmethod?
def mouse_drawing(event, x, y, flags, circles):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Left click")
        circles.append((x, y))
        print(len(circles), 'circles')

# class BorderDetector(IFrameAnalyzer):
class BorderDetector:
    def __init__(self):
        # super().__init__()
        # сделать circles изначально np.ndarraym чтобы каждый раз не превращать в points?
        self.circles = []
        self.isPressMarkUpButton = False
        self.isPolyCreated = False
        self.windowId = None

    def get_polygon_image(self, frame):
        points = np.array(self.circles)
        for center_position in self.circles:
            cv2.circle(frame, center_position, 2, (0, 0, 255), -1)

        # if len(points) >= 4 and self.isPressMarkUpButton == False:
        if len(points) >= 3 and self.isPressMarkUpButton == False:
            cv2.polylines(frame, np.int32([points]), True, (255, 255, 255), 3)
            self.isPolyCreated = True
            stencil = np.zeros(frame.shape).astype(frame.dtype)
            stencil[:] = (255, 255, 255) # далее белым по белому?
            cv2.fillPoly(stencil, np.int32([points]), (255, 255, 255))
            frame = cv2.bitwise_and(frame, stencil)
        return frame

    """def get_polygon_frame(self):
        frame = self.get_polygon_image(width)
        # (w, h) = frame.shape[:2]

        boxes, scores, classes = self.detect(width=width, img=frame)
        print(len(boxes), 'object(s) detected')

        for i in range(len(boxes)):
            box = boxes[i]
            # box = box * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box
            label = self.detector.labels[classes[i] - 1]

            if self.isPolyCreated:
                # print('ok its draw')
                points = np.array(circles)
                if (in_polygon((box[1] + box[3]) / 2, (box[0] + box[2]) / 2, points[:, 0], points[:, 1])):
                    # print('draw 1')
                    # if(isPixelsInArea(startX, startY, endX, endY,points[:, 0], points[:, 1])):
                    cv2.rectangle(frame, (box[1], box[0]), (box[3], box[2]), self.color3, 2)
                    y = box[0] - 15 if box[0] - 15 > 15 else box[0] + 15
                    cv2.putText(frame, "not a good guy", (box[1], y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color3, 2)
                else:
                    # print('draw 2')
                    cv2.rectangle(frame, (box[1], box[0]), (box[3], box[2]), self.color1, 2)
                    y = box[0] - 15 if box[0] - 15 > 15 else box[0] + 15
                    cv2.putText(frame, label, (box[1], y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color1, 2)
        return frame"""

    def clearCircles():
            self.circles = []
            self.isPolyCreated = False

    """def start_selecting_region(self, frame):
        # bad code
        self.isPressMarkUpButton = True
        self.windowId = datetime.now()
        cv2.namedWindow(self.windowId)
        cv2.setMouseCallback(self.windowId, mouse_drawing)
        while isPressMarkUpButton:
            cv2.imshow(self.windowId, get_polygon_image(frame))"""
    def start_selecting_region(self, windowId):
        self.isPressMarkUpButton = True
        self.windowId = windowId
        cv2.namedWindow(self.windowId)
        cv2.setMouseCallback(self.windowId, mouse_drawing, param=self.circles)
        """while isPressMarkUpButton:
            cv2.imshow(self.windowId, get_polygon_image(frame))"""

    def end_selecting_region(self):
        self.isPressMarkUpButton = False
        self.isPolyCreated = len(self.circles) >= 3
        if not self.isPolyCreated:
            self.clearCircles()
        cv2.destroyWindow(self.windowId)
        self.windowId = None

    """
    def process(self, frame):
        # Expand dimensions since the trained_model expects frames to have shape: [1, None, None, 3]
        frame_np_expanded = np.expand_dims(frame, axis=0)

        # Actual detection.
        (boxes, scores, classes, num) = self.sess.run(
            [self.detection_boxes, self.detection_scores, self.detection_classes, self.num_detections],
            feed_dict={self.image_tensor: frame_np_expanded})

        im_height, im_width, _ = frame.shape
        boxes_list = [None for i in range(boxes.shape[1])]
        for i in range(boxes.shape[1]):
            boxes_list[i] = (int(boxes[0, i, 0] * im_height),
                             int(boxes[0, i, 1] * im_width),
                             int(boxes[0, i, 2] * im_height),
                             int(boxes[0, i, 3] * im_width))

        return boxes_list, scores[0].tolist(), [int(x) for x in classes[0].tolist()], int(num[0])

    def close(self):
        self.sess.close()
        # self.default_graph.close()  # AttributeError: '_GeneratorContextManager' object has no attribute 'close'
        """

