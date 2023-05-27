import torch
from ultralytics.yolo.engine.predictor import BasePredictor
from ultralytics.yolo.engine.results import Results
from ultralytics.yolo.utils import  ops
from ultralytics.yolo.data.augment import LetterBox
from bentoml.io import Image
from pathlib import Path
import numpy as np
import yaml
from rfai.config import CLASS_CFG
import cv2
import base64
from ultralytics.yolo.cfg import get_cfg

class RFaiPredctor(BasePredictor):
    def __init__(self, overrides=None):
        super(RFaiPredctor, self).__init__()
        self.args = get_cfg(self.args, overrides)
        with open(CLASS_CFG, errors='ignore') as f:
            self.names = yaml.safe_load(f)['names']

    def encode_image(self, input_img):
        ratio = 3  # 0~9
        encode_param = [cv2.IMWRITE_PNG_COMPRESSION, ratio]
        encoded_img = base64.b64encode(cv2.imencode(".png", input_img, encode_param)[1])

        return encoded_img.decode("utf8")

    def pre_processing(self, f: Image,
                    img_size: int=640,
                    stride: int=32):
        self.img_origin = np.array(f)
        img = LetterBox(img_size, True, stride=stride)(image=self.img_origin)
        
        img = img.transpose((2, 0, 1)) # HWC to CHW, BGR to RGB
        img = np.ascontiguousarray(img)  # contiguous
        img = torch.from_numpy(img).cuda()
        img = img.float() / 255.
        self.img = img[None]
        return self.img_origin, self.img


    def get_result(self, preds, img, orig_imgs):
        preds = ops.non_max_suppression(preds,
                                        self.args.conf,
                                        self.args.iou,
                                        agnostic=self.args.agnostic_nms,
                                        max_det=self.args.max_det,
                                        classes=self.args.classes)
        results = []
        for i, pred in enumerate(preds):
            orig_img = orig_imgs[i] if isinstance(orig_imgs, list) else orig_imgs
            if not isinstance(orig_imgs, torch.Tensor):
                pred[:, :4] = ops.scale_boxes(img.shape[2:], pred[:, :4], orig_img.shape)
            results.append(Results(orig_img=orig_img, path=Path('dummy'), names=self.names, boxes=pred))
        return results
    
    def get_image(self, results, batch):
        p, im, _ = batch
        log_string = ''
        frame = getattr(self.dataset, 'frame', 0)
        log_string += '%gx%g ' % im.shape[2:]  # print string
        result = results[0]
        log_string += result.verbose()

        plot_args = dict(line_width=self.args.line_width,
                            boxes=self.args.boxes,
                            conf=self.args.show_conf,
                            labels=self.args.show_labels)
        if not self.args.retina_masks:
            plot_args['im_gpu'] = im[0]
        return result.plot(**plot_args)
    
    def post_processing(self,
                        img_origin: np.array,
                        img_tensor: torch.Tensor,
                        out: torch.Tensor):
        
        # predictor = DetectionPredictor()
        preds = self.get_result(out, img_tensor, img_origin)
        show_img = self.get_image(preds, ((Path('dummy'), img_tensor, img_origin)))
        return preds[0].boxes, cv2.cvtColor(show_img, cv2.COLOR_RGB2BGR)