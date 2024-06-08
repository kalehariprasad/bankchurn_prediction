
# -*- coding: utf-8 -*-

import os,sys
import pathlib
import yaml
import pandas as pd
from sklearn.model_selection import train_test_split
from src.exception import CustomException
from src.logging import logging
from src.utils import save_data
from dvclive import Live

class DataInjectionConfig:
    curr_dir = pathlib.Path(__file__)
    home_dir = curr_dir.parent.parent.parent
    params_file = home_dir.as_posix() + '/params.yaml'
    params = yaml.safe_load(open(params_file))["make_dataset"]

    data_path = home_dir.as_posix() + '/data/raw/Churn_Modelling.csv'
    output_train_path = home_dir.as_posix() + '/data/external/train.csv'
    output_test_path = home_dir.as_posix() + '/data/external/test.csv'
    

class DataInjection:
    def __init__(self):
        self.datainjectionconfig = DataInjectionConfig()
  
    def load_data(self, data_path):
        try:
            # Load your dataset from a given path
            df = pd.read_csv(data_path)
            logging.info('data is readed from data/raw')
            return df
        except Exception as e:
            raise CustomException(e, sys)
    
    def split_data(self, df, test_split, seed):
        try:
            with Live(save_dvc_exp=True) as live:

               
                # Split the dataset into train and test sets
                train, test = train_test_split(df, test_size=test_split, random_state=seed)
                logging.info(" data splitted into train and test data frames")
                live.log_param("data test size is :",test_split)
                live.log_param("train_test_split random_state :",seed)
                return train, test
        except Exception as e:
            raise CustomException(e,sys)


if __name__ == "__main__":
    data_injection = DataInjection()
    data = data_injection.load_data(data_injection.datainjectionconfig.data_path)
    train_data, test_data = data_injection.split_data(data, data_injection.datainjectionconfig.params['test_split'], data_injection.datainjectionconfig.params['seed'])
    save_data(train_data, data_injection.datainjectionconfig.output_train_path)
    save_data(test_data, data_injection.datainjectionconfig.output_test_path)
