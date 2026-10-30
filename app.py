import streamlit as st
import tensorflow as tf
import numpy as np
import cv2
import os
import gdown

# Page Configuration
st.set_page_config(
    page_title="ASL AI Classifier - Project Showcase",
    page_icon="🤟",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Ultra-Vibrant High-Tech Styling with Complete Project Links Integration
st.markdown("""
    <style>
    /* Dark Premium Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #0b0f19 0%, #17102e 50%, #0f172a 100%);
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0f0b1e;
        border-right: 1px solid rgba(168, 85, 247, 0.2);
    }
    
    /* Main Title Glowing Gradient */
    .main-title {
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(90deg, #FF416C, #FF4B2B, #A855F7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.2rem;
        text-shadow: 0 0 20px rgba(255, 65, 108, 0.3);
    }
    
    .sub-title {
        text-align: center;
        color: #cbd5e1;
        font-size: 1.1rem;
        font-weight: 500;
        margin-bottom: 1.8rem;
    }

    /* Prominent Camera Header Banner */
    .camera-banner {
        background: linear-gradient(90deg, rgba(255, 65, 108, 0.25), rgba(168, 85, 247, 0.25));
        border: 2px solid #FF416C;
        border-radius: 14px;
        padding: 12px 20px;
        text-align: center;
        margin-bottom: 15px;
        box-shadow: 0 0 25px rgba(255, 65, 108, 0.5);
    }
    
    .camera-banner h3 {
        color: #FF416C !important;
        margin: 0 !important;
        font-weight: 800;
        letter-spacing: 0.5px;
    }

    /* Glassmorphism Card for Results */
    .result-card {
        background: rgba(30, 27, 75, 0.6);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 65, 108, 0.4);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 10px 30px rgba(255, 65, 108, 0.15);
        margin-top: 15px;
        margin-bottom: 20px;
        text-align: center;
    }

    /* Project Info Section Box */
    .info-box {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(168, 85, 247, 0.3);
        border-radius: 16px;
        padding: 20px;
        margin-top: 30px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
    }

    /* Streamlit Metrics Styling */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        color: #FF416C !important;
        font-weight: 800;
        text-shadow: 0 0 10px rgba(255, 65, 108, 0.4);
    }
    
    [data-testid="stMetricLabel"] {
        color: #e2e8f0 !important;
        font-size: 1rem !important;
        font-weight: 600;
    }

    /* Camera Container Wrapper Box */
    div[data-testid="stCameraInput"] {
        border: 3px solid #FF416C;
        border-radius: 18px;
        padding: 10px;
        background: rgba(15, 11, 30, 0.7);
        box-shadow: 0 0 25px rgba(255, 65, 108, 0.5);
    }

    /* Glowing Capture Button */
    div[data-testid="stCameraInput"] button {
        background: linear-gradient(90deg, #FF416C 0%, #FF4B2B 100%) !important;
        color: #ffffff !important;
        font-size: 1.1rem !important;
        font-weight: 800 !important;
        border: 2px solid #ffffff !important;
        border-radius: 12px !important;
        padding: 12px 30px !important;
        box-shadow: 0 0 20px rgba(255, 65, 108, 0.8) !important;
        transition: all 0.3s ease-in-out !important;
    }

    div[data-testid="stCameraInput"] button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 0 30px rgba(255, 75, 43, 1) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar UI without separate YouTube link
with st.sidebar:
    st.markdown("<h2 style='color: #FF416C; font-weight: 800;'>Project Hub</h2>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### Quick Navigation")
    st.markdown("[GitHub Repository](https://github.com/amnaibrar56-tech/asl-sign-language-classifier-amna)")
    st.markdown("[Kaggle Dataset](https://www.kaggle.com/datasets/grassknoted/asl-alphabet)", unsafe_allow_html=True)
    st.markdown("[Project Report](#project-report)")
    st.markdown("[Presentation & YouTube](#presentation-youtube)")
    st.markdown("---")
    st.info("**Tips for Best Accuracy:**\n- Bring hand close to camera.\n- Ensure proper lighting.\n- Keep background clean.")

# Main Header
st.markdown("<h1 class='main-title'>ASL Alphabet Classifier</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Real-Time AI Sign Language Recognition Engine (MobileNetV2)</p>", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    model_path = 'best_asl_model.keras'
    if not os.path.exists(model_path):
        file_id = '1rlXbsUw7wxDjrE1sARPLE2tdF4UaKkr2' 
        url = f'https://drive.google.com/uc?id={file_id}'
        gdown.download(url, model_path, quiet=False)
    return tf.keras.models.load_model(model_path)

with st.spinner("Initializing Deep Learning Engine & Downloading Model..."):
    model = load_model()

labels = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "del", "nothing", "space"]

CONFIDENCE_THRESHOLD = 0.90

# Prominent Camera Banner
st.markdown("""
    <div class="camera-banner">
        <h3>POSITION YOUR HAND & CLICK "TAKE PHOTO" BELOW</h3>
    </div>
""", unsafe_allow_html=True)

# Camera Box Input
image_file
