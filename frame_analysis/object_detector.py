import numpy as np
import tensorflow as tf

from .i_frame_analyzer import IFrameAnalyzer


class ObjectDetector(IFrameAnalyzer):
    # bad code
    def __init__(self, detection_graph, labels, classes_to_detect, confidence_level):
        super().__init__()      
        self.detection_graph = detection_graph      
        """self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(path_to_ckpt, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')"""

        self.default_graph = self.detection_graph.as_default()
        self.sess = tf.Session(graph=self.detection_graph)
        self.labels = labels

        # Definite input and output Tensors for detection_graph
        self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
        # Each box represents a part of the image where a particular object was detected.
        self.detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
        # Each score represent how level of confidence for each of the objects.
        # Score is shown on the result image, together with the class label.
        self.detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
        self.detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
        self.num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')

        self.classes_to_detect = classes_to_detect
        self.confidence_level = confidence_level

    def process(self, frame):
        if len(self.classes_to_detect) <= 0 or self.confidence_level > 1:
            return [], [], []

        # Expand dimensions since the trained_model expects frames to have shape: [1, None, None, 3]
        frame_np_expanded = np.expand_dims(frame, axis=0)

        # Actual detection.
        (boxes, scores, classes, num) = self.sess.run(
            [self.detection_boxes, self.detection_scores, self.detection_classes, self.num_detections],
            feed_dict={self.image_tensor: frame_np_expanded})

        im_height, im_width, _ = frame.shape
        all_boxes = [None for i in range(boxes.shape[1])]
        for i in range(boxes.shape[1]):
            all_boxes[i] = (int(boxes[0, i, 0] * im_height),
                            int(boxes[0, i, 1] * im_width),
                            int(boxes[0, i, 2] * im_height),
                            int(boxes[0, i, 3] * im_width))

        all_scores = scores[0].tolist()
        all_classes = [int(x) for x in classes[0].tolist()]

        ret_boxes = []
        ret_scores = []
        ret_classes = []
        for i in range(len(all_boxes)):
            if all_classes[i] in self.classes_to_detect and all_scores[i] > self.confidence_level:
                ret_boxes.append(all_boxes[i])
                ret_scores.append(all_scores[i])
                ret_classes.append(all_classes[i])

        # чем полезен int(num[0]) ?
        # print('len(all_boxes) =', len(ret_boxes), 'int(num[0]) =', int(num[0]))
        return ret_boxes, ret_scores, ret_classes

    def close(self):
        self.sess.close()
        # self.default_graph.close()  # AttributeError: '_GeneratorContextManager' object has no attribute 'close'
