# 🚀 Quick Start Guide - Anxiety Detection Dashboard

## 30-Second Setup

### Windows

**Option 1: Automatic Setup (Recommended)**
```powershell
.\setup.ps1
```

**Option 2: Manual Setup**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run streamlit_app.py
```

### macOS / Linux

**Option 1: Automatic Setup**
```bash
chmod +x setup.sh
./setup.sh
```

**Option 2: Manual Setup**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## ✅ Verification Checklist

Before running, ensure:

- [ ] Python 3.9+ is installed
- [ ] Webcam is connected and working
- [ ] Model files exist:
  - `anxiety_model.json` 
  - `anxiety_model.h5`
- [ ] Internet connection (for initial dependency download)
- [ ] At least 2GB free RAM

## 🎯 First Run

1. **Open application** (usually automatic in browser)
   - If not, visit: `http://localhost:8501`

2. **Navigate to "Real-time Detection"** tab

3. **Enable Webcam** checkbox

4. **Position yourself** in good lighting

5. **View predictions** in real-time!

## 📊 Dashboard Sections

| Section | Purpose |
|---------|---------|
| 🏠 Home | Overview & quick stats |
| 🎥 Real-time Detection | Live webcam anxiety detection |
| 📊 Statistics | Detection history & analytics |
| ℹ️ About | Project information |

## ⚙️ Customization

### Change Detection Sensitivity
- Use "Confidence Threshold" slider (0.0-1.0)
- Lower = more detections, less strict
- Higher = fewer detections, more strict

### Adjust Frame Rate
- Use "Frame Rate (FPS)" slider (1-30)
- Lower = faster, lower quality
- Higher = slower, higher quality

### Change Theme
Edit `.streamlit/config.toml` to customize:
- Colors
- Font
- Sidebar settings

## 🆘 Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| Webcam not detected | Check permissions, try different camera |
| Model not loading | Verify file locations and names |
| Slow performance | Reduce frame rate, close other apps |
| Port already in use | `streamlit run streamlit_app.py --server.port 8502` |

## 📚 Full Documentation

See `STREAMLIT_README.md` for comprehensive documentation.

## 🔗 Useful Commands

```bash
# Run on different port
streamlit run streamlit_app.py --server.port 8502

# Run without opening browser
streamlit run streamlit_app.py --logger.level=debug

# Check Streamlit version
streamlit --version

# List all Streamlit commands
streamlit --help
```

## 💡 Tips

✨ **For best results:**
- Use natural lighting
- Position face 30-60cm from camera
- Keep face centered and straight
- Use confidence threshold of 0.5-0.7

🎬 **Recording results:**
- Results are shown in real-time
- Statistics tab shows aggregate data
- Screenshots can be taken from browser

⚡ **Performance optimization:**
- Close unnecessary applications
- Use GPU if available
- Reduce video resolution if needed

---

**Ready to detect anxiety levels? Let's go! 🚀**
