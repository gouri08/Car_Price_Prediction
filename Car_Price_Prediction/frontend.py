import streamlit as st
import pickle
import numpy as np
import pandas as pd
st.set_page_config(page_title='Car_Price_predictor')
st.header('Welcome to Car Price predictor appliaction!!!')
st.header('Please enter your details to continue...')
df=pd.read_csv('copied.csv')
objects={}
for i in df.columns:
    if df[i].dtype==object:
        objects[i]=list(df[i].unique())
        objects[i].sort()
with open('model2.pkl','rb') as file:
    model=pickle.load(file)
with st.container(border=True):
    col1, col2 = st.columns(2)
    # get all columns that start with 'Make_'
    make_columns = [col for col in df.columns if col.startswith('Make_')]
    make_options = [col.replace('Make_', '') for col in make_columns]
    Make = st.selectbox('CarBrand:', options=make_options)

    Model_columns=[col1 for col1 in df.columns if col1.startswith('Model_')]
    Model_options=[col1.replace('Model_','') for col1 in Model_columns]
    Model=st.selectbox('Car Model:',options=Model_options)

    Year=st.number_input('Car Manufacture Year:',min_value=2000,max_value=2025)

    EngineSize=st.number_input('Engine Size:',min_value=1,max_value=4)

    Mileage=st.number_input('Mileage',min_value=55,max_value=199867)

    Fuel_columns = [col2 for col2 in df.columns if col2.startswith('Fuel Type_')]
    Fuel_options = [col.replace('Fuel Type_', '') for col in Fuel_columns]
    FuelType= st.selectbox('Fuel Type:', options=Fuel_options)

    Transmission_columns = [col3 for col3 in df.columns if col3.startswith('Transmission_')]
    Transmission_options = [col.replace('Transmission_', '') for col in Transmission_columns]
    TransmissionType= st.selectbox('Fuel Type:', options=Transmission_options)

    c1, c2, c3 = st.columns([1.2, 1, 1])

    if c2.button("Predict Price"):

        input_data = {col: 0 for col in df.columns if col != 'Price'}


        input_data['Year'] = Year
        input_data['Engine Size'] = EngineSize
        input_data['Mileage'] = Mileage

        input_data[f"Make_{Make}"] = 1
        input_data[f"Model_{Model}"] = 1
        input_data[f"Fuel Type_{FuelType}"] = 1
        input_data[f"Transmission_{TransmissionType}"] = 1

        input_df = pd.DataFrame([input_data])
        input_df = input_df[df.drop(columns=['Price']).columns]  # Match training column order

        out = model.predict(input_df)[0]
        st.subheader(f"💰 Predicted Car Price: ₹ {out:,.2f}")

