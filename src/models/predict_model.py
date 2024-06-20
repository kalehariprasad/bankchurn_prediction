import os,sys
import pathlib
import yaml
import pandas as pd
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


class customdata:
    def __init__(self, Geography, Gender, Age, Tenure, Balance, HasCrCard, IsActiveMember, EstimatedSalary, Credit_group):
        self.Geography = Geography
        self.Gender = Gender
        self.Age = Age
        self.Tenure = Tenure
        self.Balance = Balance
        self.HasCrCard = HasCrCard
        self.IsActiveMember = IsActiveMember
        self.EstimatedSalary = EstimatedSalary
        self.Credit_group = Credit_group

    def get_dataframe(self):
        try:
            data_dict = {
                'Geography': [self.Geography],
                'Gender': [self.Gender],
                'Age': [self.Age],
                'Tenure': [self.Tenure],
                'Balance': [self.Balance],
                'HasCrCard': [self.HasCrCard],
                'IsActiveMember': [self.IsActiveMember],
                'EstimatedSalary': [self.EstimatedSalary],
                'Credit group': [self.Credit_group],
            }

            # Create DataFrame from data_dict
            df = pd.DataFrame(data_dict)

            # Define column mapping (correcting the typo in HasCrCard)
            column_mapping = {
                'Geography': 'Geography',
                'Gender': 'Gender',
                'Age': 'Age',
                'Tenure': 'Tenure',
                'Balance': 'Balance',
                'HasCrCard': 'HasCrCard',
                'IsActiveMember': 'IsActiveMember',
                'EstimatedSalary': 'EstimatedSalary',
                'Credit group': 'Credit group'
            }

            print("Keys in df:", df.columns)
            print("Keys in column_mapping:", column_mapping.keys())

            # Validate data types
            expected_data_types = {
                'Geography': str,
                'Gender': str,
                'Age': int,
                'Tenure': int,
                'Balance': float,
                'HasCrCard': str,  # Adjusted to string type
                'IsActiveMember': str,  
                'EstimatedSalary': float,
                'Credit group': str
            }

            
            for col, expected_type in expected_data_types.items():
                actual_type = df[col].dtype
                if actual_type != expected_type:
                    raise TypeError(f"Column '{col}' has incorrect data type '{actual_type}', expected '{expected_type}'.")

      
            mapped_data = {column_mapping[col]: df[col] for col in df.columns}

            return mapped_data

        except Exception as e:
            raise CustomException(e, sys)




       
