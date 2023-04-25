import pandas as pd
import numpy as np
from pycaret.regression import *
import streamlit as st

model = load_model('loan_approval_v1')

def predict(model, input_df):
    input_df.to_csv("teste.csv",index=False)
    predictions_df = predict_model(estimator=model, data=input_df)
    predictions_df.to_csv("pred.csv",index=False)
    predictions = predictions_df['prediction_label'][0]
    return predictions

def run():

    from PIL import Image
    #image = Image.open('logo.png')
    image_loan = Image.open('loan.jpg')

    #st.image(image,use_column_width=False)

    add_selectbox = st.sidebar.selectbox(
    "How would you like to predict?",
    ("Online", "Batch"))

    st.sidebar.info('Will you get a loan? Try your luck here!')
    #st.sidebar.success('https://www.pycaret.org')
    
    st.sidebar.image(image_loan)

    st.title("Loan Approval app")

    if add_selectbox == 'Online':


        sex = st.selectbox('Gender', ['male', 'female'])
        married = st.selectbox('Married', ['Yes', 'No'])
        dep = st.selectbox('Dependents', [0,1,2,3,4,5,6,7,8,9,10])
        ed = st.selectbox('Education', ['Graduate', 'Not Graduate'])
        emp = st.selectbox('Self_Employed', ['Yes', 'No'])
        inc = st.number_input('ApplicantIncome', min_value=0, max_value=5000, value=2000)
        coinc = st.number_input('CoapplicantIncome', min_value=0, max_value=5000, value=0)
        loan = st.number_input('LoanAmount', min_value=0, max_value=1000, value=0)
        loant = st.number_input('Loan_Amount_Term', min_value=0, max_value=360, value=0)
        credit = st.number_input('Credit_History', min_value=0, max_value=1, value=0)
        prop = st.selectbox('Property_Area', ['Urban', 'Rural'])
        
        #if st.checkbox('Smoker'):
        #    smoker = 'yes'
        #else:
        #    smoker = 'no'
        
        output=""

        input_dict = {'Gender' : sex, 'Married' : married, 'Dependents' : dep, 
                      'Education' : ed,
                      'Self_Employed' : emp,
                      'ApplicantIncome' : inc,'CoapplicantIncome' : coinc,'LoanAmount' : loan,'Loan_Amount_Term' : loant,
                      'Credit_History' : credit,'Property_Area' : prop}
        input_df = pd.DataFrame([input_dict])

        if st.button("Predict"):
            output = predict(model=model, input_df=input_df)
            output = '$' + str(output)

        st.success('The output is {}'.format(output))

    if add_selectbox == 'Batch':

        file_upload = st.file_uploader("Upload csv file for predictions", type=["csv"])

        if file_upload is not None:
            data = pd.read_csv(file_upload)
            predictions = predict_model(estimator=model,data=data)
            st.write(predictions)

if __name__ == '__main__':
    run()