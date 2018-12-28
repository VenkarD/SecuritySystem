import numpy as np
import tensorflow as tf
import face_recognition
import cv2

from .i_frame_analyzer import IFrameAnalyzer


class FaceRecognizer(IFrameAnalyzer):
    unknown_face_name = 'Unknown'

    @staticmethod
    def get_face_encoding(image):
        return face_recognition.face_encodings(image)[0]

    def __init__(self, known_face_encodings, known_face_names):
        super().__init__()
        self.known_face_encodings = known_face_encodings
        self.known_face_names = known_face_names

    def process(self, frame):
        # Resize frame of video to 1/4 size for faster face recognition processing
        #small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = frame[:, :, ::-1]

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame, 1, "hog")
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = FaceRecognizer.unknown_face_name

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = self.known_face_names[first_match_index]

            face_names.append(name)

        for i in range(len(face_locations)):
            face_locations[i] = (
                face_locations[i][3],
                face_locations[i][0],
                face_locations[i][1],
                face_locations[i][2]
            )
        print(face_locations, face_names)
        return face_locations, face_names
        """ Остаток от того что было:
        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            # top *= 4
            # right *= 4
            # bottom *= 4
            # left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)"""
