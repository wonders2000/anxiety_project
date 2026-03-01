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
        
        st.markdown("### 📱 Camera Setup")
        
        # Camera mode selection
        camera_mode = st.radio(
            "Select camera mode:",
            ["🎥 Browser Camera (Recommended)", "💻 Windows/Desktop Camera", "📸 Single Capture"],
            horizontal=True
        )
        
        # Initialize session state for continuous capture
        if 'detections_log' not in st.session_state:
            st.session_state.detections_log = {"High_Anx": 0, "Low_Anx": 0, "No_Anx": 0}
        if 'frame_count' not in st.session_state:
            st.session_state.frame_count = 0
        
        # Display layout
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
        col1, col2 = st.columns(2)
        
        with col1:
            confidence_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.5)
        
        with col2:
            frame_rate = st.slider("Frame Rate (FPS)", 1, 30, 15)
        
        with col3:
            capture_interval = st.slider("Capture Interval (ms)", 50, 500, 100)
        
        # Permission notice
        st.markdown("---")
        st.info("📋 **Camera Access Required:** Please allow camera access when prompted by your browser or device.")
        
        # BROWSER CAMERA MODE - Works on Windows, Mac, Linux, iOS, Android
        if camera_mode == "🎥 Browser Camera (Recommended)":
            st.markdown("### Browser Camera Mode")
            st.markdown("✅ Works on **Windows, Mac, Linux, iPhone, Android**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                capture_mode = st.radio(
                    "Capture Mode:",
                    ["📸 Single Frames", "🔄 Continuous (Auto)"],
                    key="browser_mode"
                )
            
            with col2:
                if capture_mode == "🔄 Continuous (Auto)":
                    auto_refresh = st.checkbox("Auto-refresh every capture", value=True)
            
            if capture_mode == "📸 Single Frames":
                st.markdown("Click 'Take Photo' to capture and analyze a single frame.")
                img_file = st.camera_input("📷 Camera Input", key="single_capture")
                
                if img_file is not None:
                    file_bytes = np.asarray(bytearray(img_file.getvalue()), dtype=np.uint8)
                    frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

                    # Process frame
                    st.session_state.frame_count += 1
                    result, conf = detector.detect(frame)
                    if result:
                        st.session_state.detections_log[result] += 1

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
                        st.markdown(f"**Result:** {result if result else 'Processing...'}")
                        if result:
                            confidence_color = "🟢" if result == "No_Anx" else "🟡" if result == "Low_Anx" else "🔴"
                            st.markdown(f"{confidence_color} **Confidence:** {conf:.2%}")

                    with confidence_placeholder.container():
                        st.bar_chart(st.session_state.detections_log)
            
            else:  # Continuous mode
                st.markdown("📹 **Continuous Capture Mode** - Takes photos automatically")
                col1, col2 = st.columns(2)
                
                with col1:
                    enable_continuous = st.checkbox("Enable Continuous Capture", value=False, key="enable_continuous")
                
                with col2:
                    num_captures = st.number_input("Number of captures:", 1, 50, 5)
                
                if enable_continuous:
                    st.markdown(f"Capturing {num_captures} frames...")
                    
                    for capture_idx in range(num_captures):
                        img_file = st.camera_input(f"📷 Frame {capture_idx + 1}", key=f"continuous_capture_{capture_idx}")
                        
                        if img_file is not None:
                            file_bytes = np.asarray(bytearray(img_file.getvalue()), dtype=np.uint8)
                            frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

                            st.session_state.frame_count += 1
                            result, conf = detector.detect(frame)
                            if result:
                                st.session_state.detections_log[result] += 1

                            frame = cv2.resize(frame, (640, 480))

                            if result:
                                color = (0, 255, 0) if result == "No_Anx" else (0, 165, 255) if result == "Low_Anx" else (0, 0, 255)
                                cv2.putText(frame, f"{result} ({conf:.2f})", (10, 40), 
                                          cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 2)

                            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                            stframe.image(frame_rgb, use_column_width=True)

                            with result_placeholder.container():
                                st.markdown(f"**Result:** {result if result else 'Processing...'}")
                                if result:
                                    confidence_color = "🟢" if result == "No_Anx" else "🟡" if result == "Low_Anx" else "🔴"
                                    st.markdown(f"{confidence_color} **Confidence:** {conf:.2%}")

                            with confidence_placeholder.container():
                                st.bar_chart(st.session_state.detections_log)
                            
                            time.sleep(capture_interval / 1000.0)
        
        # WINDOWS/DESKTOP CAMERA MODE
        elif camera_mode == "💻 Windows/Desktop Camera":
            st.markdown("### Desktop Camera Mode")
            st.markdown("✅ Native Windows/Linux camera capture using OpenCV")
            
            col1, col2 = st.columns(2)
            
            with col1:
                camera_index = st.number_input("Camera Index:", 0, 5, 0, help="Usually 0 for default camera, 1 for second camera, etc.")
            
            with col2:
                enable_desktop = st.checkbox("Enable Desktop Camera", value=False, key="enable_desktop")
            
            if enable_desktop:
                cap = cv2.VideoCapture(camera_index)
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                cap.set(cv2.CAP_PROP_FPS, frame_rate)

                if not cap.isOpened():
                    st.error(f"❌ Cannot access camera at index {camera_index}. Please check:")
                    st.markdown("""
                    - Camera is properly connected
                    - Camera permissions are granted
                    - Try Camera Index 1 or 2 if default doesn't work
                    - Close other applications using the camera
                    """)
                else:
                    st.success("✅ Camera connected. Detecting anxiety levels...")
                    
                    col_status, col_frames = st.columns([1, 1])
                    with col_status:
                        detection_mode = st.radio("Mode:", ["🔴 Live Stream", "📸 Snapshot"], key="desktop_mode")
                    
                    if detection_mode == "🔴 Live Stream":
                        duration = st.slider("Duration (seconds):", 5, 60, 10)
                        start_time = time.time()
                        
                        if st.button("🎬 Start Detection", key="start_desktop"):
                            while (time.time() - start_time) < duration and enable_desktop:
                                ret, frame = cap.read()

                                if not ret:
                                    st.error("Failed to capture frame")
                                    break

                                st.session_state.frame_count += 1
                                result, conf = detector.detect(frame)

                                if result:
                                    st.session_state.detections_log[result] += 1

                                frame = cv2.resize(frame, (640, 480))

                                if result:
                                    color = (0, 255, 0) if result == "No_Anx" else (0, 165, 255) if result == "Low_Anx" else (0, 0, 255)
                                    cv2.putText(frame, f"{result} ({conf:.2f})", (10, 40), 
                                              cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 2)

                                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                                stframe.image(frame_rgb, use_column_width=True)

                                with result_placeholder.container():
                                    st.markdown(f"**Result:** {result if result else 'Processing...'}")
                                    if result:
                                        confidence_color = "🟢" if result == "No_Anx" else "🟡" if result == "Low_Anx" else "🔴"
                                        st.markdown(f"{confidence_color} **Confidence:** {conf:.2%}")

                                if st.session_state.frame_count % 10 == 0:
                                    with confidence_placeholder.container():
                                        st.bar_chart(st.session_state.detections_log)

                                time.sleep(1 / frame_rate)
                    
                    else:  # Snapshot mode
                        if st.button("📷 Capture Snapshot", key="snapshot_desktop"):
                            ret, frame = cap.read()
                            if ret:
                                st.session_state.frame_count += 1
                                result, conf = detector.detect(frame)
                                if result:
                                    st.session_state.detections_log[result] += 1

                                frame = cv2.resize(frame, (640, 480))

                                if result:
                                    color = (0, 255, 0) if result == "No_Anx" else (0, 165, 255) if result == "Low_Anx" else (0, 0, 255)
                                    cv2.putText(frame, f"{result} ({conf:.2f})", (10, 40), 
                                              cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 2)

                                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                                stframe.image(frame_rgb, use_column_width=True)

                                with result_placeholder.container():
                                    st.markdown(f"**Result:** {result if result else 'Processing...'}")
                                    if result:
                                        confidence_color = "🟢" if result == "No_Anx" else "🟡" if result == "Low_Anx" else "🔴"
                                        st.markdown(f"{confidence_color} **Confidence:** {conf:.2%}")

                                with confidence_placeholder.container():
                                    st.bar_chart(st.session_state.detections_log)

                cap.release()
        
        # SINGLE CAPTURE MODE
        else:  # Single Capture
            st.markdown("### Quick Capture")
            st.markdown("Take a single photo and get instant anxiety detection")
            
            img_file = st.camera_input("📷 Take a Photo", key="quick_capture")
            
            if img_file is not None:
                file_bytes = np.asarray(bytearray(img_file.getvalue()), dtype=np.uint8)
                frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

                # Process frame
                st.session_state.frame_count += 1
                result, conf = detector.detect(frame)
                if result:
                    st.session_state.detections_log[result] += 1

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
                    if result:
                        if result == "No_Anx":
                            st.success(f"🟢 **{result}**")
                        elif result == "Low_Anx":
                            st.warning(f"🟡 **{result}**")
                        else:
                            st.error(f"🔴 **{result}**")
                        st.markdown(f"**Confidence:** {conf:.2%}")
                    else:
                        st.markdown("Analyzing...")

                with confidence_placeholder.container():
                    st.bar_chart(st.session_state.detections_log)
        
        # Summary statistics
        st.markdown("---")
        st.markdown("### 📊 Session Summary")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Frames", st.session_state.frame_count)
        with col2:
            st.metric("High Anxiety", st.session_state.detections_log["High_Anx"])
        with col3:
            st.metric("Low Anxiety", st.session_state.detections_log["Low_Anx"])
        with col4:
            st.metric("No Anxiety", st.session_state.detections_log["No_Anx"])
    
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
