import bentoml
from bentoml.io import Image, JSON
from bentoml import Service

yolov8s_runner = bentoml.pytorch.get("yolov8s_model:latest").to_runner()
svc = bentoml.Service("yolov8s_svc", runners=[yolov8s_runner])

from rfai.detect import RFaiPredctor
from rfai.config import RFAI_CFG


@svc.api(input=Image(), output=JSON())
async def predict(f: Image):
    predictor = RFaiPredctor(overrides=RFAI_CFG)
    img_origin, img_tensor = predictor.pre_processing(f=f)

    out = yolov8s_runner.run(img_tensor)
    out_bbox_info, out_img = predictor.post_processing(img_origin=img_origin,
                                             img_tensor=img_tensor,
                                             out=out)
    enc_out_img = predictor.encode_image(out_img) 

    cls = out_bbox_info.cls.detach().cpu().numpy()
    conf = out_bbox_info.conf.detach().cpu().numpy()
    coord = out_bbox_info.data[:,:4].detach().cpu().numpy()

    res = {'enc_out_img': enc_out_img, 'cls': cls, 'conf': conf, 'coord': coord}
    return res