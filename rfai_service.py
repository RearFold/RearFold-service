import bentoml
from bentoml.io import Image, JSON

from rfai.detect import RFaiPredctor
from rfai.config import RFAI_CFG

# 먼저 pack을 해야함. 모델을 그런 다음 그 모델이 bento list로 보면 있는데 그 모델을 가져와서 runner로 만들고 시작하는거임!
yolov8s_runner = bentoml.pytorch.get("yolov8s_model:latest").to_runner()
svc = bentoml.Service("yolov8s_svc", runners=[yolov8s_runner])

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