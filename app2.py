import pandas as pd
import numpy as np
import pickle
import pathlib
import streamlit as st
from src.models.predict_model import customdata





model_path = 'models/model.pkl'
preprocer='data\objects\preprocessor.pkl'

# Load the pickled model
with open(model_path, 'rb') as f:
    model = pickle.load(f)
st.title('BankChurn Prediction')

with open(preprocer,'rb')as f:
    pre_obj=pickle.load(f)

Geography=st.selectbox('geography',['France','Germany','Spain'])
Gender=st.selectbox('Gender',['Male','Female'])
Age=st.number_input('Enter your age')
Tenure=st.number_input('Tenure')
Balance=st.number_input('Balance')
NumOfProducts=st.number_input('no of products')
HasCrCard=st.number_input('do you have card')
IsActiveMember=st.number_input('IsActiveMember')
EstimatedSalary=st.number_input('EstimatedSalary')
Credit_group=st.selectbox('credit group',['Fair','Very_Good','Poor','Good','Exceptional'])

# Check if predict button is clicked (assuming predict_button is a boolean variable)
if st.button('Predict'):
    data_instance = customdata(Geography, Gender, Age, Tenure, Balance, HasCrCard, IsActiveMember, EstimatedSalary, Credit_group)

    df = data_instance.get_dataframe()
    input=pre_obj.transform(df)


    # Perform prediction using your model (assuming model.predict is correct)
    result = model.predict(input)
    if result==0:
        st.header('Person will not Churn')
    else:
        st.header('person Will churn')







 

