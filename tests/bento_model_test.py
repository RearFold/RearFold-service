import bentoml
bento_model: bentoml.Model = bentoml.pytorch.get("yolov8s_model:latest")


print(bento_model.path)
print(bento_model.info.metadata)
print(bento_model.info.labels)