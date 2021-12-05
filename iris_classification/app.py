### Script for CS329s ML Deployment Lec 
import os
import requests
import streamlit as st
from src.train import Classifier
import math
import numpy as np
from utils import predict_json

def predict_class_local(sepl, sepw, petl, petw):
    dt = list(map(float,[sepl, sepw, petl, petw]))

    req = {
        "data": [
            dt
        ]
    }

    cls = Classifier()
    return cls.load_and_test(req)

def predict_class_aws(sepl, sepw, petl, petw):
    API_URL = "https://ti53furxkb.execute-api.us-east-1.amazonaws.com/test/classify"

    dt = list(map(float,[sepl, sepw, petl, petw]))

    req = {
        "data": [
            dt
        ]
    }

    r = requests.post(API_URL, json=req)
    return r.json()

def predict_class_gcp(sepl, sepw, petl, petw):
    # Setup environment credentials (you'll need to change these)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "shreyansh-dl-playground-c06e2b7e31f3.json" # change for your GCP key
    PROJECT = "shreyansh-dl-playground" # change for your GCP project
    REGION = "us-central1" # change for your GCP region (where your model is hosted)
    MODEL = "iris_classifier"

    dt = [list(map(float,[sepl, sepw, petl, petw]))]
    
    iris_types = {
                0: 'setosa',
                1: 'versicolor',
                2: 'virginica'
            }

    preds = predict_json(project=PROJECT,
                         region=REGION,
                         model=MODEL,
                         instances=dt)

    return iris_types[preds[0]]

### Streamlit code (works as a straigtht-forward script) ###
st.title("Welcome to Iris Classifier")
st.header("Classify Iris type based on dimensions of the flower")

sepl = st.slider('Sepal Length (in cm)', 4.0, 8.0, 4.0)
sepw = st.slider('Sepal Width (in cm)', 2.0, 5.0, 2.0)
petl = st.slider('Petal Length (in cm)', 1.0, 7.0, 1.0)
petw = st.slider('Petal Width (in cm)', 0.1, 2.8, 0.1)

left, center, right = st.beta_columns(3)
with left:
    if st.button("Predict Local"):
        ret = predict_class_local(sepl, sepw, petl, petw)
        conf_list = np.array(ret['log_proba'][0])
        conf = math.exp(conf_list.max())*100

        st.write(f"Prediction: {ret['prediction'][0]}")
        st.write(f"Confidence: {conf:.2f}%")

with center:
    if st.button("Predict AWS"):
        ret = predict_class_aws(sepl, sepw, petl, petw)
        conf_list = np.array(ret['log_proba'][0])
        conf = math.exp(conf_list.max())*100

        st.write(f"Prediction: {ret['prediction'][0]}")
        st.write(f"Confidence: {conf:.2f}%")

with right:
    if st.button("Predict GCP"):
        ret = predict_class_gcp(sepl, sepw, petl, petw)

        st.write(f"Prediction: {ret}")

