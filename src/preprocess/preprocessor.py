import os,sys
import pathlib
import yaml
import pandas as pd
import numpy as np
from sklearn.preprocessing import  OneHotEncoder,OrdinalEncoder,StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as imbpipe
from src.exception import CustomException
from src.logging import logging
from src.utils import save_data,save_object
from dvclive import Live
from src.models.train_model import modelTraining
from src.models.predict_model import Predict


class PreprocessrConfig:
    curr_dir = pathlib.Path(__file__)
    home_dir = curr_dir.parent.parent.parent
    train_data_path = home_dir.as_posix() + '/data/interim/train/data.csv'
    test_data_path = home_dir.as_posix() + '/data/interim/test/data.csv'
    output_train_path = home_dir.as_posix() + '/data/processed/train'
    output_test_path = home_dir.as_posix() + '/data/processed/test'
    preprocessor_object=home_dir.as_posix() + '/models/preprocessor'
class Preprocessing:
    def __init__(self):
        self.PreprocessingConfig = PreprocessrConfig()
    
    def preprocess(self):
        try:

  
            categorical_cols = ['Geography', 'Gender']
            numerical_cols = ['Age', 'Tenure', 'Balance', 'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'EstimatedSalary']
            ordinal_cols = ['Credit_group']
            logging.info('pipeline creation started')
            categorical_transformer = Pipeline(steps=[
                ('onehot', OneHotEncoder(handle_unknown='ignore'))
            ])

            numerical_transformer = Pipeline(steps=[
                ('scaler', StandardScaler())
            ])

            ordinal_transformer = Pipeline(steps=[
                ('ordinal', OrdinalEncoder(categories=[['Poor', 'Fair', 'Good', 'Very_Good', 'Exceptional']]))
            ])
            logging.info('combinig onehot, scaler,ordinal pipelines as single preprocessor started')
            preprocessor = ColumnTransformer(
            transformers=[
                ('cat', categorical_transformer, categorical_cols),
                ('num', numerical_transformer, numerical_cols),
                ('ord', ordinal_transformer, ordinal_cols)
            ])
            pipeline = Pipeline(steps=[('preprocessor', preprocessor)])
            logging.info('combinig onehot, scaler,ordinal pipelines as single preprocessor is compleeted')

            return pipeline

        except Exception as e:
            raise CustomException(e, sys)
    def initiate_preprocess(self,train_data,test_data):
        try:
            logging.info('preprocess step intiated')
            preprocesser = self.preprocess()
            
            # Exclude the target variable 'Exited' from features
            logging.info('train_x,test_x,test_x,test_y splitting started')
            train_X = train_data.drop(columns=['Exited'])
            train_y = train_data['Exited']
            test_X = test_data.drop(columns=['Exited'])
            test_y = test_data['Exited']

            transformed_train_X = preprocesser.fit_transform(train_X)

            save_object(preprocesser,self.PreprocessingConfig.preprocessor_object)
            logging.info(f'preprocessing compleeted and stored pickle file in :{self.PreprocessingConfig.preprocessor_object}')
            print('transformed_train_X_shape is : ', transformed_train_X.shape)
            print('train_y shape is ',train_y.shape)
            
            transformed_test_X = preprocesser.transform(test_X)
      
            resampler = SMOTE()
            transformed_train_X_resampled, train_y_resampled = resampler.fit_resample(transformed_train_X, train_y)
          
            print('transformed_train_X_resampled_shape is :', transformed_train_X_resampled.shape)
            print('train_y_resampled shape is :' ,train_y_resampled.shape)

            # Convert arrays to DataFrames
            logging.info('started converting transformed arrays to dataframes')
            X_column_names=['Geography_France', 'Geography_Germany', 'Geography_Spain', 'Gender_Female', 'Gender_Male', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'EstimatedSalary', 'Credit_group']
            df_train_resampled = pd.DataFrame(transformed_train_X_resampled, columns=X_column_names)  # replace 'feature1', 'feature2', ... with actual feature names
            df_train_resampled['Exited'] = train_y_resampled  
            df_test = pd.DataFrame(transformed_test_X, columns=X_column_names)  # replace 'feature1', 'feature2', ... with actual feature names
            df_test['Exited'] = test_y  
            logging.info('compleetd converting transformed arrays to dataframes')

            save_data(df_train_resampled,self.PreprocessingConfig.output_train_path)
            save_data(df_test,self.PreprocessingConfig.output_test_path)
            logging.info(f'transformed train data is stored at:{self.PreprocessingConfig.output_train_path}')
            logging.info(f'transformed test data is stored at:{self.PreprocessingConfig.output_test_path}')
       

            logging.info('prepcossing compleeted and rweturned transformed_train_X_resampled, train_y_resampled, transformed_test_X, test_y')
            return (transformed_train_X_resampled, train_y_resampled, transformed_test_X, test_y)
        
        except Exception as e:
            raise CustomException(e, sys)





if __name__ == "__main__":
    pre= Preprocessing()
    train_data = pd.read_csv(pre.PreprocessingConfig.train_data_path)
    test_data = pd.read_csv(pre.PreprocessingConfig.test_data_path)
    transformed_train_X_resampled, train_y_resampled, transformed_test_X, test_y=pre.initiate_preprocess(train_data,test_data)
    model=modelTraining()
    prediction=Predict()
    model.training( transformed_train_X_resampled, train_y_resampled)
    prediction.predict(transformed_test_X, test_y)

 
