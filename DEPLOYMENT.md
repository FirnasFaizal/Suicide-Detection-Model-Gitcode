# Deployment Guide

## 🌐 Production Deployment Options

### Option 1: Docker Deployment (Recommended)

#### Backend Dockerfile
Create `backend/Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY ../model /app/model

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Frontend Dockerfile
Create `frontend/Dockerfile`:
```dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### Docker Compose
Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    volumes:
      - ./model:/app/model
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped
```

Run with:
```bash
docker-compose up -d
```

### Option 2: Cloud Platforms

#### Render.com

**Backend:**
1. Create new Web Service
2. Connect GitHub repository
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variable: `GEMINI_API_KEY`

**Frontend:**
1. Create new Static Site
2. Build command: `npm install && npm run build`
3. Publish directory: `dist`

#### Vercel (Frontend)

```bash
cd frontend
npm install -g vercel
vercel --prod
```

Add environment variable in Vercel dashboard:
- `VITE_API_BASE_URL`: Your backend URL

#### Railway (Backend)

1. Create new project
2. Deploy from GitHub
3. Add `GEMINI_API_KEY` environment variable
4. Railway auto-detects Python and runs the app

#### Heroku

**Backend:**
Create `Procfile`:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

Deploy:
```bash
heroku create mindsafe-backend
heroku config:set GEMINI_API_KEY=your_key
git push heroku main
```

### Option 3: VPS (DigitalOcean, AWS EC2, etc.)

#### Setup Script
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3 python3-pip python3-venv -y

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install Nginx
sudo apt install nginx -y

# Clone repository
git clone your-repo-url
cd your-repo

# Setup backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create systemd service
sudo nano /etc/systemd/system/mindsafe-backend.service
```

**Backend Service File:**
```ini
[Unit]
Description=MindSafe Backend
After=network.target

[Service]
User=your-user
WorkingDirectory=/path/to/backend
Environment="PATH=/path/to/backend/venv/bin"
EnvironmentFile=/path/to/backend/.env
ExecStart=/path/to/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable mindsafe-backend
sudo systemctl start mindsafe-backend
```

#### Nginx Configuration
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

#### SSL with Let's Encrypt
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

## 🔒 Production Security Checklist

### Backend
- [ ] Set `DEBUG=False` in production
- [ ] Use strong secret keys
- [ ] Enable HTTPS only
- [ ] Configure CORS for specific domains
- [ ] Add rate limiting
- [ ] Set up logging and monitoring
- [ ] Use environment variables for secrets
- [ ] Enable request validation
- [ ] Add API authentication if needed
- [ ] Set up database backups (if using DB)

### Frontend
- [ ] Minify and bundle assets
- [ ] Enable gzip compression
- [ ] Set up CDN for static assets
- [ ] Configure CSP headers
- [ ] Remove console.logs
- [ ] Add error tracking (Sentry)
- [ ] Enable HTTPS
- [ ] Set cache headers
- [ ] Add analytics (optional)

## 📊 Monitoring

### Backend Monitoring
```python
# Add to main.py
from prometheus_client import Counter, Histogram
import time

REQUEST_COUNT = Counter('requests_total', 'Total requests')
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency')

@app.middleware("http")
async def monitor_requests(request, call_next):
    REQUEST_COUNT.inc()
    start_time = time.time()
    response = await call_next(request)
    REQUEST_LATENCY.observe(time.time() - start_time)
    return response
```

### Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

## 🚀 Performance Optimization

### Backend
- Use gunicorn with multiple workers
- Enable response caching
- Optimize model loading
- Use async operations
- Add request queuing for high load

### Frontend
- Code splitting
- Lazy loading components
- Image optimization
- Service worker for offline support
- Preload critical resources

## 📈 Scaling

### Horizontal Scaling
- Load balancer (Nginx, HAProxy)
- Multiple backend instances
- Shared model storage (S3, GCS)
- Redis for session management

### Vertical Scaling
- Increase server resources
- Optimize model inference
- Use GPU for faster predictions
- Database query optimization

## 🔄 CI/CD Pipeline

### GitHub Actions Example
Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy Backend
        run: |
          # Your deployment commands
          
      - name: Deploy Frontend
        run: |
          cd frontend
          npm install
          npm run build
          # Deploy to hosting
```

## 💰 Cost Estimation

### Small Scale (< 1000 users/day)
- Render/Railway: $7-15/month
- Vercel: Free tier
- Total: ~$10-20/month

### Medium Scale (1000-10000 users/day)
- VPS (2GB RAM): $10-20/month
- CDN: $5-10/month
- Monitoring: $10/month
- Total: ~$25-40/month

### Large Scale (> 10000 users/day)
- Multiple servers: $50-100/month
- Load balancer: $10-20/month
- CDN: $20-50/month
- Monitoring: $20-50/month
- Total: ~$100-220/month

## 🆘 Troubleshooting Production Issues

### Backend not responding
```bash
# Check service status
sudo systemctl status mindsafe-backend

# Check logs
sudo journalctl -u mindsafe-backend -f

# Restart service
sudo systemctl restart mindsafe-backend
```

### High memory usage
- Reduce number of workers
- Optimize model loading
- Add memory limits
- Use model quantization

### Slow response times
- Enable caching
- Optimize database queries
- Use CDN for static assets
- Add load balancing

## 📞 Support

For deployment issues:
1. Check logs first
2. Verify environment variables
3. Test API endpoints manually
4. Check firewall/security groups
5. Review server resources
