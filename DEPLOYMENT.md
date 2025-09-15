# 🚀 Deployment Guide - Marketing Intelligence Dashboard

This guide provides step-by-step instructions for deploying the Marketing Intelligence Dashboard on various hosting platforms.

## 📋 Prerequisites

- Python 3.8 or higher
- Git (for version control)
- Access to a hosting platform account

## 🏠 Local Development

### Quick Start
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run directly with Streamlit
streamlit run marketing_dashboard.py
```

### Manual Setup
```bash
# 1. Install dependencies
pip install streamlit pandas plotly numpy

# 2. Verify data files exist
ls "Marketing Intelligence Dashboard/"
# Should show: business.csv, Facebook.csv, Google.csv, TikTok.csv

# 3. Run dashboard
streamlit run marketing_dashboard.py --server.headless true --server.port 8501
```

## ☁️ Cloud Deployment Options

### Option 1: Streamlit Cloud (Recommended)

**Advantages**: Free, easy setup, automatic updates
**Best for**: Quick deployment, sharing with stakeholders

#### Steps:
1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Marketing Intelligence Dashboard"
   git branch -M main
   git remote add origin https://github.com/yourusername/marketing-dashboard.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file path: `marketing_dashboard.py`
   - Click "Deploy"

3. **Configure Secrets (if needed)**
   - Add any API keys or sensitive data in Streamlit Cloud secrets

### Option 2: Heroku

**Advantages**: Full control, custom domains
**Best for**: Production deployments, custom configurations

#### Steps:
1. **Create Heroku App**
   ```bash
   # Install Heroku CLI
   # Create Procfile
   echo "web: streamlit run marketing_dashboard.py --server.port=$PORT --server.address=0.0.0.0" > Procfile
   
   # Create runtime.txt
   echo "python-3.9.16" > runtime.txt
   
   # Deploy
   heroku create your-dashboard-name
   git push heroku main
   ```

2. **Configure Heroku**
   ```bash
   # Set environment variables
   heroku config:set STREAMLIT_SERVER_HEADLESS=true
   heroku config:set STREAMLIT_SERVER_PORT=8501
   
   # Scale the app
   heroku ps:scale web=1
   ```

### Option 3: AWS EC2

**Advantages**: Full control, scalable, cost-effective
**Best for**: Enterprise deployments, high traffic

#### Steps:
1. **Launch EC2 Instance**
   - Choose Ubuntu 20.04 LTS
   - Select t3.medium or larger
   - Configure security group (open port 8501)

2. **Setup Environment**
   ```bash
   # Connect to EC2
   ssh -i your-key.pem ubuntu@your-ec2-ip
   
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python and pip
   sudo apt install python3 python3-pip -y
   
   # Clone repository
   git clone https://github.com/yourusername/marketing-dashboard.git
   cd marketing-dashboard
   
   # Install dependencies
   pip3 install -r requirements.txt
   ```

3. **Run Dashboard**
   ```bash
   # Run in background
   nohup streamlit run marketing_dashboard.py --server.headless true --server.port 8501 --server.address 0.0.0.0 &
   
   # Or use systemd service
   sudo nano /etc/systemd/system/marketing-dashboard.service
   ```

4. **Systemd Service Configuration**
   ```ini
   [Unit]
   Description=Marketing Intelligence Dashboard
   After=network.target

   [Service]
   Type=simple
   User=ubuntu
   WorkingDirectory=/home/ubuntu/marketing-dashboard
   ExecStart=/usr/bin/python3 -m streamlit run marketing_dashboard.py --server.headless true --server.port 8501 --server.address 0.0.0.0
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

5. **Enable Service**
   ```bash
   sudo systemctl enable marketing-dashboard
   sudo systemctl start marketing-dashboard
   sudo systemctl status marketing-dashboard
   ```

### Option 4: Docker Deployment

**Advantages**: Consistent environment, easy scaling
**Best for**: Containerized deployments, microservices

#### Steps:
1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.9-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install -r requirements.txt

   COPY . .

   EXPOSE 8501

   CMD ["streamlit", "run", "marketing_dashboard.py", "--server.headless", "true", "--server.port", "8501", "--server.address", "0.0.0.0"]
   ```

2. **Build and Run**
   ```bash
   # Build image
   docker build -t marketing-dashboard .
   
   # Run container
   docker run -p 8501:8501 marketing-dashboard
   
   # Or with docker-compose
   docker-compose up -d
   ```

3. **Docker Compose Configuration**
   ```yaml
   version: '3.8'
   services:
     marketing-dashboard:
       build: .
       ports:
         - "8501:8501"
       volumes:
         - ./Marketing Intelligence Dashboard:/app/Marketing Intelligence Dashboard
       restart: unless-stopped
   ```

## 🔧 Configuration

### Environment Variables
```bash
# Streamlit configuration
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Optional: Custom theme
export STREAMLIT_THEME_BASE="light"
```

### Custom Domain (Optional)
```bash
# For production deployments
export STREAMLIT_SERVER_CERT_FILE=/path/to/cert.pem
export STREAMLIT_SERVER_KEY_FILE=/path/to/key.pem
```

## 📊 Performance Optimization

### For High Traffic
1. **Use Gunicorn with Streamlit**
   ```bash
   pip install gunicorn
   gunicorn --bind 0.0.0.0:8501 --workers 4 marketing_dashboard:app
   ```

2. **Enable Caching**
   - Streamlit automatically caches data with `@st.cache_data`
   - Consider Redis for distributed caching

3. **Load Balancing**
   - Use nginx as reverse proxy
   - Deploy multiple instances behind load balancer

### For Data Updates
1. **Automated Data Refresh**
   ```bash
   # Cron job to update data daily
   0 2 * * * /path/to/update_data.sh
   ```

2. **Real-time Updates**
   - Use Streamlit's experimental features
   - Implement WebSocket connections

## 🔒 Security Considerations

### Production Security
1. **Authentication**
   ```python
   # Add to marketing_dashboard.py
   import streamlit_authenticator as stauth
   
   # Implement user authentication
   authenticator = stauth.Authenticate(
       credentials,
       'cookie_name',
       'cookie_key',
       cookie_expiry_days=30
   )
   ```

2. **HTTPS Configuration**
   ```bash
   # Use reverse proxy (nginx)
   server {
       listen 443 ssl;
       server_name your-domain.com;
       
       ssl_certificate /path/to/cert.pem;
       ssl_certificate_key /path/to/key.pem;
       
       location / {
           proxy_pass http://localhost:8501;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

3. **Data Protection**
   - Encrypt sensitive data
   - Use environment variables for secrets
   - Implement access controls

## 📈 Monitoring & Maintenance

### Health Checks
```python
# Add to marketing_dashboard.py
@st.cache_data
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "data_loaded": combined_df is not None
    }
```

### Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dashboard.log'),
        logging.StreamHandler()
    ]
)
```

### Backup Strategy
1. **Data Backup**
   ```bash
   # Daily backup script
   tar -czf backup_$(date +%Y%m%d).tar.gz "Marketing Intelligence Dashboard/"
   ```

2. **Code Backup**
   - Use Git for version control
   - Regular commits and pushes
   - Tag releases for rollback

## 🚨 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Find process using port 8501
   lsof -i :8501
   # Kill process
   kill -9 PID
   ```

2. **Memory Issues**
   ```bash
   # Increase memory limit
   export STREAMLIT_SERVER_MAX_UPLOAD_SIZE=200
   ```

3. **Data Loading Errors**
   - Check file paths
   - Verify CSV format
   - Check file permissions

### Debug Mode
```bash
# Run with debug information
streamlit run marketing_dashboard.py --logger.level debug
```

## 📞 Support

For deployment issues:
1. Check the logs for error messages
2. Verify all dependencies are installed
3. Ensure data files are accessible
4. Check network connectivity and firewall settings

## 🎯 Next Steps

After successful deployment:
1. **Test all features** with sample data
2. **Configure monitoring** and alerting
3. **Set up automated backups**
4. **Train users** on dashboard features
5. **Plan regular updates** and maintenance

---

**Happy Deploying! 🚀**
