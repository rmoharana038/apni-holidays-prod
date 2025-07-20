#!/usr/bin/env python3
"""
Script to update user credentials with the specified requirements
"""

from werkzeug.security import generate_password_hash
from datetime import datetime
import sys
import os

# Add current directory to path to import local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from firestore_utils import init_firestore, get_user_by_email, add_user, update_user

def generate_rajesh_hash():
    """Generate password hash for Rajesh@123"""
    return generate_password_hash("Rajesh@123")

def update_user_credentials():
    """Update user credentials as per requirements"""
    
    password_hash = generate_rajesh_hash()
    print(f"Generated password hash: {password_hash}")
    
    # Define the required users
    required_users = [
        # Admin users
        {
            'email': 'rajesh4telecom@gmail.com',
            'name': 'Rajesh (Admin)',
            'role': 'admin',
            'phone': '+91-8819881881',
            'id': 'usr_rajesh_admin'
        },
        {
            'email': 'admin@apniholidays.com', 
            'name': 'Apni (Admin)',
            'role': 'admin',
            'phone': '+91-6371573038',
            'id': 'usr_admin_main'
        },
        {
            'email': 'rkm.ytw1@gmail.com',
            'name': 'RKM-1 (Admin)', 
            'role': 'admin',
            'phone': '+91-9876543209',
            'id': 'usr_rkm1_admin'
        },
        # Regular users
        {
            'email': 'rkm.ytw2@gmail.com',
            'name': 'RKM-2 (User)',
            'role': 'user', 
            'phone': '+91-9876543210',
            'id': 'usr_rkm2_user'
        },
        {
            'email': 'rkm.ytw3@gmail.com',
            'name': 'RKM-3 (User)',
            'role': 'user',
            'phone': '+91-9876543211', 
            'id': 'usr_rkm3_user'
        },
        {
            'email': 'rkm.ytw4@gmail.com',
            'name': 'RKM-4 (User)',
            'role': 'user',
            'phone': '+91-9876543212',
            'id': 'usr_rkm4_user'
        }
    ]
    
    print("Updating user credentials...")
    
    for user_info in required_users:
        try:
            # Check if user already exists
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
                # Update existing user
                print(f"Updating existing user: {user_info['email']}")
                success = update_user(existing_user['id'], user_data)
                if success:
                    print(f"✓ Updated {user_info['email']}")
                else:
                    print(f"✗ Failed to update {user_info['email']}")
            else:
                # Create new user
                print(f"Creating new user: {user_info['email']}")
                user_data['id'] = user_info['id']
                user_id = add_user(user_data)
                if user_id:
                    print(f"✓ Created {user_info['email']} with ID: {user_id}")
                else:
                    print(f"✗ Failed to create {user_info['email']}")
                    
        except Exception as e:
            print(f"✗ Error processing {user_info['email']}: {e}")
    
    print("\nUser credential update complete!")

if __name__ == '__main__':
    update_user_credentials()