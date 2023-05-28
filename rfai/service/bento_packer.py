import bentoml
from ultralytics import YOLO


def rfai_pack():
    model = YOLO("yolov8s.pt").model
    model.eval()
    saved_model = bentoml.pytorch.save_model(name='yolov8s_model',
                                            model=model,
                                            signatures={"__call__": {"batchable": False}})
    print(saved_model)

