# 🧠 Anxiety Detection Dashboard - Streamlit Edition

A modern, real-time anxiety detection system built with **Streamlit** and **TensorFlow/Keras**.

## 📋 Features

- ⚡ **Real-time Detection** - Live webcam anxiety detection with confidence scores
- 📊 **Interactive Dashboard** - Beautiful and intuitive user interface
- 🎯 **Multi-level Classification** - High Anxiety, Low Anxiety, No Anxiety
- 📈 **Statistics & Analytics** - Track detection history and trends
- 🎨 **Modern UI** - Clean, responsive design with dark/light mode support
- 🔒 **Privacy-First** - All processing done locally

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Webcam/camera connected to your system
- 2GB RAM minimum

### Installation

1. **Clone or Download the Project**
```bash
cd Anxity_Project
```

2. **Create Virtual Environment** (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Verify Model Files**
Ensure these files exist in your project directory:
- `anxiety_model.json` - Model architecture
- `anxiety_model.h5` - Model weights

Or in the `model/` folder:
- `model/anxiety_model.json`
- `model/anxiety_model.h5`

### Running the Application

```bash
streamlit run streamlit_app.py
```

The app will open in your default browser at `http://localhost:8501`

## 📱 Application Structure

### Pages

#### 1. **Home** 🏠
- Welcome and overview
- Quick statistics
- Information about the system

#### 2. **Real-time Detection** 🎥
- Live webcam feed
- Real-time anxiety detection
- Confidence scores
- Detection statistics
- Adjustable settings:
  - Confidence threshold
  - Frame rate control
  - Enable/disable webcam

#### 3. **Statistics** 📊
- Detection history
- Anxiety distribution charts
- Session statistics
- Trends and analytics

#### 4. **About** ℹ️
- Project information
- Technology stack
- Model details
- Features and limitations

## 🔧 Configuration

### Streamlit Config (`.streamlit/config.toml`)
The application uses custom theme colors and settings. Edit this file to customize:
- Primary color
- Background color
- Font preferences
- Server settings

### Environment Variables
Create a `.env` file if needed:
```
MODEL_PATH=anxiety_model.json
WEIGHTS_PATH=anxiety_model.h5
FACE_CASCADE_PATH=haarcascade/haarcascade_frontalface_default.xml
```

## 📊 How It Works

### Detection Pipeline

1. **Face Detection**
   - Uses Haar Cascade Classifier
   - Detects frontal faces in video frame

2. **Image Processing**
   - Crops detected face region
   - Resizes to 48x48 pixels (model input size)
   - Converts to grayscale
   - Normalizes pixel values (0-1)

3. **Model Inference**
   - Passes processed image to Keras model
   - Returns probability distribution across 3 classes
   - Selects class with highest probability

4. **Visualization**
   - Draws bounding box around detected face
   - Displays predicted anxiety level
   - Shows confidence score

### Model Details

- **Architecture**: Convolutional Neural Network (CNN)
- **Input Size**: 48×48 grayscale images
- **Output Classes**: 3
  - 0: High Anxiety 😟
  - 1: Low Anxiety 😐
  - 2: No Anxiety 😊
- **Model Format**: Keras (JSON + HDF5)

## 📦 Project Structure

```
Anxity_Project/
├── streamlit_app.py          # Main Streamlit application
├── requirements.txt          # Python dependencies
├── anxiety_model.json        # Model architecture
├── anxiety_model.h5          # Model weights
├── haarcascade/              # Face detection cascade
│   └── haarcascade_frontalface_default.xml
├── utils/                    # Utility modules
│   ├── __init__.py
│   └── model.py             # AnxietyDetector class
├── model/                    # Alternative model location
│   ├── anxiety_model.json
│   └── anxiety_model.h5
├── data/                     # Training/test data (optional)
│   ├── train/
│   └── test/
├── .streamlit/
│   └── config.toml          # Streamlit configuration
└── README.md                # This file
```

## ⚙️ System Requirements

### Minimum
- CPU: Dual-core 2.0 GHz
- RAM: 2 GB
- Disk: 500 MB free space
- Python: 3.9+

### Recommended
- CPU: Quad-core 2.4 GHz
- RAM: 4 GB
- Disk: 2 GB free space
- GPU: NVIDIA GPU with CUDA support (optional, for faster inference)

## 🎯 Tips for Best Results

1. **Lighting**: Use adequate lighting to clearly see your face
2. **Face Orientation**: Keep your face straight and centered
3. **Distance**: Position yourself 30-60 cm from the webcam
4. **Background**: Use a plain, non-distracting background
5. **Confidence Threshold**: Adjust based on your needs (0.5-0.9 recommended)

## 🐛 Troubleshooting

### Webcam Not Working
```bash
# Check if webcam is accessible
python -c "import cv2; cap = cv2.VideoCapture(0); print(cap.isOpened())"
```

### Model Not Loading
- Verify model files exist in project root or `model/` folder
- Check file permissions
- Ensure correct file formats (.json and .h5)

### Performance Issues
- Reduce frame rate in the app
- Close other applications
- Ensure adequate disk space
- Consider using GPU if available

### Module Import Errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Verify Streamlit installation
streamlit --version
```

## 🚀 Deployment

### Local Server
```bash
streamlit run streamlit_app.py
```

### Streamlit Cloud (Free)
1. Push project to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy from your repository
4. Note: Webcam access may be limited on web deployments

### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py"]
```

## 📈 Future Enhancements

- [ ] Database integration for storing results
- [ ] Export reports and statistics
- [ ] Multiple language support
- [ ] Mobile app version
- [ ] Advanced analytics dashboard
- [ ] Model retraining interface
- [ ] User authentication
- [ ] API endpoint for integration

## 📝 License

[Your License Here]

## 👤 Author

[Your Name/Organization]

## 📧 Support

For issues, questions, or suggestions, please:
- Create an issue in the repository
- Contact: [your-email@example.com]

---

**Made with ❤️ using Streamlit and TensorFlow**

Last Updated: March 2024
