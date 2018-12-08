import numpy as np
import cv2
import tensorflow as tf
from datetime import datetime

from .i_frame_analyzer import IFrameAnalyzer

class SecurityDetector(IFrameAnalyzer):
    def __init__(self, object_detector):
        super().__init__()
        self.security_curr_state = False
        self.security_prev_state = False
        self.security_check_series = 5
        self.security_check_period = 30 * 30 - self.security_check_series
        self.security_frame_counter = self.security_check_period - 1
        self.log_str = ""

        self.object_detector = object_detector

    def get_security_detected(self, frame):

        # print("detected: ", "security_curr_state = ", self.security_curr_state,
        #                     " security_prev_state = ", self.security_prev_state,
        #                     " security_check_series = ", self.security_check_series,
        #                     " security_check_period = ", self.security_check_period,
        #                     " security_frame_counter = ", self.security_frame_counter)
        self.log_str = ""
        self.security_frame_counter = (self.security_frame_counter + 1) % self.security_check_period


        if self.security_frame_counter == 0:
            self.security_prev_state = self.security_curr_state
            self.security_curr_state = False
        if not self.security_curr_state and self.security_frame_counter < self.security_check_series:
            boxes, scores, classes = self.object_detector.process(frame)
            #print ("boxes = ", boxes)
            #for oneclass in classes:
            if boxes is not None:  # person
                print("Security_person!")
                self.security_curr_state = True
        elif self.security_frame_counter == self.security_check_series and \
                self.security_curr_state != self.security_prev_state:
            print("almost")
            print('{}: охранник {}'.format(datetime.now(). \
                                           strftime('%d.%m.%y %H:%M'), \
                                           'на месте' if self.security_curr_state else 'отсутствует'))
            self.log_str = '{}: охранник {}'.format(datetime.now(). \
                                               strftime('%d.%m.%y %H:%M'), \
                                               'на месте' if self.security_curr_state else 'отсутствует')

        if (self.log_str != ""):
            f = open('log.txt', 'a')
            f.write(self.log_str + '\n')
            f.close()

        """if security_state != (len(boxes) > 0):
            security_state = (len(boxes) > 0)
        if security_state:
            logger.debug("Security came")
        else:
            logger.debug("Security gone")"""
