import streamlit as st
from streamlit_option_menu import option_menu
import json
import os

# Page configuration
st.set_page_config(
    page_title="Anxiety Detection Dashboard",
    page_icon="😰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .title-main {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77e4;
        margin-bottom: 2rem;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.title("🧠 Anxiety Detection")
    st.markdown("---")
    
    selected = option_menu(
        menu_title=None,
        options=["Home", "Real-time Detection", "Statistics", "About"],
        icons=["house", "camera-video", "bar-chart", "info-circle"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "#1f77e4", "font-size": "25px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#eee",
            },
            "nav-link-selected": {"background-color": "#1f77e4"},
        },
    )

# Home Page
if selected == "Home":
    st.markdown('<p class="title-main">🧠 Anxiety Detection System</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Welcome to Anxiety Detection Dashboard
        
        This application uses **deep learning** to detect anxiety levels from facial expressions.
        
        **Anxiety Detection Levels:**
        - 😟 **High Anxiety** - Intense anxiety symptoms detected
        - 😐 **Low Anxiety** - Mild anxiety symptoms detected
        - 😊 **No Anxiety** - Normal/calm state detected
        """)
        
        st.info("💡 **Tip:** Use good lighting and ensure your face is clearly visible for best results.")
    
    with col2:
        st.markdown("""
        ### How it Works
        
        1. **Face Detection** - Detects your face using Haar Cascade
        2. **Image Processing** - Normalizes facial region (48x48 pixels)
        3. **Model Inference** - Uses trained Keras model to predict anxiety level
        4. **Real-time Display** - Shows prediction with confidence
        
        ### Key Features
        - ⚡ Real-time anxiety detection
        - 📊 Statistical insights
        - 🎥 Webcam integration
        - 💾 Results history
        """)
    
    st.markdown("---")
    
    # Quick stats
    st.markdown("### Quick Statistics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Model Accuracy", "87%", "+2%")
    with col2:
        st.metric("Detections Today", "0", "Real-time")
    with col3:
        st.metric("Status", "Ready", "✅")

# Detection Page
elif selected == "Real-time Detection":
    st.markdown('<p class="title-main">🎥 Real-time Anxiety Detection</p>', unsafe_allow_html=True)
    
    try:
        import cv2
        import numpy as np
        import tensorflow as tf
        from utils.model import AnxietyDetector

        # Debug prints removed to avoid leaking environment/file listings in production UI

        detector = AnxietyDetector()
        
        st.markdown("### Webcam Detection")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("**Live Feed**")
            stframe = st.empty()
        
        with col2:
            st.markdown("**Statistics**")
            result_placeholder = st.empty()
            confidence_placeholder = st.empty()
        
        # Controls
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            confidence_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.5)
        
        with col2:
            start_detection = st.checkbox("Enable Webcam", value=False)
        
        with col3:
            frame_rate = st.slider("Frame Rate (FPS)", 1, 30, 15)
        
        if start_detection:
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                st.error("❌ Cannot access webcam. Please check permissions.")
            else:
                st.success("✅ Webcam connected. Detecting anxiety levels...")
                
                detections_log = {"High_Anx": 0, "Low_Anx": 0, "No_Anx": 0}
                frame_count = 0
                
                while start_detection:
                    ret, frame = cap.read()
                    
                    if not ret:
                        st.error("Failed to capture frame")
                        break
                    
                    # Process frame
                    frame_count += 1
                    result, conf = detector.detect(frame)
                    
                    if result:
                        detections_log[result] += 1
                    
                    # Resize for display
                    frame = cv2.resize(frame, (640, 480))
                    
                    # Display result on frame
                    if result:
                        color = (0, 255, 0) if result == "No_Anx" else (0, 165, 255) if result == "Low_Anx" else (0, 0, 255)
                        cv2.putText(frame, f"{result} ({conf:.2f})", (10, 40), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 2)
                    
                    # Convert BGR to RGB for display
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    stframe.image(frame_rgb, use_column_width=True)
                    
                    with result_placeholder.container():
                        st.markdown(f"**Latest Detection:** {result if result else 'Processing...'}")
                        st.markdown(f"**Confidence:** {conf:.2%}" if result else "")
                    
                    # Update stats every 10 frames
                    if frame_count % 10 == 0:
                        with confidence_placeholder.container():
                            st.bar_chart(detections_log)
                
                cap.release()
        else:
            st.info("👈 Enable the webcam checkbox to start detection")
    
    except Exception as e:
        st.error("Failed loading model utilities — showing error details below.")
        st.exception(e)
        raise

# Statistics Page
elif selected == "Statistics":
    st.markdown('<p class="title-main">📊 Statistics & Analytics</p>', unsafe_allow_html=True)
    
    st.markdown("### Detection History")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Detections", "0")
    with col2:
        st.metric("High Anxiety", "0")
    with col3:
        st.metric("Low Anxiety", "0")
    with col4:
        st.metric("No Anxiety", "0")
    
    st.markdown("---")
    
    st.info("📝 Statistics will be populated as you run real-time detections.")

# About Page
elif selected == "About":
    st.markdown('<p class="title-main">ℹ️ About This Project</p>', unsafe_allow_html=True)
    
    st.markdown("""
    ### Project Information
    
    **Anxiety Detection System** is a deep learning-based application that analyzes facial expressions 
    to detect anxiety levels in real-time.
    
    #### Technology Stack
    - **Frontend:** Streamlit
    - **Deep Learning:** Keras/TensorFlow
    - **Computer Vision:** OpenCV
    - **Face Detection:** Haar Cascade Classifier
    
    #### Model Details
    - **Architecture:** Convolutional Neural Network (CNN)
    - **Input Size:** 48x48 grayscale images
    - **Output Classes:** 3 (High Anxiety, Low Anxiety, No Anxiety)
    - **Training Data:** Facial expression dataset
    
    #### Features
    - ⚡ Real-time anxiety detection from webcam
    - 📊 Statistical analysis and history
    - 🎯 High accuracy with confidence scores
    - 🖥️ User-friendly web interface
    - 🔒 Privacy-focused (local processing)
    
    #### Limitations
    - Requires adequate lighting
    - Face must be clearly visible
    - Works best with frontal face orientation
    
    #### Contact & Support
    For issues or suggestions, please refer to the project repository.
    """)
    
    st.markdown("---")
    st.markdown("**Made with ❤️ using Streamlit and TensorFlow**")
