import streamlit as st
import tensorflow as tf
import numpy as np
import cv2

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

# Sidebar UI with Project Links
with st.sidebar:
    st.markdown("<h2 style='color: #FF416C; font-weight: 800;'>🤟 Project Hub</h2>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 📌 Quick Navigation")
    st.markdown("[🔗 GitHub Repository](https://github.com/amnaibrar56-tech/asl-sign-language-classifier-amna)")
    st.markdown("[📊 Kaggle Dataset](https://www.kaggle.com/datasets/grassknoted/asl-alphabet)", unsafe_allow_html=True)
    st.markdown("[📄 Project Report](#project-report)")
    st.markdown("[🎥 Presentation & YouTube](#presentation-youtube)")
    st.markdown("---")
    st.info("💡 **Tips for Best Accuracy:**\n- Bring hand close to camera.\n- Ensure proper lighting.\n- Keep background clean.")

# Main Header
st.markdown("<h1 class='main-title'>ASL Alphabet Classifier</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Real-Time AI Sign Language Recognition Engine (MobileNetV2)</p>", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    return tf.keras.models.load_model('/content/best_asl_model.keras')

with st.spinner("⚡ Initializing Deep Learning Engine..."):
    model = load_model()

labels = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "del", "nothing", "space"]

CONFIDENCE_THRESHOLD = 0.90

# Prominent Camera Banner
st.markdown("""
    <div class="camera-banner">
        <h3>📸 POSITION YOUR HAND & CLICK "TAKE PHOTO" BELOW</h3>
    </div>
""", unsafe_allow_html=True)

# Camera Box Input
image_file = st.camera_input("Take a picture of your sign")

if image_file is not None:
    bytes_data = image_file.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    img_resized = cv2.resize(cv2_img, (224, 224)) / 255.0
    img_expanded = np.expand_dims(img_resized, axis=0)
    
    with st.spinner("🔮 Analyzing Hand Gesture..."):
        predictions = model.predict(img_expanded)
        max_score = np.max(predictions)
        predicted_label = labels[np.argmax(predictions)]
    
    st.write("---")
    
    if max_score < CONFIDENCE_THRESHOLD or predicted_label == "nothing":
        st.error("❌ **Invalid / Unrecognized Sign**\nPlease show a clear ASL hand gesture from the 29 trained classes.")
    else:
        st.markdown(f"""
            <div class="result-card">
                <h2 style="color: #FF416C; margin-top: 0; font-weight: 800;">✨ Gesture Detected Successfully</h2>
                <p style="color: #cbd5e1; margin-bottom: 0;">High precision match confirmed by deep neural network.</p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Detected Alphabet", value=predicted_label)
        with col2:
            st.metric(label="Confidence Level", value=f"{max_score * 100:.2f}%")

# ==========================================
# PROJECT DETAILS & LINKS SECTION (Required by Sir)
# ==========================================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div class="info-box">
        <h2 style="color: #FF416C; margin-top: 0; font-weight: 800;">📂 Project Documentation & Links</h2>
        <p style="color: #cbd5e1;">Here you can find all the official resources, source code, dataset references, and presentation links associated with this Deep Learning semester project.</p>
        <hr style="border-color: rgba(168, 85, 247, 0.3);">
        
        <h3 style="color: #A855F7;">1. Source Code & Repository</h3>
        <p>Access the complete source code, trained model files, and deployment scripts on GitHub:</p>
        <a href="https://github.com/amnaibrar56-tech/asl-sign-language-classifier-amna" target="_blank" style="color: #00E5FF; font-weight: bold; font-size: 1.1rem;">👉 Click here to view GitHub Repository</a>
        
        <h3 style="color: #A855F7; margin-top: 20px;">2. Dataset & Architecture Details</h3>
        <ul style="color: #cbd5e1;">
            <li><b>Official Dataset Source:</b> <a href="https://www.kaggle.com/datasets/grassknoted/asl-alphabet" target="_blank" style="color: #00E5FF;">Kaggle ASL Alphabet Dataset</a> (29 Classes: A-Z, space, del, nothing).</li>
            <li><b>Dataset Splits (Google Drive):</b> 
                <br>&nbsp;&nbsp;&nbsp;&nbsp;• <a href="https://drive.google.com/file/d/1zD66nVXa4qYGsXMnflMThFUmOfvuIE7i/view?usp=sharing" target="_blank" style="color: #00E5FF;">Training Set (asl_alphabet_train.zip)</a>
                <br>&nbsp;&nbsp;&nbsp;&nbsp;• <a href="https://drive.google.com/file/d/1qQwb4zdq-bMrVFgMBoYgvnyEUA5w1l_B/view?usp=sharing" target="_blank" style="color: #00E5FF;">Testing Set (asl_alphabet_test.zip)</a>
            </li>
            <li><b>Model Architecture:</b> MobileNetV2 (Transfer Learning with Fine-Tuning).</li>
            <li><b>Preprocessing:</b> Resized to 224x224 pixels, normalized with strict 90% confidence threshold validation.</li>
        </ul>
        
        <h3 id="project-report" style="color: #A855F7; margin-top: 20px;">3. Project Report</h3>
        <p style="color: #cbd5e1;">Comprehensive documentation outlining training metrics, validation accuracy, and architecture performance.</p>
        
        <h3 id="presentation-youtube" style="color: #A855F7; margin-top: 20px;">4. Presentation & Video Demonstration</h3>
        <p style="color: #cbd5e1;">Complete walkthrough, slide deck, and live demonstration video showcasing the real-time recognition pipeline.</p>
    </div>
""", unsafe_allow_html=True)
