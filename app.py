import pandas as pd
import numpy as np
import pickle
import pathlib
import streamlit as st


curr_dir = pathlib.Path(__file__)
home_dir = curr_dir.parent.parent.parent


model_path = home_dir.as_posix() + 'models/model.pkl'
preprocer=home_dir.as_posix() + 'models\preprocessor.pkl'

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
    # Create a dictionary with the collected data
    data_dict = {
        'Geography': [Geography],
        'Gender': [Gender],
        'Age': [Age],
        'Tenure': [Tenure],
        'Balance': [Balance],
        'NumOfProducts': [NumOfProducts],
        'HasCrCard': [HasCrCard],
        'IsActiveMember': [IsActiveMember],
        'EstimatedSalary': [EstimatedSalary],
        'Credit_group': [Credit_group]
    }

    # Convert the dictionary into a DataFrame with an explicit index
    input_data = pd.DataFrame(data_dict)
    input=pre_obj.transform(input_data)


    # Perform prediction using your model (assuming model.predict is correct)
    result = model.predict(input)
    if result==0:
        st.header('Person will not Churn')
    else:
        st.header('person Will churn')







 

