#!/usr/bin/env python3
"""
Script to update user credentials in both Firebase Auth and Firestore
"""

import sys
import os
from datetime import datetime
from werkzeug.security import generate_password_hash
import firebase_admin
from firebase_admin import auth, credentials

# Add current directory to path to import local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from firestore_utils import init_firestore, get_user_by_email, add_user, update_user

# Initialize Firebase Admin SDK (only once)
if not firebase_admin._apps:
    cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "firebase-key.json")
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

def generate_rajesh_hash():
    """Generate password hash for Rajesh@123"""
    return generate_password_hash("Rajesh@123")

def ensure_firebase_auth_user(email, password, display_name):
    """
    Create Firebase Auth user if doesn't exist, or get existing UID
    """
    try:
        user = auth.get_user_by_email(email)
        print(f"Firebase Auth user exists: {email}")
    except auth.UserNotFoundError:
        user = auth.create_user(email=email, password=password, display_name=display_name)
        print(f"✓ Created Firebase Auth user: {email}")
    return user.uid

def update_user_credentials():
    """Update Firestore & Firebase Auth user credentials"""

    plain_password = "Rajesh@123"
    password_hash = generate_rajesh_hash()
    print(f"Generated hash for 'Rajesh@123': {password_hash}\n")

    required_users = [
        # Admins
        {'email': 'rajesh4telecom@gmail.com', 'name': 'Rajesh (Admin)', 'role': 'admin', 'phone': '+91-8819881881', 'id': 'usr_rajesh_admin'},
        {'email': 'admin@apniholidays.com', 'name': 'Apni (Admin)', 'role': 'admin', 'phone': '+91-6371573038', 'id': 'usr_admin_main'},
        {'email': 'rkm.ytw1@gmail.com', 'name': 'RKM-1 (Admin)', 'role': 'admin', 'phone': '+91-9876543209', 'id': 'usr_rkm1_admin'},
        # Users
        {'email': 'rkm.ytw2@gmail.com', 'name': 'RKM-2 (User)', 'role': 'user', 'phone': '+91-9876543210', 'id': 'usr_rkm2_user'},
        {'email': 'rkm.ytw3@gmail.com', 'name': 'RKM-3 (User)', 'role': 'user', 'phone': '+91-9876543211', 'id': 'usr_rkm3_user'},
        {'email': 'rkm.ytw4@gmail.com', 'name': 'RKM-4 (User)', 'role': 'user', 'phone': '+91-9876543212', 'id': 'usr_rkm4_user'}
    ]

    print("Syncing users with Firebase Auth and Firestore...\n")

    for user_info in required_users:
        try:
            # Create/check Firebase Auth
            firebase_uid = ensure_firebase_auth_user(user_info['email'], plain_password, user_info['name'])

            # Prepare Firestore user data
            user_data = {
                'name': user_info['name'],
                'email': user_info['email'],
                'phone': user_info['phone'],
                'password': password_hash,
                'firebase_uid': firebase_uid,
                'status': 'active',
                'role': user_info['role'],
                'created_at': datetime.now(),
                'last_login': None
            }

            existing_user = get_user_by_email(user_info['email'])

            if existing_user:
                print(f"Updating Firestore user: {user_info['email']}")
                success = update_user(existing_user['id'], user_data)
                if success:
                    print(f"✓ Firestore updated: {user_info['email']}\n")
                else:
                    print(f"✗ Failed to update Firestore: {user_info['email']}\n")
            else:
                print(f"Creating Firestore user: {user_info['email']}")
                user_data['id'] = user_info['id']
                result = add_user(user_data)
                if result:
                    print(f"✓ Firestore created: {user_info['email']}\n")
                else:
                    print(f"✗ Failed to create Firestore user: {user_info['email']}\n")

        except Exception as e:
            print(f"✗ Error for {user_info['email']}: {e}\n")

    print("✅ User credential update complete!")

if __name__ == '__main__':
    update_user_credentials()
