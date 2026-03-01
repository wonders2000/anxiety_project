# 📊 Project Architecture & Flow Diagrams

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│         Streamlit Application (streamlit_app.py)             │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌────────────────┐  ┌──────────────┐  ┌────────────────┐   │
│  │  Home Page     │  │  Detection   │  │  Statistics    │   │
│  │  📈 Overview   │  │  🎥 Webcam   │  │  📊 Analytics  │   │
│  │  🎯 Stats      │  │  🔍 Analysis │  │  📉 History    │   │
│  └────────────────┘  └──────────────┘  └────────────────┘   │
│                                                               │
└──────────┬──────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────┐
│            Utils Module (utils/model.py)                    │
├─────────────────────────────────────────────────────────────┤
│  AnxietyDetector Class                                      │
│  • load_model()      - Load Keras model                     │
│  • detect()          - Predict anxiety from frame           │
│  • detect_with_viz() - Draw predictions on frame            │
└──────────┬──────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────┐
│  Computer Vision Pipeline                                   │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Input Frame (BGR) → Face Detection → ROI Extraction        │
│        ↓                  ↓                ↓                 │
│    (640x480)      Haar Cascade      (48x48 Region)          │
│                                                               │
│  → Preprocessing → Model Inference → Post-processing        │
│      ↓                ↓                    ↓                 │
│  Grayscale       Keras Model        Confidence Score        │
│  Normalize       (1x48x48x1)         + Label                │
│                                                               │
└─────────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────┐
│           Deep Learning Model                               │
├─────────────────────────────────────────────────────────────┤
│  Format: anxiety_model.json + anxiety_model.h5              │
│  Architecture: CNN (Convolutional Neural Network)           │
│  Input: 48x48 grayscale image                               │
│  Output: 3 classes                                          │
│    • 0: High_Anx 😟                                          │
│    • 1: Low_Anx  😐                                          │
│    • 2: No_Anx   😊                                          │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
User Opens App
    │
    ▼
┌─────────────────────────┐
│  Select Page            │
│  • Home                 │
│  • Real-time Detection  │
│  • Statistics           │
│  • About                │
└────────────┬────────────┘
             │
             ├─────────────────────────┬──────────────────┬─────────┐
             │                         │                  │         │
             ▼                         ▼                  ▼         ▼
         HOME PAGE             DETECTION PAGE        STATS PAGE   ABOUT
         ┌─────────┐          ┌──────────────┐     ┌────────┐   ┌──────┐
         │Overview │          │1. Enable     │     │Charts  │   │Info  │
         │Stats    │          │   Webcam     │     │History │   │Tech  │
         │Info     │          │              │     │Records │   │Help  │
         │         │          │2. Start      │     │        │   │      │
         │         │          │   Detection  │     │        │   │      │
         │         │          │              │     │        │   │      │
         │         │          │3. View       │     │        │   │      │
         │         │          │   Predictions│     │        │   │      │
         │         │          │              │     │        │   │      │
         │         │          │4. Adjust     │     │        │   │      │
         │         │          │   Settings   │     │        │   │      │
         └─────────┘          └──────┬───────┘     └────────┘   └──────┘
                                     │
                                     ▼
                         ┌─────────────────────────┐
                         │ WEBCAM PROCESSING LOOP  │
                         └────────────┬────────────┘
                                      │
                 ┌────────────────────┼────────────────────┐
                 │                    │                    │
                 ▼                    ▼                    ▼
            Capture      Face Detection    Model Inference
            Frame        (Haar Cascade)    (CNN Prediction)
              │                │                 │
              └────────────────┴─────────────────┘
                       │
                       ▼
             ┌──────────────────────┐
             │ Draw Predictions     │
             │ • Bounding Box       │
             │ • Label              │
             │ • Confidence Score   │
             └──────┬───────────────┘
                    │
                    ▼
          ┌─────────────────────┐
          │ Display in Streamlit │
          │ • Video Frame        │
          │ • Stats Chart        │
          │ • Metrics            │
          └─────────────────────┘
```

## Detection Pipeline (Detailed)

```
                    ANXIETY DETECTION PIPELINE
                             │
        ┌────────────────────┴────────────────────┐
        │                                         │
        ▼                                         ▼
   ┌─────────────┐                        ┌──────────────┐
   │Load Model   │                        │Initialize    │
   │ • JSON      │                        │Face Cascade  │
   │ • Weights   │                        │ • Haar XML   │
   └──────┬──────┘                        └──────┬───────┘
          │                                      │
          └──────────────┬───────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  For Each Frame:     │
              └──────────┬───────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
    Resize         Convert to      Detect Faces
    to 500x500      Grayscale       (detectMultiScale)
        │                │                │
        └────────────────┼────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │ For Each Face:       │
              └──────────┬───────────┘
                         │
        ┌────────────────┼────────────────────────┐
        │                │                        │
        ▼                ▼                        ▼
    Extract          Resize            Normalize
    ROI (48x48)       to (48x48)        (0-1 range)
        │                │                        │
        └────────────────┼────────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │ Model Prediction:    │
              │ • Input: (1,48,48,1) │
              │ • Process: CNN       │
              │ • Output: [p0,p1,p2] │
              └──────────┬───────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
    Get Max       Get Confidence    Get Label
    Probability   Score (p_max)     anxiety_dict
        │                │                │
        └────────────────┼────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │ Return Results:      │
              │ • Label              │
              │ • Confidence         │
              │ • Bounding Box       │
              └──────────────────────┘
```

## File Dependencies

```
streamlit_app.py (Main Entry Point)
    │
    ├─► streamlit
    ├─► streamlit-option-menu
    ├─► cv2 (OpenCV)
    ├─► numpy
    │
    └─► utils/model.py
            │
            ├─► keras.models
            ├─► cv2 (OpenCV)
            ├─► numpy
            │
            ├─► anxiety_model.json ◄─────┬────────────────────┐
            └─► anxiety_model.h5         │                    │
                                    Also in model/ folder     │
                                                              │
            └─► haarcascade_frontalface_default.xml (from CV2)
```

## Configuration & Setup

```
Project Initialization
        │
    ┌───┴────────────────────┐
    │                        │
    ▼                        ▼
setup.bat              setup.ps1
(Windows)              (PowerShell)
    │                        │
    └───────────┬────────────┘
                │
                ▼
    Create Virtual Environment
                │
                ▼
    Install Dependencies
    (pip install -r requirements.txt)
                │
                ├─► TensorFlow
                ├─► Keras
                ├─► OpenCV
                ├─► Streamlit
                ├─► Numpy/Pandas
                └─► Other packages
                │
                ▼
    Load Model & Config
    (.streamlit/config.toml)
                │
                ▼
    Ready to Run!
    streamlit run streamlit_app.py
```

## Database Integration (Optional Future)

```
Streamlit App
    │
    ▼
detect_anxiety()
    │
    ▼
Result: (label, confidence, timestamp)
    │
    ├──► Display on UI ────────┐
    │                          │
    └──► Store in Database     │
         │                      │
         ▼                      │
    ┌─────────────────┐        │
    │ SQLite/PostgreSQL│        │
    ├─────────────────┤        │
    │ • Detections    │        │
    │ • Timestamps    │        │
    │ • Confidence    │        │
    │ • Labels        │        │
    └────────┬────────┘        │
             │                  │
             ▼                  ▼
         Statistics Page ────── Results Chart
         • Trends              • Predictions
         • Analytics           • History
         • Export Reports
```

## Deployment Architecture

```
                    USER
                     │
        ┌────────────┴─────────────┐
        │                          │
        ▼                          ▼
   Local Machine              Cloud Deployment
        │                          │
        ├─ Python Venv            ├─ Streamlit Cloud
        ├─ streamlit CLI          ├─ Docker Container
        └─ Direct Webcam          └─ Nginx Reverse Proxy
           Access                    │
                                     ▼
                                  HTTPS Connection
                                     │
                                     ▼
                                   Browser
```

## Performance Optimization

```
Performance Bottlenecks
        │
    ┌───┴─────────────────┬──────────────┬──────────────┐
    │                     │              │              │
    ▼                     ▼              ▼              ▼
Model       Face Detection    Image Processing    Display
Inference   (Haar Cascade)    (Resize, Normalize)  (Rendering)
    │                     │              │              │
    └─ Use GPU      ┌─────┘              │              │
    │              │          ┌──────────┘              │
    ├─ Batch       │          │          ┌──────────────┘
    │  Processing  │          │          │
    │              │          ▼          ▼
    │              │      Reduce     Lower
    │              │      Resolution Frame Rate
    │              │      (480p)     (15 FPS)
    ▼              ▼
  Result: ~20-50ms per frame = 20-50 FPS possible
```

---

**Diagrams created to help visualize the system architecture and data flows!**
