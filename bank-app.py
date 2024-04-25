# import the streamlit library
import streamlit as st
import numpy as np
import pickle

loaded_model = pickle.load(open('model/bank-learn.pkl', 'rb'))

country_to_number = {
    'Kenya': 0,
    'Rwanda': 1,
    'Tanzania': 2,
    'Uganda': 3
}

job_to_number = {
    'Self employed': 9, 
    'Government Dependent': 4,
    'Formally employed Private': 3, 
    'Informally employed': 5,
    'Formally employed Government': 2, 
    'Farming and Fishing': 1,
    'Remittance Dependent': 8, 
    'Other Income': 7,
    'No Income': 6,
    'Dont Know/Refuse to answer': 0
}

maritalStatus_to_number = {
    'Married/Living together': 2, 
    'Widowed': 4, 
    'Single/Never Married': 3,
    'Divorced/Seperated': 0, 
    'Dont know': 1
}

access_to_number = {'Yes': 1, 'No': 0}

location_to_number = {'Urban': 1, 'Rural': 0}

gender_to_number = {'Male': 1, 'Female': 2}

account_access = 'This user is most likely to have or use a bank account.'

def account_prediction(input_data):
    # changing the input_data to numpy array
    input_data_as_numpy_array = np.asarray(input_data)
    
    # reshape the array as we are predicting for one instance
    input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)
    
    prediction = loaded_model.predict(input_data_reshaped)
    if (prediction[0] == 0):
        return 'This user would not have or use a bank account.'
    else:
        return account_access

# give a title to our app
st.title('Welcome to Financial Inclusion App')

country = st.selectbox("Country: ", ['Select an option'] + list(country_to_number.keys()) )

maritalStatus = st.selectbox('Relationship Status: ', ['Select an option'] + list(maritalStatus_to_number.keys()))

jobType = st.selectbox('Employment: ', ['Select an option'] + list(job_to_number.keys()))

age_of_personnel = st.number_input("Age:", min_value=0, step=1, format='%d', value=0)

phone_access = st.radio("Access to cellphones? ", ('Yes', 'No'), index=None)

status = st.radio("Select Gender: ", ('Male', 'Female'), index=None)

location = st.radio("Select Area: ", ('Rural', 'Urban'), index=None)

if(st.button('Predict Account Holder')):
    
    # Map the selected option to its corresponding number
    country_number = country_to_number.get(country, '')
    job_number = job_to_number.get(jobType, '')
    marital_number = maritalStatus_to_number.get(maritalStatus, '')
    access_number = access_to_number.get(phone_access)
    location_number = location_to_number.get(location)
    gender_number = gender_to_number.get(status)

    try:
        if age_of_personnel == 0:
            raise ValueError('to input a value')
        result = account_prediction([location_number, access_number, age_of_personnel, gender_number, job_number, country_number, marital_number ])
        if result == account_access:
            st.success(result)
        else:
            st.error(result)
    except ValueError:
        st.error('Please complete the form for predictions.')