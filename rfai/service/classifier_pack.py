
import bentoml

def rfai_pack():
    model = "Your Model"
    model.eval()
    saved_model = bentoml.pytorch.save_model(name='classifier_model',
                                            model=model,
                                            signatures={"__call__": {"batchable": False}})
    print(saved_model)

