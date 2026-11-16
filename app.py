import streamlit as st
import tensorflow as tf
import numpy as np
import cv2
import os
import requests

# (Baqi sara code waisa hi rahay ga, bas load_model function ko yeh kar lein:)

@st.cache_resource
def load_model():
    model_path = 'best_asl_model.keras'
    if not os.path.exists(model_path):
        url = 'https://github.com/amnaibrar56-tech/asl-sign-language-classifier-amna/releases/download/v1.0/best_asl_model.keras'
        with st.spinner("Downloading model from GitHub Releases (Please wait)..."):
            response = requests.get(url, allow_redirects=True)
            with open(model_path, 'wb') as f:
                f.write(response.content)
    return tf.keras.models.load_model(model_path, compile=False)
