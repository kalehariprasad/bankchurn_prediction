import os,sys
import pathlib
import yaml
from src.exception import CustomException
from src.logging import logging
from src.utils import save_object
from sklearn.ensemble import RandomForestClassifier,BaggingClassifier,AdaBoostClassifier

class TrainingConfig:
    curr_dir = pathlib.Path(__file__)
    home_dir = curr_dir.parent.parent.parent
    model_path = home_dir.as_posix() + '/models/model'

class modelTraining:
    def __init__(self):
        self.modelconfig =TrainingConfig()
     
    def training(self,train_x,train_y):
        try:
            logging.info('model training started')
            model=RandomForestClassifier()
            model.fit(train_x,train_y)
            logging.info(f'{model} trained on tran  data')
            save_object(model,self.modelconfig.model_path)
            logging.info(f'{model}is saved In {self.modelconfig.model_path} ')

        except Exception as e:
            raise CustomException(e,sys)

   
  


