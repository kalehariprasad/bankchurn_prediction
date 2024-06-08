import os,sys
import pathlib
import yaml
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from src.exception import CustomException
from src.logging import logging
from src.utils import save_data
from dvclive import Live

class FeaturebuildingConfig:
    curr_dir = pathlib.Path(__file__)
    home_dir = curr_dir.parent.parent.parent
    train_data_path = home_dir.as_posix() + '/data/external/train.csv/data.csv'
    test_data_path = home_dir.as_posix() + '/data/external/test.csv/data.csv'
    output_train_path = home_dir.as_posix() + '/data/interim/train'
    output_test_path = home_dir.as_posix() + '/data/interim/test'

class featurebuilding:
    def __init__(self) :
        self.featureengineeringconfig=FeaturebuildingConfig()

    def datatype_change(self, df):
        try:

            logging.info('data type change in progress')
            print(df.head())
            df=df.dropna()
            df["Age"] = df["Age"].astype(np.int64)
            df["CreditScore"] = df["CreditScore"].astype(np.float64)
            df["HasCrCard"] = df["HasCrCard"].astype(np.int64)
            df["IsActiveMember"] = df["IsActiveMember"].astype(np.int64)
            logging.info('data types changed for age,Creditscore,HasCrcard,IsActiveMember columns')
            return df
        except Exception as e:
            raise CustomException(e, sys)
    


    def binning(self,df): 
        try:
            logging.info('binning started for Credit Score column')
            creditscore_bins = [0, 580, 670,740,800,851]
            creditscore_labels = ['Poor', 'Fair', 'Good' , 'Very_Good' , 'Exceptional']
            df['Credit_group'] = pd.cut(df['CreditScore'], bins=creditscore_bins, labels=creditscore_labels, right=False)
            df.drop('CreditScore',inplace=True,axis=1)
            logging.info('binning compleeted and dropped crediscore column')
            return df
        except Exception as e:
            raise CustomException(e, sys)
    
    def bulding_features(self, df):
        try:   
            logging.info('started applying datatype change and binning both on a data frame')  
            df_type_change = self.datatype_change(df)
            data = self.binning(df)  # Apply binning after datatype change
            logging.info('compleeted applying datatype change and binning both on a data frame') 
            return data
        except Exception as e:
            raise CustomException(e, sys)
                




#data=pd.read_csv('C:\\Users\\Hariprasad\\Documents\\bankchurn_prediction\\data\\external\\train.csv\\data.csv')

if __name__ == "__main__":
    fe=featurebuilding()
    train_data=pd.read_csv(fe.featureengineeringconfig.train_data_path)
    test_data =pd.read_csv(fe.featureengineeringconfig.test_data_path)
    features_train=fe.bulding_features(df=train_data)
    print(features_train.columns)
    featues_test=fe.bulding_features(df=test_data)
    print(featues_test.columns)
    save_data(features_train,fe.featureengineeringconfig.output_train_path)
    save_data(featues_test,fe.featureengineeringconfig.output_test_path)

    logging.info('data validation compleeted')