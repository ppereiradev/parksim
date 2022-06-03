
from django.conf import settings

import torch
# version inspection
import detectron2
print(f"Detectron2 version is {detectron2.__version__}")

# import some common detectron2 utilities
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog
import cv2

import requests
import numpy as np
import os

class CountCars():
    def __init__(self):
        self.cfg = get_cfg()
        self.cfg.MODEL.DEVICE = "cpu"
        # add project-specific config (e.g., TensorMask) here if you're not running a model in detectron2's core library
        self.cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model
        # Find a model from detectron2's model zoo. You can use the https://dl.fbaipublicfiles... url as well
        self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
        


    def count(self,im):
        results = {}
        #im = cv2.imdecode(np.fromstring(img, np.uint8), cv2.IMREAD_UNCHANGED)
        predictor = DefaultPredictor(self.cfg)
        outputs = predictor(im)
        
        obj = self.onlyKeepCarClass(outputs, im)
        v = Visualizer(im[:, :, ::-1], MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]), scale=1.0)
        out = v.draw_instance_predictions(obj.to("cpu"))

        font                   = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText = (50,50)
        fontScale              = 2
        fontColor              = (255,255,255)
        lineType               = 2


        img = cv2.putText(out.get_image(),'CARROS: ' + str(len(obj)), bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
        return len(obj)
        


    def onlyKeepCarClass(self,outputs, im):
        cls = outputs['instances'].pred_classes
        scores = outputs["instances"].scores
        masks = outputs['instances'].pred_masks
        boxes = outputs['instances'].pred_boxes
        
        # remove all other classes which are not person(index:0)
        indx_to_remove = (cls != 2).nonzero().flatten().tolist()

        # delete corresponding arrays
        cls = np.delete(cls.cpu().numpy(), indx_to_remove)
        scores = np.delete(scores.cpu().numpy(), indx_to_remove)
        masks = np.delete(masks.cpu().numpy(), indx_to_remove, axis=0)
        #boxes = np.delete(boxes.cpu().numpy(), indx_to_remove, axis=0)

        # convert back to tensor and move to cuda
        cls = torch.tensor(cls).to('cpu')
        scores = torch.tensor(scores).to('cpu')
        masks = torch.tensor(masks).to('cpu')
        #boxes = torch.tensor(boxes).to('cuda:0')

        # not interested in boxes
        outputs['instances'].remove('pred_boxes')

        # create new instance obj and set its fields
        obj = detectron2.structures.Instances(image_size=(im.shape[0], im.shape[1]))
        obj.set('pred_classes', cls)
        obj.set('scores', scores)
        obj.set('pred_masks', masks)
        return obj
    

