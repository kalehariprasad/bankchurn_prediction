import os,sys
import pathlib
import yaml
from src.exception import CustomException
from src.logging import logging
from src.utils import read_object
from sklearn.metrics import accuracy_score,precision_score,recall_score,confusion_matrix

class ModelPredictionConfig:
    curr_dir = pathlib.Path(__file__)
    home_dir = curr_dir.parent.parent.parent
    model= home_dir.as_posix() + '/models/model.pkl'

class Predict:
    def __init__(self) :
        self.predictconfig=ModelPredictionConfig()
    def predict(self,test_x,test_y):
        try:

            model=read_object(self.predictconfig.model)
            logging.info('model prediction stated')
            pred=model.predict(test_x)
            accuracy=accuracy_score(pred,test_y)
            precision=precision_score(pred,test_y)
            recall=recall_score(pred,test_y)
            confusion_mtrtic=confusion_matrix(pred,test_y)
        
            metrics_dict={
                'accuracy':accuracy,
                'precision':precision,
                'recall':recall,
                'confusion_mtrtic':confusion_mtrtic
                } 
            logging.info(f'prediction compleeted and the metrics are {metrics_dict}')
            return metrics_dict
        except Exception as  e:
            raise CustomException(e,sys)

       
