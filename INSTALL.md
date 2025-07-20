# Installation Guide - Apni Holidays

## Quick Installation

### Automatic Setup (Recommended)
```bash
python deploy.py
```

### Manual Setup

1. **Install Dependencies**
   ```bash
   pip install flask firebase-admin google-cloud-firestore python-dateutil werkzeug gunicorn
   # OR
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your actual settings
   ```

3. **Update Firebase Configuration**
   - Replace `firebase-key.json` with your actual Firebase service account key
   - Update project ID in the configuration files

4. **Run Application**
   ```bash
   # Development
   python main.py
   
   # Production
   gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
   ```

## Platform-Specific Instructions

### Replit
1. Upload all files to your Replit project
2. Run `python deploy.py` for setup
3. Configure secrets in the Secrets panel
4. Use the provided workflow or run `python main.py`

### GoDaddy Hosting
1. Upload all files to your hosting directory
2. Ensure Python 3.9+ is available through your hosting panel
3. Install packages via SSH: `pip install -r requirements.txt`
4. Configure Apache with the provided .htaccess file
5. Set up SSL certificate for HTTPS

### Other Cloud Providers
Follow your provider's Python/Flask deployment instructions.

## Configuration Files

- **`.env`** - Environment variables and secrets
- **`.htaccess`** - Apache web server configuration  
- **`firebase-key.json`** - Firebase service account credentials
- **`requirements.txt`** - Python package dependencies
- **`main.py`** - Main Flask application
- **`firestore_utils.py`** - Database utilities

## Default Login Credentials

### Admin Accounts
- **rajesh4telecom@gmail.com** / Rajesh@123 (Primary Admin)
- **admin@apniholidays.com** / Rajesh@123 (System Admin)
- **rkm.ytw1@gmail.com** / Rajesh@123 (RKM Admin)

### User Accounts  
- **rkm.ytw2@gmail.com** / Rajesh@123
- **rkm.ytw3@gmail.com** / Rajesh@123
- **rkm.ytw4@gmail.com** / Rajesh@123

## Features Included

✅ **Complete Travel Booking System**
- Browse travel packages (Thailand, Dubai, Phuket, Bali, Singapore)
- User registration and authentication
- Google Sign-In integration
- Admin panel for package and user management

✅ **Security Features**
- Password hashing with Werkzeug
- Firebase authentication
- Session management
- HTTPS enforcement

✅ **Database Integration**
- Firestore (NoSQL) database
- Mock data fallback for development
- Real-time data synchronization

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Verify Firebase configuration in `firebase-key.json`
   - Check internet connection
   - Ensure Firestore is enabled in Firebase console

2. **Authentication Issues**  
   - Verify Firebase project settings
   - Check API keys and configuration
   - Ensure authentication methods are enabled

3. **Module Import Errors**
   - Run `pip install -r requirements.txt`
   - Check Python version (3.9+ required)

### Support
For additional help, refer to:
- `README.md` - Project overview
- `setup-guide.md` - Detailed setup instructions
- `user_credentials_summary.md` - Account information

---
**Apni Holidays Travel Booking System** - Built with Flask, Firebase, and Bootstrap