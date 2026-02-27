# 🌐 Deployment Guide - PGT TMS

## For Online Deployment on Your Domain

---

## 📋 Prerequisites

- Domain name (e.g., tms.pgtinternational.com)
- Web server (VPS, Cloud hosting, etc.)
- Python 3.9+
- Node.js 16+
- PostgreSQL or MySQL (recommended for production)

---

## 🚀 Deployment Steps

### 1. Prepare Your Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3 python3-pip -y

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y

# Install PostgreSQL (optional but recommended)
sudo apt install postgresql postgresql-contrib -y
```

### 2. Upload Your Application

```bash
# Upload via SCP, FTP, or Git
scp -r pgt-tms user@your-server:/var/www/

# Or clone from Git
git clone your-repo-url /var/www/pgt-tms
```

### 3. Setup Backend

```bash
cd /var/www/pgt-tms/backend

# Install dependencies
pip3 install -r requirements.txt

# Initialize database
python3 init_database.py
python3 create_admin.py

# For production, use PostgreSQL:
# Update database.py with PostgreSQL connection
```

### 4. Build Frontend

```bash
cd /var/www/pgt-tms/frontend

# Install dependencies
npm install

# Build for production
npm run build
```

### 5. Configure Backend for Production

Edit `backend/main.py`:

```python
# Update CORS origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 6. Setup Process Manager (PM2 or Systemd)

#### Option A: Using PM2

```bash
# Install PM2
sudo npm install -g pm2

# Start backend
cd /var/www/pgt-tms/backend
pm2 start "uvicorn main:app --host 0.0.0.0 --port 8002" --name pgt-backend

# Save PM2 configuration
pm2 save
pm2 startup
```

#### Option B: Using Systemd

Create `/etc/systemd/system/pgt-backend.service`:

```ini
[Unit]
Description=PGT TMS Backend
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/pgt-tms/backend
ExecStart=/usr/bin/python3 -m uvicorn main:app --host 0.0.0.0 --port 8002
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable pgt-backend
sudo systemctl start pgt-backend
```

### 7. Setup Nginx as Reverse Proxy

Install Nginx:
```bash
sudo apt install nginx -y
```

Create `/etc/nginx/sites-available/pgt-tms`:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    # Frontend
    location / {
        root /var/www/pgt-tms/frontend/build;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8002;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/pgt-tms /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 8. Setup SSL Certificate (HTTPS)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com

# Auto-renewal is configured automatically
```

---

## 🔒 Security Checklist

- [ ] Change default admin password
- [ ] Use strong SECRET_KEY in backend
- [ ] Enable HTTPS (SSL certificate)
- [ ] Configure firewall (UFW)
- [ ] Use PostgreSQL instead of SQLite
- [ ] Set up regular database backups
- [ ] Restrict CORS to your domain only
- [ ] Keep system and packages updated

---

## 📊 Production Database Setup

### PostgreSQL Configuration:

1. Create database:
```bash
sudo -u postgres psql
CREATE DATABASE pgt_tms;
CREATE USER pgt_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE pgt_tms TO pgt_user;
\q
```

2. Update `backend/database.py`:
```python
SQLALCHEMY_DATABASE_URL = "postgresql://pgt_user:your_secure_password@localhost/pgt_tms"
```

3. Install PostgreSQL driver:
```bash
pip3 install psycopg2-binary
```

---

## 🔄 Updating Your Application

```bash
# Pull latest changes
cd /var/www/pgt-tms
git pull

# Update backend
cd backend
pip3 install -r requirements.txt
pm2 restart pgt-backend

# Update frontend
cd ../frontend
npm install
npm run build
```

---

## 📈 Monitoring

### Check Backend Status:
```bash
pm2 status
pm2 logs pgt-backend
```

### Check Nginx Status:
```bash
sudo systemctl status nginx
sudo tail -f /var/log/nginx/error.log
```

---

## 🆘 Troubleshooting

### Backend not starting?
```bash
# Check logs
pm2 logs pgt-backend

# Check if port is in use
sudo lsof -i :8002
```

### Frontend not loading?
```bash
# Check Nginx configuration
sudo nginx -t

# Check Nginx logs
sudo tail -f /var/log/nginx/error.log
```

### Database connection error?
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Test connection
psql -U pgt_user -d pgt_tms -h localhost
```

---

## 📝 Environment Variables

Create `.env` file in backend:

```env
DATABASE_URL=postgresql://pgt_user:password@localhost/pgt_tms
SECRET_KEY=your-very-secure-secret-key-here
ALLOWED_ORIGINS=https://yourdomain.com
DEBUG=False
```

---

## 🎯 Quick Deployment Checklist

- [ ] Server setup complete
- [ ] Application uploaded
- [ ] Backend dependencies installed
- [ ] Frontend built
- [ ] Database configured
- [ ] Backend running (PM2/Systemd)
- [ ] Nginx configured
- [ ] SSL certificate installed
- [ ] Domain DNS configured
- [ ] Security measures applied
- [ ] Backups configured
- [ ] Monitoring setup

---

## 📞 Support

For deployment assistance, contact your system administrator or hosting provider.

---

**Ready to deploy your PGT TMS to production!** 🚀
