# Apni Holidays - Travel Booking Website

A complete travel booking platform built with Flask/Python and Firebase integration, designed for professional hosting environments.

## 🌟 Features

- **Complete Travel Package Management**: Browse and book travel packages with detailed itineraries
- **Firebase Authentication**: Secure user registration and login with Google Sign-In integration
- **Admin Panel**: Comprehensive management system for packages and users
- **Responsive Design**: Mobile-first design with Bootstrap framework
- **Firestore Database**: Real-time data storage and synchronization
- **Role-based Access**: Separate admin and user access levels

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Firebase project with Firestore enabled
- Web hosting environment (Replit, GoDaddy, etc.)

### Installation

1. **Upload files to your hosting environment**
2. **Install Python dependencies**:
   ```bash
   pip install flask firebase-admin google-cloud-firestore python-dateutil werkzeug gunicorn
   ```

3. **Configure Firebase**:
   - Replace `firebase-key.json` with your actual Firebase service account key
   - Update Firebase project ID in the configuration

4. **Set up environment variables**:
   - Copy `.env.example` to `.env`
   - Configure your database and session settings

5. **Run the application**:
   ```bash
   python main.py
   # OR for production:
   gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
   ```

## 📁 File Structure

```
apniholidays.com/
├── main.py                 # Main Flask application
├── firestore_utils.py      # Firestore database utilities
├── mock_data.py           # Development mock data
├── firebase-key.json      # Firebase service account key
├── .htaccess             # Apache configuration
├── .env.example          # Environment variables template
├── requirements.txt      # Python dependencies
└── static/               # CSS, JS, and image assets
```

## 🔑 Default Login Credentials

**Admin Accounts**:
- `rajesh4telecom@gmail.com` / `Rajesh@123`
- `admin@apniholidays.com` / `Rajesh@123` 
- `rkm.ytw1@gmail.com` / `Rajesh@123`

**User Accounts**:
- `rkm.ytw2@gmail.com` / `Rajesh@123`
- `rkm.ytw3@gmail.com` / `Rajesh@123`
- `rkm.ytw4@gmail.com` / `Rajesh@123`

## 🌟 Features Included

✅ **Complete Travel Package System**
- 5 Featured destinations: Thailand, Dubai, Phuket, Bali, Singapore
- Detailed package information with pricing and itineraries
- Image galleries and responsive design

✅ **User Authentication System**
- Email/password registration and login
- Google Sign-In integration
- Secure password hashing
- Session management

✅ **Admin Management Panel**
- Package management (add, edit, delete, feature packages)
- User management and monitoring
- Dashboard with statistics
- Role-based access control

✅ **Database Integration**
- Firebase Firestore for production use
- Mock data system for development
- Real-time data synchronization
- Automatic fallback system

## 🚀 Deployment

### For GoDaddy Hosting
1. Upload all files to your hosting directory
2. Ensure Python 3.9+ is available
3. Install required packages via pip
4. Configure `.htaccess` for URL rewriting
5. Set up SSL certificate for HTTPS

### For Replit
1. Import the project files
2. Install packages using the package manager
3. Configure secrets for environment variables
4. Run with the provided workflow configuration

## 📞 Support

For technical support or customization requests, please refer to the setup guide or contact the development team.

## 🔒 Security

- All passwords are securely hashed using Werkzeug
- Firebase handles authentication security
- HTTPS enforced via .htaccess
- Input validation and SQL injection prevention
- Session security with secure tokens

---

**Built with ❤️ for Apni Holidays Travel Agency**