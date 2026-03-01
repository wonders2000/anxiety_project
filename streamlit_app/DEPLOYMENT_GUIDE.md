# 🚀 Deployment Guide - Anxiety Detection Dashboard

## Deployment Options

Choose the best option for your use case:

| Option | Difficulty | Cost | Pros | Cons |
|--------|-----------|------|------|------|
| **Local** | ⭐ Easy | Free | Full control, no dependencies | Single machine only |
| **Streamlit Cloud** | ⭐ Easy | Free-$599/mo | Instant, auto-deploy from GitHub | Limited resources on free tier |
| **Docker + Server** | ⭐⭐⭐ Hard | Varies | Scalable, reproducible | Requires server knowledge |
| **Heroku** | ⭐⭐ Medium | Free-$50/mo | Easy setup, auto-deploy | Deprecated free tier |

---

## 1. 🏠 Local Deployment (Development)

### Best For
- Local testing and development
- Private use only
- Sharing on local network

### Quick Start
```bash
streamlit run streamlit_app.py
```

Access at: `http://localhost:8501`

### Share on Local Network
```bash
streamlit run streamlit_app.py --server.address 0.0.0.0
```

Then access from other machines using: `http://<your-ip>:8501`

---

## 2. ☁️ Streamlit Cloud (Recommended)

### Best For
- Quick deployment
- GitHub-based projects
- Free hosting
- Automatic updates

### Prerequisites
- GitHub account
- Project pushed to GitHub repo
- Free Streamlit account

### Deployment Steps

#### Step 1: Prepare Your Repository
```bash
git init
git add .
git commit -m "Streamlit anxiety detection dashboard"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/anxiety-detection.git
git push -u origin main
```

#### Step 2: Create Streamlit Cloud App
1. Go to https://streamlit.io/cloud
2. Click "Create app"
3. Select "GitHub account" (authorize if needed)
4. Choose repository: `anxiety-detection`
5. Choose branch: `main`
6. Choose file: `streamlit_app.py`
7. Click "Deploy"

#### Step 3: Share Your App
Once deployed, your app is live at:
```
https://<your-username>-anxiety-detection-<random>.streamlit.app
```

#### Environment Variables (if needed)
Create `.streamlit/secrets.toml`:
```toml
# .streamlit/secrets.toml
database_url = "postgresql://user:password@localhost/dbname"
api_key = "your-secret-key"
```

### Limitations
- **Free Tier**: 3 apps, 1 GB RAM, restart after 7 days of inactivity
- **Webcam**: May not work on web (browser security)
- **GPU**: Not available on free tier

### Cost Upgrade Path
- Free: $0
- Starter: $5/month (1 private app)
- Growth: $30/month (3 private apps)
- Business: Custom pricing

---

## 3. 🐳 Docker Deployment

### Best For
- Cloud servers (AWS, Google Cloud, Azure, DigitalOcean)
- Kubernetes/container orchestration
- Reproducible deployments

### Prerequisites
- Docker installed
- Docker Hub account (for image storage)

### Step 1: Create Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libsm6 libxext6 libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run Streamlit
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Step 2: Build Docker Image
```bash
docker build -t anxiety-detection:latest .
```

### Step 3: Run Container Locally
```bash
docker run -p 8501:8501 anxiety-detection:latest
```

### Step 4: Push to Docker Hub
```bash
docker tag anxiety-detection:latest YOUR_USERNAME/anxiety-detection:latest
docker push YOUR_USERNAME/anxiety-detection:latest
```

### Step 5: Deploy on Cloud

#### AWS EC2
```bash
# Connect to instance
ssh -i key.pem ec2-user@instance-ip

# Install Docker
sudo yum update -y
sudo yum install -y docker
sudo usermod -aG docker ec2-user

# Run container
docker run -d -p 8501:8501 YOUR_USERNAME/anxiety-detection:latest

# Access app
# http://instance-ip:8501
```

#### DigitalOcean Droplet
```bash
# Similar to EC2
# But use Ubuntu instead of Amazon Linux
sudo apt update
sudo apt install -y docker.io
```

#### Google Cloud Run
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/anxiety-detection
gcloud run deploy anxiety-detection \
  --image gcr.io/PROJECT_ID/anxiety-detection \
  --platform managed \
  --region us-central1
```

---

## 4. 🐍 Traditional Server (Advanced)

### Best For
- Maximum control
- Custom configuration
- Legacy infrastructure

### Prerequisites
- Ubuntu/CentOS server
- Python 3.9+
- Nginx or Apache

### Step 1: Server Setup
```bash
# SSH into server
ssh user@server-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.9 python3-pip python3-venv nginx

# Clone project
cd /var/www
git clone https://github.com/username/anxiety-detection.git
cd anxiety-detection
```

### Step 2: Setup Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Create Systemd Service
```bash
sudo nano /etc/systemd/system/anxiety-detection.service
```

```ini
[Unit]
Description=Anxiety Detection Streamlit App
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/anxiety-detection
Environment="PATH=/var/www/anxiety-detection/venv/bin"
ExecStart=/var/www/anxiety-detection/venv/bin/streamlit run streamlit_app.py \
  --server.port=8501 \
  --server.address=0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

### Step 4: Configure Nginx Reverse Proxy
```bash
sudo nano /etc/nginx/sites-available/anxiety-detection
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }
}
```

### Step 5: Enable and Start
```bash
sudo ln -s /etc/nginx/sites-available/anxiety-detection \
           /etc/nginx/sites-enabled/

sudo nginx -t
sudo systemctl restart nginx
sudo systemctl enable anxiety-detection
sudo systemctl start anxiety-detection
```

### Step 6: Setup SSL (Let's Encrypt)
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## 5. 📱 Mobile/Web Access (Webcam Limitations)

### Issue
Webcam access via browser has limitations due to security.

### Solutions

#### Option A: Use Progressive Web App
```bash
# Add to streamlit config
[client]
toolbarMode = "viewer"
```

#### Option B: Use WebRTC Bridge
Already integrated in `requirements.txt`:
```bash
streamlit-webrtc==0.47.0
```

Enhanced detection page can use:
```python
from streamlit_webrtc import webrtc_streamer
webrtc_ctx = webrtc_streamer(key="WrtcKey")
```

#### Option C: Server-Side Processing
Send frames to server without browser access restrictions.

---

## 6. 🔐 Security Best Practices

### Environment Variables
```bash
# Create .env file (add to .gitignore)
API_KEY=your-secret-key
DATABASE_URL=your-db-connection
```

Load in app:
```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
```

### Authentication (Optional)
```python
import streamlit as st

# Simple authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    password = st.text_input("Password", type="password")
    if password == "your-secret-password":
        st.session_state.authenticated = True
    else:
        st.stop()

# Rest of app
```

### HTTPS/SSL
Always use HTTPS in production:
```bash
# Streamlit Cloud: Automatic
# Docker: Use reverse proxy (Nginx/Apache)
# Server: Use Let's Encrypt
```

---

## 7. 📊 Monitoring & Logging

### Streamlit Cloud
- Built-in monitoring dashboard
- Email notifications

### Docker/Server
```bash
# Check logs
docker logs container-id
journalctl -u anxiety-detection -f

# Monitor resources
docker stats
htop
```

### Application Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('anxiety_detection.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
```

---

## 8. 📦 Backup & Recovery

### Backup Important Files
```bash
# Exclude venv and cache
tar --exclude='venv' --exclude='__pycache__' \
    --exclude='.git' -czf anxiety-detection-backup.tar.gz .
```

### Database Backups
```bash
# PostgreSQL
pg_dump dbname > backup.sql

# SQLite
cp anxiety.db anxiety.db.backup
```

---

## Troubleshooting Deployments

### Streamlit Cloud: Webcam Not Working
- Expected - browser security limitations
- Use local deployment for full functionality

### Docker: Out of Memory
```bash
# Increase memory limit
docker run -m 2g anxiety-detection:latest
```

### Nginx: Timeout Errors
```nginx
# Increase timeout
proxy_read_timeout 300;
proxy_connect_timeout 75;
```

### SSL Certificate Issues
```bash
sudo certbot renew
```

---

## Summary Table

| Deployment Type | Setup Time | Monthly Cost | Scalability | Webcam Support |
|-----------------|-----------|-------------|-------------|----------------|
| Local | 5 min | $0 | Single machine | ✅ Full |
| Streamlit Cloud | 15 min | $0-600 | Auto | ⚠️ Limited |
| Docker (VPS) | 30 min | $5-20 | Good | ✅ Full |
| Traditional Server | 1 hour | $10-50 | Very good | ✅ Full |

---

## Next Steps

1. **Choose your deployment method** based on your needs
2. **Follow the relevant section** above
3. **Test thoroughly** before going live
4. **Monitor logs** and performance
5. **Scale** as needed

---

**Need help? Check documentation or community forums!**

Good luck with your deployment! 🚀
