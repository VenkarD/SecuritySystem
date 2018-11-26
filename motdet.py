
# Pyhton program to implement 
# WebCam Motion Detector
 
# importing OpenCV, time and Pandas library
import cv2, time, pandas
# importing datetime class from datetime library
from datetime import datetime
from collections import deque
 

### ПАРАМЕТРЫ ###

FRAMES_DELAY = 20   # Задержка для сравнения - текущий кадр сравнивается
                    #   с тем, что был такое число кадров назад.
BLUR_W = 9          # Величина размывания кадра по OX
BLUR_H = BLUR_W     # Величина размывания кадра по OY
DETECT_LEVEL = 20   # Нижний порог для определения движения - разность
                    #   оттенков серого, от 0 до 255
DILATE_VALUE = 15   # Толщина обводки обнаруженного движения - позволяет
                    #   объединить много мелких областей, расположенных
                    #   рядом в одну, но также раширяет область в стороны
MIN_AREA = 10000    # Минимальная площадь изменившейся области. Если
                    #   движение обнаружено в площади меньше данной, то
                    #   оно будет проигнорировано

#################


# Очередь кадров для сравнения
delayed_gray = deque([], FRAMES_DELAY)
 
# List when any moving object appear
motion_list = [ None, None ]
 
# Time of movement
time = []
 
# Initializing DataFrame, one column is start 
# time and other column is end time
df = pandas.DataFrame(columns = ["Start", "End"])
 
# Capturing video
video = cv2.VideoCapture('../people.mp4')
 
# Infinite while loop to treat stack of image as video
while True:
    # Reading frame(image) from video
    check, frame = video.read()
 
    # Initializing motion = 0(no motion)
    motion = 0

    # Converting color image to curr_frame_gray_scale image
    curr_frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 
    # Converting curr_frame_gray scale image to GaussianBlur 
    # so that change can be find easily
    curr_frame_gray = cv2.GaussianBlur(curr_frame_gray, (BLUR_W, BLUR_H), 0)
 
    # Добавляем текущий кадр в очередь, и если очередь
    # не заполнена, пропускаем итерацию
    delayed_gray.appendleft(curr_frame_gray)
    if len(delayed_gray) < FRAMES_DELAY:
        continue
 
    # Difference between static background 
    # and current frame(which is GaussianBlur)
    diff_frame = cv2.absdiff(delayed_gray[FRAMES_DELAY - 1], curr_frame_gray)
 
    # If change in between static background and
    # current frame is greater than DETECT_LEVEL it will show white color(255)
    thresh_frame = cv2.threshold(diff_frame, DETECT_LEVEL, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations = DILATE_VALUE)
 
    # Finding contour of moving object
    (_, cnts, _) = cv2.findContours(thresh_frame.copy(), 
                       cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
 
    for contour in cnts:
        if cv2.contourArea(contour) < MIN_AREA:
            continue
        motion = 1
 
        (x, y, w, h) = cv2.boundingRect(contour)
        # making green rectangle arround the moving object
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
 
    # Appending status of motion
    motion_list.append(motion)
 
    motion_list = motion_list[-2:]
 
    # Appending Start time of motion
    if motion_list[-1] == 1 and motion_list[-2] == 0:
        time.append(datetime.now())
 
    # Appending End time of motion
    if motion_list[-1] == 0 and motion_list[-2] == 1:
        time.append(datetime.now())
 
    # Displaying image in curr_frame_gray_scale
    cv2.imshow("Gray Frame", curr_frame_gray)
 
    # Displaying the difference in currentframe to
    # the staticframe(very first_frame)
    cv2.imshow("Difference Frame", diff_frame)
 
    # Displaying the black and white image in which if
    # intencity difference greater than DETECT_LEVEL it will appear white
    cv2.imshow("Threshold Frame", thresh_frame)
 
    # Displaying color frame with contour of motion of object
    cv2.imshow("Color Frame", frame)
 
    key = cv2.waitKey(1)
    # if q entered whole process will stop
    if key == ord('q'):
        # if something is movingthen it append the end time of movement
        if motion == 1:
            time.append(datetime.now())
        break
 
# Appending time of motion in DataFrame
for i in range(0, len(time), 2):
    df = df.append({"Start":time[i], "End":time[i + 1]}, ignore_index = True)
 
# Creating a csv file in which time of movements will be saved
df.to_csv("Time_of_movements.csv")
 
video.release()
 
# Destroying all the windows
cv2.destroyAllWindows()
