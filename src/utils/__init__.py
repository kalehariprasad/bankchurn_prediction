import os,sys
import pathlib
import yaml
import pandas as pd
from sklearn.model_selection import train_test_split
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
