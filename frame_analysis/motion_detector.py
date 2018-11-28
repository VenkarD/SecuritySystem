import cv2
from collections import deque

from .i_frame_analyzer import IFrameAnalyzer


### ПАРАМЕТРЫ ###
"""
FRAMES_DELAY = 2    # Задержка для сравнения - текущий кадр сравнивается
                    #   с тем, что был такое число кадров назад.
BLUR_W = 25         # Величина размывания кадра по OX
BLUR_H = BLUR_W     # Величина размывания кадра по OY
DETECT_LEVEL = 5    # Нижний порог для определения движения - разность
                    #   оттенков серого, от 0 до 255
DILATE_VALUE = 15   # Толщина обводки обнаруженного движения - позволяет
                    #   объединить много мелких областей, расположенных
                    #   рядом, в одну, но также раширяет область в стороны
MIN_AREA = 3000     # Минимальная площадь изменившейся области. Если
                    #   движение обнаружено в площади меньше данной, то
                    #   оно будет проигнорировано
"""
#################


class MotionDetector(IFrameAnalyzer):
    def __init__(self, frames_delay=2, blur_w=25, blur_h=25,
                 detect_level=5, dilate_value=15, min_area=3000):
        super().__init__()
        self.frames_delay = frames_delay
        self.blur_w = blur_w
        self.blur_h = blur_h
        self.detect_level = detect_level
        self.dilate_value = dilate_value
        self.min_area = min_area

        self.delayed_gray = deque([], self.frames_delay)

    def process(self, frame):
        curr_frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        curr_frame_gray = cv2.GaussianBlur(curr_frame_gray,
                                           (self.blur_w, self.blur_h), 0)
        self.delayed_gray.appendleft(curr_frame_gray)
        if len(self.delayed_gray) < self.frames_delay:
            return []

        diff_frame = cv2.absdiff(self.delayed_gray[self.frames_delay - 1],
                                 curr_frame_gray)
        thresh_frame = cv2.threshold(diff_frame, self.detect_level, 255,
                                     cv2.THRESH_BINARY)[1]
        thresh_frame = cv2.dilate(thresh_frame, None,
                                  iterations=self.dilate_value)

        (_, all_contours, _) = cv2.findContours(thresh_frame.copy(),
                                                cv2.RETR_EXTERNAL,
                                                cv2.CHAIN_APPROX_SIMPLE)
        ret_contours = []
        for contour in all_contours:
            if cv2.contourArea(contour) < self.min_area:
                continue
            (x, y, w, h) = cv2.boundingRect(contour)
            ret_contours.append((x, y, x + w, y + h))
        return ret_contours

    def clear_queue(self):
        self.delayed_gray.clear()
