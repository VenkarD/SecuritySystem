import numpy as np
import tensorflow as tf

from .i_frame_analyzer import IFrameAnalyzer

class ObjectDetector(IFrameAnalyzer):
    # bad code
    def __init__(self, path_to_ckpt, path_to_labels):
        super().__init__()
        self.detection_graph = tf.Graph()
        with tf.device("/gpu:0"):
            with self.detection_graph.as_default():
                od_graph_def = tf.GraphDef()
                with tf.gfile.GFile(path_to_ckpt, 'rb') as fid:
                    serialized_graph = fid.read()
                    od_graph_def.ParseFromString(serialized_graph)
                    tf.import_graph_def(od_graph_def, name='')

        self.default_graph = self.detection_graph.as_default()
        self.sess = tf.Session(graph=self.detection_graph)

        # Definite input and output Tensors for detection_graph
        self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
        # Each box represents a part of the image where a particular object was detected.
        self.detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
        # Each score represent how level of confidence for each of the objects.
        # Score is shown on the result image, together with the class label.
        self.detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
        self.detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
        self.num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')

        with open(path_to_labels) as f:
            self.labels = f.readlines()
        self.labels = [s.strip() for s in self.labels]

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
