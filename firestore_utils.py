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
                "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_CERT_URL")
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
        else:
            print("No Firebase credentials found, using mock data")
            raise Exception("No Firebase credentials available")
    except Exception as e:
        print(f"Firestore connection failed: {e}")
        # For development, fall back to mock data
        print("Using mock data for development")
        from unittest.mock import Mock
        db = Mock()
        db._is_mock = True  # Mark as mock for easier detection
        return db

def get_packages(featured_only=False, status='active'):
    """Get packages from Firestore or mock data fallback"""
    try:
        db = init_firestore()
        
        # Check if we have a real Firestore connection or using mock
        if hasattr(db, '_is_mock') or not hasattr(db, 'collection'):
            # Use mock data
            print("Using mock data for packages")
            from mock_data import PACKAGES
            packages = PACKAGES.copy()
            
            # Apply filters
            if status:
                packages = [p for p in packages if p.get('status') == status]
            if featured_only:
                packages = [p for p in packages if p.get('featured') == True]
            
            # Sort by created_at descending
            packages.sort(key=lambda x: x.get('created_at', datetime.now()), reverse=True)
            return packages
        else:
            # Real Firestore connection - simplified query to avoid index requirements
            query = db.collection('packages')
            
            # Apply only one filter at a time to avoid composite index requirements
            if featured_only:
                query = query.where(filter=firestore.FieldFilter('featured', '==', True))
            elif status:
                query = query.where(filter=firestore.FieldFilter('status', '==', status))
            
            docs = query.stream()
            
            packages = []
            for doc in docs:
                package_data = doc.to_dict()
                package_data['id'] = doc.id
                packages.append(package_data)
            
            return packages
            
    except Exception as e:
        print(f"Error fetching packages: {e}")
        # Final fallback to mock data
        try:
            from mock_data import PACKAGES
            filtered_packages = []
            for p in PACKAGES:
                if (not status or p.get('status') == status) and (not featured_only or p.get('featured')):
                    filtered_packages.append(p)
            return filtered_packages
        except Exception as mock_error:
            print(f"Mock data also failed: {mock_error}")
            return []

def get_package_by_id(package_id):
    """Get a single package by ID"""
    try:
        db = init_firestore()
        doc = db.collection('packages').document(package_id).get()
        
        if doc.exists:
            package_data = doc.to_dict()
            package_data['id'] = doc.id
            return package_data
        return None
    except Exception as e:
        print(f"Error fetching package {package_id}: {e}")
        return None

def add_package(package_data):
    """Add a new package to Firestore"""
    try:
        db = init_firestore()
        
        # Generate unique ID if not provided
        if 'id' not in package_data:
            timestamp = int(datetime.now().timestamp())
            package_data['id'] = f"pkg_{package_data['destination'].lower().replace(' ', '_')}_{timestamp}"
        
        package_data['created_at'] = datetime.now()
        package_data['updated_at'] = datetime.now()
        
        doc_ref = db.collection('packages').document(package_data['id'])
        doc_ref.set(package_data)
        
        return package_data['id']
    except Exception as e:
        print(f"Error adding package: {e}")
        return None

def update_package(package_id, package_data):
    """Update an existing package"""
    try:
        db = init_firestore()
        package_data['updated_at'] = datetime.now()
        
        doc_ref = db.collection('packages').document(package_id)
        doc_ref.update(package_data)
        
        return True
    except Exception as e:
        print(f"Error updating package {package_id}: {e}")
        return False

def delete_package(package_id):
    """Delete a package"""
    try:
        db = init_firestore()
        db.collection('packages').document(package_id).delete()
        return True
    except Exception as e:
        print(f"Error deleting package {package_id}: {e}")
        return False

def get_user_by_email(email):
    """Get user by email from Firestore or mock data fallback"""
    try:
        db = init_firestore()
        
        # Check if we have a real Firestore connection or using mock
        if hasattr(db, '_is_mock') or not hasattr(db, 'collection'):
            # Use mock data
            print(f"Using mock data to find user: {email}")
            from mock_data import USERS
            for user in USERS:
                if user.get('email') == email:
                    return user.copy()
            return None
        else:
            # Real Firestore connection
            query = db.collection('users').where(filter=firestore.FieldFilter('email', '==', email))
            docs = list(query.stream())
            
            if docs:
                user_data = docs[0].to_dict()
                user_data['id'] = docs[0].id
                return user_data
            return None
            
    except Exception as e:
        print(f"Error fetching user by email {email}: {e}")
        # Final fallback to mock data
        try:
            from mock_data import USERS
            for user in USERS:
                if user.get('email') == email:
                    return user.copy()
        except Exception as mock_error:
            print(f"Mock data also failed: {mock_error}")
        return None

def get_user_by_id(user_id):
    """Get user by ID"""
    try:
        db = init_firestore()
        doc = db.collection('users').document(user_id).get()
        
        if doc.exists:
            user_data = doc.to_dict()
            user_data['id'] = doc.id
            return user_data
        return None
    except Exception as e:
        print(f"Error fetching user {user_id}: {e}")
        return None

def get_all_users():
    """Get all users from Firestore or mock data fallback"""
    try:
        db = init_firestore()
        
        # Check if we have a real Firestore connection or using mock
        if hasattr(db, '_is_mock') or not hasattr(db, 'collection'):
            # Use mock data
            print("Using mock data for users")
            from mock_data import USERS
            return USERS.copy()
        else:
            # Real Firestore connection - avoid order_by due to mixed date types
            docs = db.collection('users').stream()
            
            users = []
            for doc in docs:
                user_data = doc.to_dict()
                user_data['id'] = doc.id
                users.append(user_data)
            
            # Sort in Python instead to handle mixed date types
            def safe_date_sort(user):
                date_val = user.get('created_at', datetime.min)
                if isinstance(date_val, str):
                    try:
                        from dateutil import parser
                        return parser.parse(date_val)
                    except:
                        return datetime.min
                elif hasattr(date_val, 'timestamp'):
                    return date_val
                else:
                    return datetime.min
            
            users.sort(key=safe_date_sort, reverse=True)
            return users
    except Exception as e:
        print(f"Error fetching users: {e}")
        # Final fallback to mock data
        try:
            from mock_data import USERS
            return USERS.copy()
        except Exception as mock_error:
            print(f"Mock data also failed: {mock_error}")
            return []

def add_user(user_data):
    """Add a new user"""
    try:
        db = init_firestore()
        
        # Generate unique ID if not provided
        if 'id' not in user_data:
            timestamp = int(datetime.now().timestamp())
            user_data['id'] = f"usr_{timestamp}"
        
        user_data['created_at'] = datetime.now()
        user_data['last_login'] = None
        
        doc_ref = db.collection('users').document(user_data['id'])
        doc_ref.set(user_data)
        
        return user_data['id']
    except Exception as e:
        print(f"Error adding user: {e}")
        return None

def create_user(user_data):
    """Create a new user - alias for add_user"""
    return add_user(user_data)

def update_user_data(user_id, user_data):
    """Update user data - alias for update_user with data parameter"""
    return update_user(user_id, user_data)

def update_user(user_id, user_data):
    """Update user data"""
    try:
        db = init_firestore()
        doc_ref = db.collection('users').document(user_id)
        doc_ref.update(user_data)
        return True
    except Exception as e:
        print(f"Error updating user {user_id}: {e}")
        return False

def update_user_status(user_id, new_status):
    """Update user status"""
    try:
        db = init_firestore()
        doc_ref = db.collection('users').document(user_id)
        doc_ref.update({'status': new_status})
        return True
    except Exception as e:
        print(f"Error updating user status {user_id}: {e}")
        return False

def delete_user(user_id):
    """Delete a user"""
    try:
        db = init_firestore()
        db.collection('users').document(user_id).delete()
        return True
    except Exception as e:
        print(f"Error deleting user {user_id}: {e}")
        return False

def authenticate_user(email, password):
    """Authenticate user with email and password"""
    user = get_user_by_email(email)
    if user and user.get('password_hash') and check_password_hash(user['password_hash'], password):
        # Update last_login in Firestore
        try:
            update_user(user['id'], {'last_login': datetime.now()})
        except Exception as e:
            print(f"Error updating last_login: {e}")
        return user
    # Fallback: check if password field exists (backward compatibility)
    elif user and user.get('password') and check_password_hash(user['password'], password):
        return user
    return None

def get_admin_users():
    """Get all admin users"""
    try:
        db = init_firestore()
        query = db.collection('users').where('role', '==', 'admin')
        docs = query.order_by('created_at', direction=firestore.Query.DESCENDING).stream()
        
        admins = []
        for doc in docs:
            admin_data = doc.to_dict()
            admin_data['id'] = doc.id
            admins.append(admin_data)
        
        return admins
    except Exception as e:
        print(f"Error fetching admin users: {e}")
        return []

def is_admin_user(email):
    """Check if user is admin"""
    user = get_user_by_email(email)
    return user and user.get('role') == 'admin' and user.get('status') == 'active'



def add_package(package_data):
    """Add a new package to Firestore"""
    try:
        db = init_firestore()
        package_id = package_data.get('id')
        if package_id:
            # Use the provided ID as document ID
            db.collection('packages').document(package_id).set(package_data)
            print(f"Package created with ID: {package_id}")
        else:
            # Auto-generate ID
            doc_ref = db.collection('packages').add(package_data)
            print(f"Package created with ID: {doc_ref[1].id}")
        return True
    except Exception as e:
        print(f"Error adding package: {e}")
        return False

def delete_package(package_id):
    """Delete a package from Firestore"""
    try:
        db = init_firestore()
        db.collection('packages').document(package_id).delete()
        print(f"Package {package_id} deleted successfully")
        return True
    except Exception as e:
        print(f"Error deleting package {package_id}: {e}")
        return False

def update_package(package_id, package_data):
    """Update a package in Firestore"""
    try:
        db = init_firestore()
        doc_ref = db.collection('packages').document(package_id)
        doc_ref.update(package_data)
        print(f"Package {package_id} updated successfully")
        return True
    except Exception as e:
        print(f"Error updating package {package_id}: {e}")
        return False

def get_stats():
    """Get dashboard statistics"""
    try:
        db = init_firestore()
        
        # Count packages
        packages_count = len(list(db.collection('packages').where('status', '==', 'active').stream()))
        
        # Count users
        users_count = len(list(db.collection('users').where('role', '==', 'user').stream()))
        
        # Count featured packages
        featured_count = len(list(db.collection('packages').where('featured', '==', True).stream()))
        
        return {
            'packages': packages_count,
            'users': users_count,
            'featured': featured_count,
            'inquiries': 0  # Placeholder for now
        }
    except Exception as e:
        print(f"Error fetching stats: {e}")
        return {'packages': 0, 'users': 0, 'featured': 0, 'inquiries': 0}
