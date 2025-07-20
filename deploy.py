#!/usr/bin/env python3
"""
Deployment script for Apni Holidays
Run this script to set up the application in production
"""

import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 9):
        print("❌ Python 3.9 or higher is required")
        return False
    print("✅ Python version is compatible")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def setup_environment():
    """Set up environment variables"""
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            print("📋 Copying .env.example to .env")
            import shutil
            shutil.copy('.env.example', '.env')
            print("⚠️  Please update .env with your actual configuration")
        else:
            print("⚠️  No .env.example found")
    else:
        print("✅ .env file exists")

def main():
    """Main deployment function"""
    print("🌍 Apni Holidays Deployment Script")
    print("=" * 40)
    
    if not check_python_version():
        return
    
    setup_environment()
    
    print("\n✅ Basic setup complete!")
    print("\n📋 Next steps:")
    print("1. Update firebase-key.json with your Firebase service account key")
    print("2. Configure .env file with your settings")  
    print("3. Install dependencies: pip install -r requirements.txt")
    print("4. Start application: python main.py")
    print("   For production: gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app")
    
    print("\n🔑 Default Credentials:")
    print("Admin: rajesh4telecom@gmail.com / Rajesh@123")
    print("Admin: admin@apniholidays.com / Rajesh@123") 
    print("Admin: rkm.ytw1@gmail.com / Rajesh@123")

if __name__ == "__main__":
    main()