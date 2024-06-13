import os,sys
import pathlib
import yaml
import pandas as pd
import pickle
from src.exception import CustomException
from src.logging import logging


def save_data(data, output_path):
    try:
        # Save the split datasets to the specified output path
        pathlib.Path(output_path).mkdir(parents=True, exist_ok=True)
        csv_file_path = os.path.join(output_path, 'data.csv')
        data.to_csv(csv_file_path , index=False)
        
        logging.info(f'Data saved at {csv_file_path}')
    except Exception as e:
        raise CustomException(e,sys)
    
def save_object(obj, file_path, file_extension='pkl'):
    try:
        file_path_with_extension = f"{file_path}.pkl"
        dir_path = os.path.dirname(file_path_with_extension)
        os.makedirs(dir_path, exist_ok=True) 
        with open(file_path_with_extension, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        
      
        logging.info(f'Object saved at {file_path_with_extension}')

    except Exception as e:
        raise CustomException(e, sys)


def read_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            obj = pickle.load(file_obj)
        
        logging.info(f'Object read from {file_path}')
        
        return obj

    except Exception as e:
        raise CustomException(e, sys)



