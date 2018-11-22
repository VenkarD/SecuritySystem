from imutils.video import VideoStream
from tkinter import Tk, Text, BOTH, W, N, E, S, Canvas, NW
from tkinter.ttk import Frame, Button, Label, Style
from PIL import Image, ImageTk
import numpy as np
import imutils
import time
import cv2
import matplotlib.path as mplPath
import winsound

duration = 1000  # millisecond
freq = 440  # Hz

prototxt = "MobileNetSSD_deploy.prototxt.txt"
model = "MobileNetSSD_deploy.caffemodel"
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]
NotHidden = {"person", "cat", "dog"}
net = cv2.dnn.readNetFromCaffe(prototxt, model)

global circles
circles = []
global isPressMarkUpButton
isPressMarkUpButton = False
global isPolyCreated
isPolyCreated = False


def GetImages(fr):
    img = cv2.cvtColor(fr, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(img)
    return img

def mouse_drawing(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Left click")
        circles.append((x, y))

# Function that show: is point in polygon. or not.
def inPolygon(x, y, xp, yp):
    c=0
    for i in range(len(xp)):
        if (((yp[i]<=y and y<yp[i-1]) or (yp[i-1]<=y and y<yp[i])) and \
            (x > (xp[i-1] - xp[i]) * (y - yp[i]) / (yp[i-1] - yp[i]) + xp[i])): c = 1 - c
    return c

def isPixsInArea(StartX, StartY, EndX, EndY, xp, yp):
    ret = False
    for y in range(StartY, EndY):
        for x in range(StartX, EndX):
            if(inPolygon(x,y, xp, yp)):
                ret = True
    return ret

class UI(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("Windows")
        self.pack(fill=BOTH, expand=True)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.canvas = Canvas(self)
        self.canvas.grid(row=1, column=0, columnspan=2, rowspan=4, padx=5, sticky=E + W + S + N)

        abtn = Button(self, text="Activate Rec")
        abtn.grid(row=1, column=3)

        bbtn = Button(self, text="Activaation else")
        bbtn.grid(row=2, column=3)

        cbtn = Button(self, text="Another button")
        cbtn.grid(row=3, column=3 )

        ebtn = Button(self, text="Another button")
        ebtn.grid(row=4, column=3)

        polygramButton = Button(self, text="Mark up borders")
        polygramButton.grid(row=1, column=2)

        polygramButton.bind("<Button-1>", self.markUp)

    # event for press markUp button
    def markUp(self,event):
        global isPressMarkUpButton
        if(isPressMarkUpButton == False):
            isPressMarkUpButton = True
        elif(isPressMarkUpButton == True):
            isPressMarkUpButton = False

    def createImg(self, mode, i1, i2, i3, i4=None):
        if mode:
            self.canvas.create_image(0, 0, image=i1, anchor=NW)
            self.canvas.create_image(510, 0, image=i2, anchor=NW)
            self.canvas.create_image(200, 400, image=i3, anchor=NW)
        else:
            pass


class Video:
    def __init__(self, src=0, color=(0, 255, 0), color2=(0, 0, 255), color3=(255, 0, 0), confidence=0.4):
        self.isPeopleRecg = True
        self.isAlarmEnabled = True

        self.vs = VideoStream(src=src).start()
        self.vc = cv2.VideoCapture(0)
        print("start")
        time.sleep(2.0)
        self.color = color
        self.color2 = color2
        self.color3 = color3
        self.isPlay = True
        self.frame = self.get_frame()
        self.confidence = confidence

    def get_frame(self, width=500):
        frame = self.vs.read()
        if frame is None:
            _, frame = self.vc.read()
        frame = imutils.resize(frame, width=width)

        return frame

    # For first cam-capture
    def detect_green_gumanoids(self):
        frame = self.get_frame()
        if not self.isPeopleRecg:
            return frame
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
        net.setInput(blob)
        detections = net.forward()
        print("detection")
        for i in np.arange(0, detections.shape[2]):
            if detections[0, 0, i, 2] < 0.3:
                continue
            if CLASSES[int(detections[0, 0, i, 1])] != "person":
                continue
            print("detected")
            label = "Gumanoid"
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            cv2.rectangle(frame, (startX, startY), (endX, endY), self.color, 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color, 2)
        return frame

    def get_image(self):
        img = self.detect_green_gumanoids()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(img)
        return img

    def get_polygon_image(self):
        global circles
        global isPressMarkUpButton
        global isPolyCreated
        img = self.get_frame()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cv2.namedWindow("Frame")
        points = np.array(circles)

        if isPressMarkUpButton == True:
            cv2.setMouseCallback("Frame", mouse_drawing)
            for center_position in circles:
                cv2.circle(img, center_position, 2, (0, 0, 255), -1)

        if len(points) >= 4 and isPressMarkUpButton == False:
            cv2.polylines(img, np.int32([points]), 1, (255, 255, 255))
            isPolyCreated = True
            stencil = np.zeros(img.shape).astype(img.dtype)
            stencil[:] = (255, 255, 255)
            cv2.fillPoly(stencil, np.int32([points]), (255, 255, 255))
            img = cv2.bitwise_and(img, stencil)

        cv2.imshow("Frame", img)

        key = cv2.waitKey(1)
        if key == ord("d"):
            circles = []
            isPressMarkUpButton = False
            isPolyCreated = False
            img = self.get_frame()

        #img = Image.fromarray(img)
        #img = ImageTk.PhotoImage(img)

        return img

    def get_polygon_frame(self, width=500):
        frame = self.get_polygon_image()

        if not self.isPeopleRecg:
            return frame
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
        net.setInput(blob)
        detections = net.forward()
        print (detections)
        print("detection")
        for i in np.arange(0, detections.shape[2]):
            if detections[0, 0, i, 2] < 0.3:
                continue
            if CLASSES[int(detections[0, 0, i, 1])] != "person":
                continue
            print("detected")
            label = "Gumanoid"
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            if (isPolyCreated == True):
                points = np.array(circles)
                if(inPolygon((startX+endX)/2, (startY+endY)/2, points[:, 0], points[:, 1])):
                #if(isPixsInArea(startX, startY, endX, endY,points[:, 0], points[:, 1])):
                    cv2.rectangle(frame, (startX, startY), (endX, endY), self.color3, 2)
                    y = startY - 15 if startY - 15 > 15 else startY + 15
                    cv2.putText(frame, "not a good guy", (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color3, 2)
                    #winsound.Beep(freq, duration)
                else:
                    cv2.rectangle(frame, (startX, startY), (endX, endY), self.color, 2)
                    y = startY - 15 if startY - 15 > 15 else startY + 15
                    cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color, 2)



        frame = Image.fromarray(frame)
        frame = ImageTk.PhotoImage(frame)
        return frame

    def play(self):
        self.isPlay = True
        self.vs.play()

    def stop(self):
        self.isPlay = False
        self.vs.stop()

    def is_alarm(self, state=None):
        if state is None:
            return self.isAlarmEnabled
        else:
            self.isAlarmEnabled = state

    def is_recognition(self, state=None):
        if state is None:
            return self.isPeopleRecg
        else:
            self.isPeopleRecg = state


def main():
    v1 = Video(src=0)
    #v2 = Video(src=0)
    #v3 = Video(src=0)
    v4 = v1

    root = Tk()
    root.geometry("300x300+0+0")
    app = UI(root)
    while True:
        frame1 = v1.get_image()
        #frame2 = v2.get_image()
        #frame3 = v3.get_image()
        frame4 = v4.get_polygon_frame()

        print("isPressMarkUpButton = ", isPressMarkUpButton)
        app.createImg(1, frame1, frame4, frame4)

        root.update()
        # cv2.imshow("main1", frame1)
        frame4 = np.asarray(frame4)
        #cv2.imshow("Frame",frame4)

        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
            v1.stop()
            #v2.stop()
            #v3.stop()
            v4.stop()
            cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
