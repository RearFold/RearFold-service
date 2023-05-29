import cv2
import base64
import numpy as np
import torch
from bentoml.io import Image


class RFaiClassifier:
    def __init__(self, overrides=None):
        # super(RFaiClassifier, self).__init__()
        # self.args = get_cfg(self.args, overrides)
        # with open(CLASS_CFG, errors='ignore') as f:
        #     self.names = yaml.safe_load(f)['names']
        pass

    def encode_image(self, input_img):
        ratio = 3  # 0~9
        encode_param = [cv2.IMWRITE_PNG_COMPRESSION, ratio]
        encoded_img = base64.b64encode(cv2.imencode(".png", input_img, encode_param)[1])

        return encoded_img.decode("utf8")

    def pre_processing(self, f: Image, img_size: int=640):
        pass

    def get_result(self, preds, img, orig_imgs):
        pass
    
    def get_image(self, results, batch):
        pass
    
    def post_processing(self, img_origin: np.array, img_tensor: torch.Tensor, out: torch.Tensor):
        pass