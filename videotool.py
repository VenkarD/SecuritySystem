import cv2
import numpy as np

import cameramode

PROCESS_PERIOD = 1  # период обновления информации детекторами


class VideoTool:
    @staticmethod
    def draw_rectangle(frame, rectangle, color, label=None):
        cv2.rectangle(frame, (rectangle[0], rectangle[1]), (rectangle[2], rectangle[3]), color, 2)
        if label is not None:
            y = rectangle[1] - 15 if rectangle[1] - 15 > 15 else rectangle[1] + 15
            cv2.putText(frame, label, (rectangle[0], y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    def __init__(self, src, color1=(0, 255, 0), color2=(255, 0, 0), color3=(0, 0, 255), init_fc = 0):
        self.set_video_source(src)
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        self.frame_counter = init_fc
        self.last_gf_func = lambda frame: frame  # последний результат обработки (в виде функции)
        self.mode = cameramode.ORIGINAL
        self.object_detector = None
        self.motion_detector = None
        self.border_detector = None
        self.security_detector = None
        self.is_playing = True
        self.is_borders_mode = False
        print('VideoTool created:', self.fps, 'FPS')

    def set_video_source(self, src):
        self.video = cv2.VideoCapture(src)
        self.fps = self.video.get(cv2.CAP_PROP_FPS)
        self.freq_ms = int(1000 / self.fps)
        self.frame_w = self.video.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.frame_h = self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)
        # fourcc = cv2.VideoWriter_fourcc(*'XVID')
        # self.out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))


    def get_frame(self, width, height, mode=None, bgr_to_rgb=True):
        retval, original = self.video.read()
        # TODO: обработать отсутствие кадра
        assert original is not None, 'Кадр не получен'
        if mode is None:
            mode = self.mode

        frame = cv2.resize(original, (width, height), interpolation=cv2.INTER_AREA)
        # bad code
        """if self.border_detector.is_drawing:
            cv2.imshow(self.border_detector.window_id, self.border_detector.draw_regions(frame))"""
        if bgr_to_rgb:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.frame_counter = (self.frame_counter + 1) % PROCESS_PERIOD
        if mode == cameramode.ORIGINAL:
            return frame

        if self.frame_counter == 0:
            if mode == cameramode.DETECT_OBJECTS:
                boxes, scores, labels = self.object_detector.process(frame)
                self.last_gf_func = lambda frame:  \
                    self.draw_retections(frame, boxes, labels)
            elif mode == cameramode.DETECT_MOTION:
                boxes = self.motion_detector.process(frame)
                self.last_gf_func = lambda frame: \
                    self.draw_retections(frame, boxes)
            elif mode == cameramode.DETECT_SECURITY:
                self.last_gf_func = lambda frame: \
                    self.get_security_detected(frame)
            else:
                self.last_gf_func = lambda frame: frame
        return self.last_gf_func(frame)

    def draw_retections(self, frame, boxes, labels=None):
        if labels is None:
            labels = [None] * len(boxes)
        colors = None
        if self.is_borders_mode:
            frame = self.border_detector.draw_regions(frame)
            are_rects_in_regs = self.border_detector.are_rectangles_in_regions(list(boxes))
            colors = [self.color2 if in_region else self.color1 for in_region\
                      in are_rects_in_regs]
        else:
            colors = [self.color1] * len(boxes)

        for i in range(len(boxes)):
            self.draw_rectangle(frame, boxes[i], colors[i], labels[i])
        return frame

    def get_security_detected(self, frame):
        #pass
        self.security_detector.get_security_detected(frame)
        #print ("get_security_detected is working")

    def is_displayable(self):
        return self.mode == cameramode.ORIGINAL or \
               self.mode == cameramode.DETECT_OBJECTS or \
               self.mode == cameramode.DETECT_MOTION

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
