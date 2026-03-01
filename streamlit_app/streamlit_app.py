import streamlit as st
from streamlit_option_menu import option_menu
import base64
import cv2
import numpy as np
from utils.model import AnxietyDetector

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="Anxiety Detection Dashboard",
    page_icon="😰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------- BACKGROUND IMAGE ---------------- #
def set_bg(image_file):
    with open(image_file, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg("assets/img1_back.jpg")

st.markdown(
    f"""
    <style>

    /* Dark overlay for readability */
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(255,255,255,0.85);
        z-index: -1;
    }}

    /* Force all text to black */
    html, body, [class*="css"]  {{
        color: black !important;
    }}

    .title-main {{
        font-size: 2.5rem;
        font-weight: bold;
        color: black;
        margin-bottom: 2rem;
    }}
    </style>
    """,
    unsafe_allow_html=True
)


# ---------------- SIDEBAR ---------------- #
with st.sidebar:
    st.title("🧠 Anxiety Detection")
    st.markdown("---")

    selected = option_menu(
        menu_title=None,
        options=["Home", "Real-time Detection", "About"],
        icons=["house", "camera-video", "info-circle"],
        default_index=0,
    )

# ---------------- HOME PAGE ---------------- #
if selected == "Home":

    st.markdown(
        '<p class="title-main" style="color:#111111;">🧠 Anxiety Detection System</p>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style="color:#111111; font-size:17px; line-height:1.6;">
        
        <h3>Welcome</h3>

        This application uses <b>deep learning</b> to detect anxiety levels from facial expressions.

        <br><br>
        <b>Detection Levels:</b>
        <ul>
            <li>😟 High Anxiety</li>
            <li>😐 Low Anxiety</li>
            <li>😊 No Anxiety</li>
        </ul>

        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="color:#111111; font-size:17px; line-height:1.6;">
        
        <h3>How It Works</h3>

        <ol>
            <li>Face Detection</li>
            <li>Image Preprocessing</li>
            <li>CNN Model Prediction</li>
            <li>Real-time Result Display</li>
        </ol>

        </div>
        """, unsafe_allow_html=True)

# ---------------- DETECTION PAGE ---------------- #
elif selected == "Real-time Detection":

    st.markdown(
        '<p class="title-main" style="color:#111111;">🎥 Real-time Anxiety Detection</p>',
        unsafe_allow_html=True
    )

    detector = AnxietyDetector()

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(
            '<h3 style="color:#111111;">Live Feed</h3>',
            unsafe_allow_html=True
        )
        stframe = st.empty()

    with col2:
        st.markdown(
            '<h3 style="color:#111111;">Controls</h3>',
            unsafe_allow_html=True
        )
        start_detection = st.checkbox("Enable Webcam")

    result_placeholder = st.empty()

    if start_detection:

        st.markdown(
            '<p style="color:#111111; font-weight:500;">Using browser camera for secure access.</p>',
            unsafe_allow_html=True
        )

        img_file = st.camera_input("Take a Photo")

        if img_file is not None:
            file_bytes = np.asarray(bytearray(img_file.getvalue()), dtype=np.uint8)
            frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

            result, conf = detector.detect(frame)
            frame = cv2.resize(frame, (640, 480))

            if result:
                color = (0, 200, 0) if result == "No_Anx" else \
                        (255, 165, 0) if result == "Low_Anx" else \
                        (255, 0, 0)

                cv2.putText(
                    frame,
                    f"{result} ({conf:.2f})",
                    (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.2,
                    color,
                    2
                )

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            stframe.image(frame_rgb, use_column_width=True)

            with result_placeholder.container():
                if result:
                    st.markdown(
                        f'<h3 style="color:#111111;">Result: {result}</h3>',
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f'<p style="color:#111111; font-size:18px;">Confidence: {conf:.2%}</p>',
                        unsafe_allow_html=True
                    )

    else:
        st.markdown(
            '<p style="color:#111111;">Enable webcam</p>',
            unsafe_allow_html=True
        )

# ---------------- ABOUT PAGE ---------------- #
elif selected == "About":
    st.markdown(
        '<p class="title-main" style="color:#000000;">ℹ️ About This Project</p>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div style="color:#000000; font-size:17px; line-height:1.6;">
    
    <b>Anxiety Detection System</b> is a CNN-based deep learning application
    that analyzes facial expressions to estimate anxiety levels.

    <br><br>
    <b>Tech Stack</b>
    <ul>
        <li>Streamlit</li>
        <li>TensorFlow / Keras</li>
        <li>OpenCV</li>
    </ul>

    <b>Model</b>
    <ul>
        <li>CNN Architecture</li>
        <li>48x48 grayscale input</li>
        <li>3-class output</li>
    </ul>

    </div>
    """, unsafe_allow_html=True)