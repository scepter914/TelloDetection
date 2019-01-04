
import matplotlib.pyplot as plt
import cv2

import chainer
import chainercv

from chainercv.datasets import voc_bbox_label_names
#from chainercv.experimental.links import YOLOv2Tiny
import yolo_v2_tiny
from chainercv.links import YOLOv2
from chainercv.links import YOLOv3
from chainercv import utils
from chainercv.visualizations import vis_bbox

class Detection():
    def __init__(self, model_ = 'yolo_v2_tiny', gpu_ = -1 , pretrained_model_ = 'voc0712'):
        self.count = 0
        if model_ == 'yolo_v2':
            self.model = YOLOv2(
                n_fg_class=len(voc_bbox_label_names),
                pretrained_model=pretrained_model_)
        elif model_ == 'yolo_v2_tiny':
            self.model = yolo_v2_tiny.YOLOv2Tiny(
                n_fg_class=len(voc_bbox_label_names),
                pretrained_model=pretrained_model_)
        elif model_ == 'yolo_v3':
            self.model = YOLOv3(
                n_fg_class=len(voc_bbox_label_names),
                pretrained_model=pretrained_model_)
        if gpu_ >= 0:
            chainer.cuda.get_device_from_id(gpu_).use()
            self.model.to_gpu()
        print("finish init detection")

    def detection(self,image):
        self.count += 1
        #img = utils.read_image(image, color=True)
        #img = image
        img = cv2.resize(image, (600, 400))
        img = img[:, :, ::-1]  # BGR -> RGB
        img = img.transpose((2, 0, 1))  # HWC -> CHW
        self.bboxes, self.labels, self.scores = self.model.predict([img])
        self.bbox, self.label, self.score = self.bboxes[0], self.labels[0], self.scores[0]
        vis_bbox(img, self.bbox, self.label, self.score, label_names=voc_bbox_label_names)
        plt.savefig("pic/" + str(self.count))
        #print(self.bboxes)
        print(self.labels)
        #print(self.scores)
        #print(img)
        #print(img.shape)
        img = img.transpose((1, 2, 0))
        return img

