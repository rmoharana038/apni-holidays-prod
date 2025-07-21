#!/usr/bin/env python3
"""
Script to update or create predefined user credentials in Firestore
"""

from werkzeug.security import generate_password_hash
from datetime import datetime
import sys
import os

# Set path to import local firestore_utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from firestore_utils import (
    init_firestore,
    get_user_by_email,
    add_user,
    update_user
)

# Initialize Firestore
init_firestore()

def generate_default_password_hash():
    """Generate hash for default password 'Rajesh@123'"""
    return generate_password_hash("Rajesh@123")

def update_user_credentials():
    """Update or create user credentials in Firestore"""
    password_hash = generate_default_password_hash()

    required_users = [
        # Admins
        {
            'id': 'usr_rajesh_admin',
            'name': 'Rajesh (Admin)',
            'email': 'rajesh4telecom@gmail.com',
            'role': 'admin',
            'phone': '+91-8819881881'
        },
        {
            'id': 'usr_admin_main',
            'name': 'Apni (Admin)',
            'email': 'admin@apniholidays.com',
            'role': 'admin',
            'phone': '+91-6371573038'
        },
        {
            'id': 'usr_rkm1_admin',
            'name': 'RKM-1 (Admin)',
            'email': 'rkm.ytw1@gmail.com',
            'role': 'admin',
            'phone': '+91-9876543209'
        },
        # Users
        {
            'id': 'usr_rkm2_user',
            'name': 'RKM-2 (User)',
            'email': 'rkm.ytw2@gmail.com',
            'role': 'user',
            'phone': '+91-9876543210'
        },
        {
            'id': 'usr_rkm3_user',
            'name': 'RKM-3 (User)',
            'email': 'rkm.ytw3@gmail.com',
            'role': 'user',
            'phone': '+91-9876543211'
        },
        {
            'id': 'usr_rkm4_user',
            'name': 'RKM-4 (User)',
            'email': 'rkm.ytw4@gmail.com',
            'role': 'user',
            'phone': '+91-9876543212'
        }
    ]

    print("\n🚀 Starting user credential update...")

    for user_info in required_users:
        try:
            existing_user = get_user_by_email(user_info['email'])

            user_data = {
                'name': user_info['name'],
                'email': user_info['email'],
                'phone': user_info['phone'],
                'password': password_hash,
                'firebase_uid': '',
                'status': 'active',
                'role': user_info['role'],
                'created_at': datetime.now(),
                'last_login': None
            }

            if existing_user:
                # Update existing user by document ID
                print(f"🔄 Updating existing user: {user_info['email']}")
                success = update_user(existing_user['id'], user_data)
                if success:
                    print(f"✅ Updated: {user_info['email']}")
                else:
                    print(f"❌ Failed to update: {user_info['email']}")
            else:
                # Add new user with specified ID
                user_data['id'] = user_info['id']
                print(f"➕ Creating new user: {user_info['email']}")
                result_id = add_user(user_data)
                if result_id:
                    print(f"✅ Created: {user_info['email']} (ID: {result_id})")
                else:
                    print(f"❌ Failed to create: {user_info['email']}")

        except Exception as e:
            print(f"⚠️ Error processing {user_info['email']}: {e}")

    print("\n🎉 User credential update complete!")

if __name__ == "__main__":
    update_user_credentials()
