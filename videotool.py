import cv2
import numpy as np

import cameramode

PROCESS_PERIOD = 1  # период обновления информации детекторами


def in_polygon(x, y, xp, yp):
    c = 0
    for i in range(len(xp)):
        if (((yp[i] <= y and y < yp[i - 1]) or (yp[i - 1] <= y and y < yp[i])) and \
                (x > (xp[i - 1] - xp[i]) * (y - yp[i]) / (yp[i - 1] - yp[i]) + xp[i])): c = 1 - c
    return c

class VideoTool:
    def __init__(self, src, color1=(0, 255, 0), color2=(0, 0, 255), color3=(255, 0, 0), init_fc = 0):
        self.set_video_source(src)
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        self.frame_counter = init_fc
        self.last_gf_func = lambda frame: frame  # последний результат обработки (в виде функции)
        self.mode = cameramode.ORIGINAL
        self.object_detector = None
        self.border_detector = None
        self.motion_detector = None
        self.is_playing = True
        print('VideoTool created:', self.fps, 'FPS')

    def set_video_source(self, src):
        self.video = cv2.VideoCapture(src)
        self.fps = self.video.get(cv2.CAP_PROP_FPS)
        self.freq_ms = 1000 / self.fps
        self.frame_w = self.video.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.frame_h = self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)
        # fourcc = cv2.VideoWriter_fourcc(*'XVID')
        # self.out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))


    def get_smart_frame(self, width, height):
        retval, original = self.video.read()
        # TODO: обработать отсутствие кадра
        assert original is not None, 'Кадр не получен'

        frame = cv2.resize(original, (width, height), interpolation=cv2.INTER_AREA)
        # bad code
        if self.border_detector.isPressMarkUpButton:
            cv2.imshow(self.border_detector.windowId, self.border_detector.get_frame_polygon(frame))

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.frame_counter = (self.frame_counter + 1) % PROCESS_PERIOD
        if self.mode == cameramode.ORIGINAL or\
                self.mode == cameramode.DETECT_BORDERS and \
                not self.border_detector.isPolyCreated:
            return frame

        if self.frame_counter == 0:
            if self.mode == cameramode.DETECT_OBJECTS:
                boxes, scores, classes = self.object_detector.process(frame)
                self.last_gf_func = lambda frame:  \
                    self.get_frame_objects(frame, boxes, classes)
            elif self.mode == cameramode.DETECT_MOTION:
                boxes = self.motion_detector.process(frame)
                self.last_gf_func = lambda frame: \
                    self.get_frame_motion(frame, boxes)
            elif self.mode == cameramode.DETECT_BORDERS:
                boxes, scores, classes = self.object_detector.process(frame)
                self.last_gf_func = lambda frame: \
                    self.get_frame_borders(frame, boxes, classes)
            else:
                self.last_gf_func = lambda frame: frame
        return self.last_gf_func(frame)

    def get_frame_objects(self, frame, boxes, classes):
        for i in range(len(boxes)):
            box = boxes[i]
            cv2.rectangle(frame, (box[3], box[2]), (box[1], box[0]), self.color1, 2)
            y = box[0] - 15 if box[0] - 15 > 15 else box[0] + 15
            cv2.putText(frame, self.object_detector.labels[classes[i] - 1], (box[1], y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color1, 2)
        return frame

    def get_frame_motion(self, frame, boxes):
        for i in range(len(boxes)):
            box = boxes[i]
            cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), self.color1, 2)
        return frame

    def get_frame_borders(self, frame, boxes, classes):
        if not self.border_detector.isPolyCreated:
            return frame

        frame = self.border_detector.get_frame_polygon(frame)  # ?
        #print(len(boxes), 'object(s) detected')

        for i in range(len(boxes)):
            box = boxes[i]
            (startX, startY, endX, endY) = box
            label = self.object_detector.labels[classes[i] - 1]

            # TODO создать функцию, которая рисует рамки с подписями
            if self.border_detector.isPolyCreated:
                # print('ok its draw')
                points = np.array(self.border_detector.circles)
                if (in_polygon((box[1] + box[3]) / 2, (box[0] + box[2]) / 2, points[:, 0], points[:, 1])):
                    # print('draw 1')
                    # if(isPixelsInArea(startX, startY, endX, endY,points[:, 0], points[:, 1])):
                    cv2.rectangle(frame, (box[1], box[0]), (box[3], box[2]), self.color2, 2)
                    y = box[0] - 15 if box[0] - 15 > 15 else box[0] + 15
                    cv2.putText(frame, "not a good guy", (box[1], y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color2, 2)
                else:
                    # print('draw 2')
                    cv2.rectangle(frame, (box[1], box[0]), (box[3], box[2]), self.color1, 2)
                    y = box[0] - 15 if box[0] - 15 > 15 else box[0] + 15
                    cv2.putText(frame, label, (box[1], y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color1, 2)
        return frame

    def get_security_detected(self, width=500, img=None):
        pass  # TODO

    def is_displayable(self):
        return self.mode == cameramode.ORIGINAL or \
               self.mode == cameramode.DETECT_OBJECTS or \
               self.mode == cameramode.DETECT_MOTION or \
               self.mode == cameramode.DETECT_BORDERS

    # def video_rec(self):
    #     while cap.isOpened():
    #         ret, frame = cap.read()
    #         if ret:
    #             out.write(frame)

    def play(self):
        self.is_playing = True

    def stop(self):
        self.is_playing = False

    def close(self):
        self.video.release()

    def set_mode(self, mode):
        self.mode = mode
