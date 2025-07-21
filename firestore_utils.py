#!/usr/bin/env python3
"""
Firestore utility functions for Apni Holidays
Replaces PostgreSQL database functions
"""
import os
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

# Global Firestore client
db = None

def init_firestore():
    """Initialize Firestore client with environment variables"""
    global db
    if db is not None:
        return db

    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate({
                "type": "service_account",
                "project_id": os.getenv("FIREBASE_PROJECT_ID"),
                "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
                "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
                "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
                "client_id": os.getenv("FIREBASE_CLIENT_ID"),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL")
            })
            firebase_admin.initialize_app(cred, {
                'projectId': os.getenv("FIREBASE_PROJECT_ID")
            })

        db = firestore.client()
        db.collection('test').limit(1).get()  # test query
        print("✅ Successfully connected to Firestore via environment variables")
        return db

    except Exception as e:
        print(f"⚠️ Firestore connection failed: {e}")
        print("🧪 Using mock Firestore for development/testing")
        from unittest.mock import Mock
        db = Mock()
        db._is_mock = True
        return db

def get_packages(featured_only=False, status='active'):
    """Get packages from Firestore or mock data fallback"""
    try:
        db = init_firestore()

        if hasattr(db, '_is_mock') or not hasattr(db, 'collection'):
            print("Using mock data for packages")
            from mock_data import PACKAGES
            packages = PACKAGES.copy()
            if status:
                packages = [p for p in packages if p.get('status') == status]
            if featured_only:
                packages = [p for p in packages if p.get('featured') is True]
            packages.sort(key=lambda x: x.get('created_at', datetime.now()), reverse=True)
            return packages
        else:
            query = db.collection('packages')
            if featured_only:
                query = query.where(filter=firestore.FieldFilter('featured', '==', True))
            elif status:
                query = query.where(filter=firestore.FieldFilter('status', '==', status))

            docs = query.stream()
            packages = []
            for doc in docs:
                data = doc.to_dict()
                data['id'] = doc.id
                packages.append(data)
            return packages

    except Exception as e:
        print(f"Error fetching packages: {e}")
        try:
            from mock_data import PACKAGES
            return [p for p in PACKAGES if (not status or p.get('status') == status) and (not featured_only or p.get('featured'))]
        except Exception as mock_error:
            print(f"Mock data also failed: {mock_error}")
            return []

def get_package_by_id(package_id):
    try:
        db = init_firestore()
        doc = db.collection('packages').document(package_id).get()
        if doc.exists:
            data = doc.to_dict()
            data['id'] = doc.id
            return data
        return None
    except Exception as e:
        print(f"Error fetching package {package_id}: {e}")
        return None

def add_package(package_data):
    try:
        db = init_firestore()
        if 'id' not in package_data:
            timestamp = int(datetime.now().timestamp())
            package_data['id'] = f"pkg_{package_data['destination'].lower().replace(' ', '_')}_{timestamp}"
        package_data['created_at'] = datetime.now()
        package_data['updated_at'] = datetime.now()
        db.collection('packages').document(package_data['id']).set(package_data)
        return package_data['id']
    except Exception as e:
        print(f"Error adding package: {e}")
        return None

def update_package(package_id, package_data):
    try:
        db = init_firestore()
        package_data['updated_at'] = datetime.now()
        db.collection('packages').document(package_id).update(package_data)
        return True
    except Exception as e:
        print(f"Error updating package {package_id}: {e}")
        return False

def delete_package(package_id):
    try:
        db = init_firestore()
        db.collection('packages').document(package_id).delete()
        return True
    except Exception as e:
        print(f"Error deleting package {package_id}: {e}")
        return False

def get_user_by_email(email):
    try:
        db = init_firestore()
        if hasattr(db, '_is_mock') or not hasattr(db, 'collection'):
            from mock_data import USERS
            for user in USERS:
                if user.get('email') == email:
                    return user.copy()
            return None
        query = db.collection('users').where(filter=firestore.FieldFilter('email', '==', email))
        docs = list(query.stream())
        if docs:
            data = docs[0].to_dict()
            data['id'] = docs[0].id
            return data
        return None
    except Exception as e:
        print(f"Error fetching user by email {email}: {e}")
        return None

def get_user_by_id(user_id):
    try:
        db = init_firestore()
        doc = db.collection('users').document(user_id).get()
        if doc.exists:
            data = doc.to_dict()
            data['id'] = doc.id
            return data
        return None
    except Exception as e:
        print(f"Error fetching user {user_id}: {e}")
        return None

def get_all_users():
    try:
        db = init_firestore()
        if hasattr(db, '_is_mock') or not hasattr(db, 'collection'):
            from mock_data import USERS
            return USERS.copy()
        docs = db.collection('users').stream()
        users = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            users.append(data)
        def safe_sort(user):
            d = user.get('created_at', datetime.min)
            try:
                from dateutil import parser
                return parser.parse(d) if isinstance(d, str) else d
            except:
                return datetime.min
        users.sort(key=safe_sort, reverse=True)
        return users
    except Exception as e:
        print(f"Error fetching users: {e}")
        return []

def add_user(user_data):
    try:
        db = init_firestore()
        if 'id' not in user_data:
            timestamp = int(datetime.now().timestamp())
            user_data['id'] = f"usr_{timestamp}"
        user_data['created_at'] = datetime.now()
        user_data['last_login'] = None
        db.collection('users').document(user_data['id']).set(user_data)
        return user_data['id']
    except Exception as e:
        print(f"Error adding user: {e}")
        return None

def update_user(user_id, user_data):
    try:
        db = init_firestore()
        db.collection('users').document(user_id).update(user_data)
        return True
    except Exception as e:
        print(f"Error updating user {user_id}: {e}")
        return False

def update_user_status(user_id, new_status):
    return update_user(user_id, {'status': new_status})

def delete_user(user_id):
    try:
        db = init_firestore()
        db.collection('users').document(user_id).delete()
        return True
    except Exception as e:
        print(f"Error deleting user {user_id}: {e}")
        return False

def authenticate_user(email, password):
    user = get_user_by_email(email)
    if user and user.get('password_hash') and check_password_hash(user['password_hash'], password):
        try:
            update_user(user['id'], {'last_login': datetime.now()})
        except Exception as e:
            print(f"Error updating last_login: {e}")
        return user
    elif user and user.get('password') and check_password_hash(user['password'], password):
        return user
    return None

def get_admin_users():
    try:
        db = init_firestore()
        docs = db.collection('users').where('role', '==', 'admin')\
            .order_by('created_at', direction=firestore.Query.DESCENDING).stream()
        admins = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            admins.append(data)
        return admins
    except Exception as e:
        print(f"Error fetching admin users: {e}")
        return []

def is_admin_user(email):
    user = get_user_by_email(email)
    return user and user.get('role') == 'admin' and user.get('status') == 'active'

def get_stats():
    try:
        db = init_firestore()
        packages_count = len(list(db.collection('packages').where('status', '==', 'active').stream()))
        users_count = len(list(db.collection('users').where('role', '==', 'user').stream()))
        featured_count = len(list(db.collection('packages').where('featured', '==', True).stream()))
        return {
            'packages': packages_count,
            'users': users_count,
            'featured': featured_count,
            'inquiries': 0
        }
    except Exception as e:
        print(f"Error fetching stats: {e}")
        return {'packages': 0, 'users': 0, 'featured': 0, 'inquiries': 0}
