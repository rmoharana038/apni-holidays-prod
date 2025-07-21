import os
from dotenv import load_dotenv  # ✅ New: loads .env
load_dotenv()

import subprocess
import json
from flask import Flask, render_template_string, request, jsonify, redirect, url_for
from datetime import datetime
from firestore_utils import (
    get_packages, get_package_by_id, add_package, update_package, delete_package,
    get_user_by_email, get_user_by_id, get_all_users, add_user, update_user, delete_user,
    authenticate_user, get_admin_users, is_admin_user, get_stats
)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "apni-holidays-secret-key-2025")

# ✅ Firebase configuration via .env
FIREBASE_CONFIG = {
    "apiKey": os.environ.get("FIREBASE_API_KEY"),
    "authDomain": os.environ.get("FIREBASE_AUTH_DOMAIN"),
    "projectId": os.environ.get("FIREBASE_PROJECT_ID"),
    "storageBucket": os.environ.get("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.environ.get("FIREBASE_SENDER_ID"),
    "appId": os.environ.get("FIREBASE_APP_ID"),
    "measurementId": os.environ.get("FIREBASE_MEASUREMENT_ID")
}

# Database is now handled by Firestore
# Legacy function maintained for compatibility
def get_db_connection():
    """Legacy function - now using Firestore"""
    return None

@app.route('/')
def index():
    """Homepage with featured packages"""
    try:
        # Get featured packages from Firestore
        packages = get_packages(featured_only=True)[:6]  # Limit to 6 packages
    except Exception as e:
        print(f"Error fetching packages: {e}")
        packages = []
    
    # Check if user is logged in and if they are admin
    from flask import session
    user_logged_in = session.get('user_id') is not None
    user_name = session.get('user_name', 'Guest')
    
    # Check if user is admin using Firestore
    user_is_admin = session.get('is_admin', False)
    if not user_is_admin and user_logged_in:
        user_email = session.get('user_email', '')
        try:
            user = get_user_by_email(user_email)
            if user and user.get('role') == 'admin':
                user_is_admin = True
                session['is_admin'] = True
        except Exception as e:
            print(f"Admin check error: {e}")
            user_is_admin = False
    
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Apni Holidays - Discover Your Dream Destination</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        .hero-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 70vh;
        }
        .hero-background {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('https://images.unsplash.com/photo-1469474968028-56623f02e42e?auto=format&fit=crop&w=1920&q=80') center/cover;
            opacity: 0.3;
        }
        .package-card {
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border: none;
            border-radius: 15px;
            overflow: hidden;
        }
        .package-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        .package-image {
            height: 250px;
            object-fit: cover;
        }
        .price-badge {
            position: absolute;
            top: 15px;
            right: 15px;
            background: linear-gradient(45deg, #ff6b6b, #ffa500);
            color: white;
            padding: 8px 15px;
            border-radius: 25px;
            font-weight: bold;
        }
        .discount-price {
            text-decoration: line-through;
            color: #999;
            font-size: 0.9em;
        }
        .search-form {
            backdrop-filter: blur(10px);
            background: rgba(255, 255, 255, 0.95);
        }
        .navbar {
            backdrop-filter: blur(10px);
            background: rgba(255, 255, 255, 0.95) !important;
        }
        .footer {
            background: #2c3e50;
            color: white;
            padding: 40px 0 20px;
        }
        .animate-fade-in {
            animation: fadeIn 1s ease-in;
        }
        .animate-slide-up {
            animation: slideUp 1s ease-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(50px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-light fixed-top">
        <div class="container">
            <a class="navbar-brand fw-bold" href="/">
                <i class="fas fa-plane text-primary"></i> Apni Holidays
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="/">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/packages">Packages</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/contact">Contact</a>
                    </li>
                </ul>
                <ul class="navbar-nav">
                    {% if user_logged_in %}
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown">
                            <i class="fas fa-user me-1"></i>{{ user_name }}
                        </a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="/profile"><i class="fas fa-user me-2"></i>My Profile</a></li>
                            <li><a class="dropdown-item" href="/my-bookings"><i class="fas fa-suitcase me-2"></i>My Bookings</a></li>
                            {% if user_is_admin %}
                            <li><hr class="dropdown-divider"></li>
                            <li><a class="dropdown-item" href="/admin/dashboard"><i class="fas fa-cog me-2"></i>Admin Panel</a></li>
                            {% endif %}
                            <li><hr class="dropdown-divider"></li>
                            <li><a class="dropdown-item" href="/auth/logout"><i class="fas fa-sign-out-alt me-2"></i>Logout</a></li>
                        </ul>
                    </li>
                    {% else %}
                    <li class="nav-item">
                        <a class="nav-link" href="/auth/login">Login</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link btn btn-primary text-white px-3 ms-2" href="/auth/register">Sign Up</a>
                    </li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero-section text-white position-relative overflow-hidden">
        <div class="hero-background"></div>
        <div class="container position-relative" style="z-index: 2; padding-top: 100px;">
            <div class="row align-items-center min-vh-75">
                <div class="col-lg-6">
                    <h1 class="display-4 fw-bold mb-4 animate-fade-in">
                        Discover Your <br>
                        <span class="text-warning">Dream Destination</span>
                    </h1>
                    <p class="lead mb-4 animate-fade-in">
                        Explore Thailand, Dubai, Bali, Singapore, Maldives, Turkey & more amazing destinations from India
                    </p>
                    
                    <!-- Search Form -->
                    <div class="search-form rounded-3 p-4 shadow-lg animate-slide-up">
                        <form method="GET" action="/packages" class="row g-3">
                            <div class="col-md-4">
                                <label class="form-label text-dark">Destination</label>
                                <select name="destination" class="form-select">
                                    <option value="">Any Destination</option>
                                    <option value="thailand">Thailand</option>
                                    <option value="dubai">Dubai</option>
                                    <option value="bali">Bali</option>
                                    <option value="singapore">Singapore</option>
                                    <option value="maldives">Maldives</option>
                                    <option value="turkey">Turkey</option>
                                </select>
                            </div>
                            <div class="col-md-4">
                                <label class="form-label text-dark">Duration</label>
                                <select name="duration" class="form-select">
                                    <option value="">Any Duration</option>
                                    <option value="3-5">3–5 Days</option>
                                    <option value="6-10">6–10 Days</option>
                                    <option value="10+">10+ Days</option>
                                </select>
                            </div>
                            <div class="col-md-4">
                                <label class="form-label text-dark">Budget</label>
                                <select name="budget" class="form-select">
                                    <option value="">Any Budget</option>
                                    <option value="under-50k">Under ₹50,000</option>
                                    <option value="50k-1l">₹50k–₹1L</option>
                                    <option value="1l+">₹1L+</option>
                                </select>
                            </div>
                            <div class="col-12">
                                <button type="submit" class="btn btn-primary btn-lg px-4">
                                    <i class="fas fa-search me-2"></i>Search Packages
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Featured Packages Section -->
    <section class="py-5" style="margin-top: 80px;">
        <div class="container">
            <div class="text-center mb-5">
                <h2 class="display-5 fw-bold">Featured Travel Packages</h2>
                <p class="lead text-muted">Handpicked destinations for unforgettable experiences</p>
            </div>

            {% if packages %}
            <div class="row g-4">
                {% for package in packages %}
                <div class="col-lg-4 col-md-6">
                    <div class="card package-card h-100 shadow-sm">
                        <div class="position-relative">
                            <img src="{{ package.image_url }}" class="card-img-top package-image" alt="{{ package.title }}">
                            <div class="price-badge">
                                {% if package.discount_price %}
                                    <div class="discount-price">₹{{ "{:,.0f}".format(package.price) }}</div>
                                    <div>₹{{ "{:,.0f}".format(package.discount_price) }}</div>
                                {% else %}
                                    <div>₹{{ "{:,.0f}".format(package.price) }}</div>
                                {% endif %}
                            </div>
                        </div>
                        <div class="card-body d-flex flex-column">
                            <h5 class="card-title">{{ package.title }}</h5>
                            <p class="text-muted mb-2">
                                <i class="fas fa-map-marker-alt me-1"></i>{{ package.destination }}
                                <i class="fas fa-calendar-alt ms-3 me-1"></i>{{ package.days }} Days
                            </p>
                            <p class="card-text flex-grow-1">{{ package.description[:120] }}{% if package.description|length > 120 %}...{% endif %}</p>
                            <div class="mt-auto">
                                <a href="/package-details?id={{ package.id }}" class="btn btn-primary w-100">
                                    <i class="fas fa-eye me-2"></i>View Details
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
            {% else %}
            <div class="text-center py-5">
                <i class="fas fa-plane fa-3x text-muted mb-3"></i>
                <h4>No packages available at the moment</h4>
                <p class="text-muted">Please check back later for exciting travel packages!</p>
            </div>
            {% endif %}

            <div class="text-center mt-5">
                <a href="/packages" class="btn btn-outline-primary btn-lg">
                    <i class="fas fa-list me-2"></i>View All Packages
                </a>
            </div>
        </div>
    </section>

    <!-- Why Choose Us Section -->
    <section class="py-5 bg-light">
        <div class="container">
            <div class="text-center mb-5">
                <h2 class="display-6 fw-bold">Why Choose Apni Holidays?</h2>
            </div>
            <div class="row g-4">
                <div class="col-lg-3 col-md-6 text-center">
                    <div class="p-4">
                        <i class="fas fa-shield-alt fa-3x text-primary mb-3"></i>
                        <h5>Trusted & Reliable</h5>
                        <p class="text-muted">Over 1000+ satisfied customers with excellent reviews</p>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6 text-center">
                    <div class="p-4">
                        <i class="fas fa-tags fa-3x text-primary mb-3"></i>
                        <h5>Best Prices</h5>
                        <p class="text-muted">Competitive pricing with exclusive deals and discounts</p>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6 text-center">
                    <div class="p-4">
                        <i class="fas fa-headset fa-3x text-primary mb-3"></i>
                        <h5>24/7 Support</h5>
                        <p class="text-muted">Round-the-clock customer support for hassle-free travel</p>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6 text-center">
                    <div class="p-4">
                        <i class="fas fa-globe fa-3x text-primary mb-3"></i>
                        <h5>Global Destinations</h5>
                        <p class="text-muted">Handpicked destinations across the world</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="row">
                <div class="col-lg-4 mb-4">
                    <h5 class="fw-bold mb-3">
                        <i class="fas fa-plane me-2"></i>Apni Holidays
                    </h5>
                    <p class="mb-3">Your trusted travel partner for unforgettable journeys across the globe. Creating memories that last a lifetime.</p>
                    <div class="social-links">
                        <a href="#" class="text-white me-3"><i class="fab fa-facebook-f"></i></a>
                        <a href="#" class="text-white me-3"><i class="fab fa-instagram"></i></a>
                        <a href="#" class="text-white me-3"><i class="fab fa-twitter"></i></a>
                        <a href="#" class="text-white"><i class="fab fa-youtube"></i></a>
                    </div>
                </div>
                <div class="col-lg-2 col-md-6 mb-4">
                    <h6 class="fw-bold mb-3">Quick Links</h6>
                    <ul class="list-unstyled">
                        <li><a href="/" class="text-white-50">Home</a></li>
                        <li><a href="/packages" class="text-white-50">Packages</a></li>
                        <li><a href="/contact" class="text-white-50">Contact</a></li>
                        <li><a href="/about" class="text-white-50">About Us</a></li>
                    </ul>
                </div>
                <div class="col-lg-3 col-md-6 mb-4">
                    <h6 class="fw-bold mb-3">Popular Destinations</h6>
                    <ul class="list-unstyled">
                        <li><a href="/packages?destination=thailand" class="text-white-50">Thailand</a></li>
                        <li><a href="/packages?destination=dubai" class="text-white-50">Dubai</a></li>
                        <li><a href="/packages?destination=bali" class="text-white-50">Bali</a></li>
                        <li><a href="/packages?destination=singapore" class="text-white-50">Singapore</a></li>
                    </ul>
                </div>
                <div class="col-lg-3 mb-4">
                    <h6 class="fw-bold mb-3">Contact Info</h6>
                    <ul class="list-unstyled">
                        <li class="mb-2"><i class="fas fa-envelope me-2"></i>info@apniholidays.com</li>
                        <li class="mb-2"><i class="fas fa-phone me-2"></i>+91 99999 99999</li>
                        <li><i class="fas fa-map-marker-alt me-2"></i>Mumbai, India</li>
                    </ul>
                </div>
            </div>
            <hr class="my-4">
            <div class="text-center">
                <p class="mb-0">&copy; 2025 Apni Holidays. All rights reserved. | Designed for GoDaddy Hosting</p>
            </div>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
    """, packages=packages, user_logged_in=user_logged_in, user_name=user_name, user_is_admin=user_is_admin)

@app.route('/packages')
def packages():
    """Package listing page with filters"""
    destination = request.args.get('destination', '')
    duration = request.args.get('duration', '')
    budget = request.args.get('budget', '')
    search = request.args.get('search', '')
    
    try:
        # Get packages from Firestore with filters
        all_packages = get_packages()
        packages = []
        
        for pkg in all_packages:
            # Apply filters
            if destination and destination.lower() not in pkg.get('destination', '').lower():
                continue
                
            days = pkg.get('days', 0)
            if duration:
                if duration == '3-5' and not (3 <= days <= 5):
                    continue
                elif duration == '6-10' and not (6 <= days <= 10):
                    continue
                elif duration == '10+' and days <= 10:
                    continue
            
            price = pkg.get('discount_price') or pkg.get('price', 0)
            if budget:
                if budget == 'under-50k' and price >= 50000:
                    continue
                elif budget == '50k-1l' and not (50000 <= price <= 100000):
                    continue
                elif budget == '1l+' and price <= 100000:
                    continue
            
            if search:
                search_lower = search.lower()
                title = pkg.get('title', '').lower()
                dest = pkg.get('destination', '').lower() 
                desc = pkg.get('description', '').lower()
                if not (search_lower in title or search_lower in dest or search_lower in desc):
                    continue
                    
            packages.append(pkg)
        
        # Sort by featured first, then by created_at
        packages.sort(key=lambda x: (not x.get('featured', False), x.get('created_at', datetime.min)))
        
    except Exception as e:
        print(f"Error fetching packages: {e}")
        packages = []
    
    # Check if user is logged in and if they are admin
    from flask import session
    user_logged_in = session.get('user_id') is not None
    user_name = session.get('user_name', 'Guest')
    
    # Check if user is admin using Firestore
    user_is_admin = session.get('is_admin', False)
    if not user_is_admin and user_logged_in:
        user_email = session.get('user_email', '')
        try:
            user = get_user_by_email(user_email)
            if user and user.get('role') == 'admin':
                user_is_admin = True
                session['is_admin'] = True
        except Exception as e:
            print(f"Admin check error: {e}")
            user_is_admin = False
    
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Travel Packages - Apni Holidays</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        .package-card {
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border: none;
            border-radius: 15px;
            overflow: hidden;
        }
        .package-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        }
        .package-image {
            height: 250px;
            object-fit: cover;
        }
        .price-badge {
            position: absolute;
            top: 15px;
            right: 15px;
            background: linear-gradient(45deg, #ff6b6b, #ffa500);
            color: white;
            padding: 8px 15px;
            border-radius: 25px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
        <div class="container">
            <a class="navbar-brand fw-bold" href="/">
                <i class="fas fa-plane text-primary"></i> Apni Holidays
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="/">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link active" href="/packages">Packages</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/contact">Contact</a>
                    </li>
                </ul>
                <ul class="navbar-nav">
                    {% if user_logged_in %}
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown">
                            <i class="fas fa-user me-1"></i>{{ user_name }}
                        </a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="/profile"><i class="fas fa-user me-2"></i>My Profile</a></li>
                            <li><a class="dropdown-item" href="/my-bookings"><i class="fas fa-suitcase me-2"></i>My Bookings</a></li>
                            {% if user_is_admin %}
                            <li><hr class="dropdown-divider"></li>
                            <li><a class="dropdown-item" href="/admin/dashboard"><i class="fas fa-cog me-2"></i>Admin Panel</a></li>
                            {% endif %}
                            <li><hr class="dropdown-divider"></li>
                            <li><a class="dropdown-item" href="/auth/logout"><i class="fas fa-sign-out-alt me-2"></i>Logout</a></li>
                        </ul>
                    </li>
                    {% else %}
                    <li class="nav-item">
                        <a class="nav-link" href="/auth/login">Login</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link btn btn-primary text-white px-3 ms-2" href="/auth/register">Sign Up</a>
                    </li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>

    <!-- Page Header -->
    <section class="bg-primary text-white py-5">
        <div class="container">
            <div class="row">
                <div class="col-lg-8">
                    <h1 class="display-5 fw-bold mb-3">Travel Packages</h1>
                    <p class="lead">Discover amazing destinations with our carefully curated travel packages</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Filters Section -->
    <section class="py-4 bg-light border-bottom">
        <div class="container">
            <form method="GET" class="row g-3 align-items-end">
                <div class="col-lg-2 col-md-6">
                    <label class="form-label fw-bold">Search</label>
                    <input type="text" name="search" class="form-control" 
                           value="{{ search }}" placeholder="Search packages...">
                </div>
                
                <div class="col-lg-2 col-md-6">
                    <label class="form-label fw-bold">Destination</label>
                    <select name="destination" class="form-select">
                        <option value="">All Destinations</option>
                        <option value="thailand" {% if destination == 'thailand' %}selected{% endif %}>Thailand</option>
                        <option value="dubai" {% if destination == 'dubai' %}selected{% endif %}>Dubai</option>
                        <option value="bali" {% if destination == 'bali' %}selected{% endif %}>Bali</option>
                        <option value="singapore" {% if destination == 'singapore' %}selected{% endif %}>Singapore</option>
                        <option value="maldives" {% if destination == 'maldives' %}selected{% endif %}>Maldives</option>
                        <option value="turkey" {% if destination == 'turkey' %}selected{% endif %}>Turkey</option>
                    </select>
                </div>
                
                <div class="col-lg-2 col-md-6">
                    <label class="form-label fw-bold">Duration</label>
                    <select name="duration" class="form-select">
                        <option value="">Any Duration</option>
                        <option value="3-5" {% if duration == '3-5' %}selected{% endif %}>3–5 Days</option>
                        <option value="6-10" {% if duration == '6-10' %}selected{% endif %}>6–10 Days</option>
                        <option value="10+" {% if duration == '10+' %}selected{% endif %}>10+ Days</option>
                    </select>
                </div>
                
                <div class="col-lg-2 col-md-6">
                    <label class="form-label fw-bold">Budget</label>
                    <select name="budget" class="form-select">
                        <option value="">Any Budget</option>
                        <option value="under-50k" {% if budget == 'under-50k' %}selected{% endif %}>Under ₹50,000</option>
                        <option value="50k-1l" {% if budget == '50k-1l' %}selected{% endif %}>₹50k–₹1L</option>
                        <option value="1l+" {% if budget == '1l+' %}selected{% endif %}>₹1L+</option>
                    </select>
                </div>
                
                <div class="col-lg-2 col-md-6">
                    <button type="submit" class="btn btn-primary w-100">
                        <i class="fas fa-filter me-1"></i>Filter
                    </button>
                </div>
                
                <div class="col-lg-2 col-md-6">
                    <a href="/packages" class="btn btn-outline-secondary w-100">
                        <i class="fas fa-times me-1"></i>Clear
                    </a>
                </div>
            </form>
        </div>
    </section>

    <!-- Packages Grid -->
    <section class="py-5">
        <div class="container">
            {% if packages %}
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h4 class="mb-0">{{ packages|length }} Package(s) Found</h4>
                    <small class="text-muted">Showing results for your search</small>
                </div>
                
                <div class="row g-4">
                    {% for package in packages %}
                        <div class="col-lg-4 col-md-6">
                            <div class="card package-card h-100 shadow-sm">
                                <div class="position-relative">
                                    <img src="{{ package.image_url or '/assets/images/placeholder-package.jpg' }}" 
                                         class="card-img-top package-image" 
                                         alt="{{ package.title }}">
                                    <div class="position-absolute top-0 start-0 m-3">
                                        <span class="badge bg-warning text-dark">{{ package.days }} Days</span>
                                        {% if package.featured %}
                                        <span class="badge bg-primary ms-1">
                                            <i class="fas fa-star me-1"></i>Featured
                                        </span>
                                        {% endif %}
                                    </div>
                                    {% if package.discount_price and package.discount_price < package.price %}
                                        <div class="price-badge">
                                            {{ "{:.0f}".format((package.price - package.discount_price) / package.price * 100) }}% OFF
                                        </div>
                                    {% endif %}
                                </div>
                                
                                <div class="card-body d-flex flex-column">
                                    <h5 class="card-title fw-bold">{{ package.title }}</h5>
                                    <p class="text-muted small mb-2">
                                        <i class="fas fa-map-marker-alt text-primary me-1"></i>{{ package.destination }}
                                    </p>
                                    
                                    <p class="card-text flex-grow-1">
                                        {{ package.description[:120] }}{% if package.description|length > 120 %}...{% endif %}
                                    </p>
                                    
                                    <div class="d-flex align-items-center justify-content-between mt-auto">
                                        <div class="price">
                                            {% if package.discount_price and package.discount_price < package.price %}
                                                <span class="h5 fw-bold text-primary mb-0">₹{{ "{:,.0f}".format(package.discount_price) }}</span>
                                                <span class="text-decoration-line-through text-muted ms-2 small">₹{{ "{:,.0f}".format(package.price) }}</span>
                                            {% else %}
                                                <span class="h5 fw-bold text-primary mb-0">₹{{ "{:,.0f}".format(package.price) }}</span>
                                            {% endif %}
                                            <div class="small text-muted">per person</div>
                                        </div>
                                        <a href="/package/{{ package.id }}" class="btn btn-outline-primary">
                                            View Details
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    {% endfor %}
                </div>
                
            {% else %}
                <div class="text-center py-5">
                    <i class="fas fa-search display-4 text-muted mb-3"></i>
                    <h4 class="text-muted">No packages found</h4>
                    <p class="text-muted mb-4">Try adjusting your search filters or browse all packages</p>
                    <a href="/packages" class="btn btn-primary">View All Packages</a>
                </div>
            {% endif %}
        </div>
    </section>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
    """, packages=packages, destination=destination, duration=duration, budget=budget, search=search, 
         user_logged_in=user_logged_in, user_name=user_name, user_is_admin=user_is_admin)

@app.route('/package-details')
@app.route('/package/<package_id>')
def package_details(package_id=None):
    """Package details page"""
    if not package_id:
        package_id = request.args.get('id')
    
    if not package_id:
        return redirect(url_for('packages'))
    
    try:
        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, title, destination, days, price, discount_price, 
                       description, highlights, inclusions, exclusions, 
                       itinerary, image_url 
                FROM packages 
                WHERE id = %s AND status = 'active'
            """, (package_id,))
            package = cur.fetchone()
            cur.close()
            conn.close()
        else:
            package = None
    except Exception as e:
        print(f"Error fetching package: {e}")
        package = None
    
    if not package:
        return redirect(url_for('packages'))
    
    pkg_data = {
        'id': package[0],
        'title': package[1],
        'destination': package[2],
        'days': package[3],
        'price': package[4],
        'discount_price': package[5],
        'description': package[6],
        'highlights': package[7],
        'inclusions': package[8],
        'exclusions': package[9],
        'itinerary': package[10],
        'image_url': package[11]
    }
    
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ package.title }} - Apni Holidays</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        .package-hero {
            height: 60vh;
            background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), url('{{ package.image_url }}');
            background-size: cover;
            background-position: center;
        }
        .price-card {
            position: sticky;
            top: 100px;
        }
        .feature-list li {
            padding: 8px 0;
            border-bottom: 1px solid #eee;
        }
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
        <div class="container">
            <a class="navbar-brand fw-bold" href="/">
                <i class="fas fa-plane text-primary"></i> Apni Holidays
            </a>
            <div class="navbar-nav">
                <a class="nav-link" href="/">Home</a>
                <a class="nav-link" href="/packages">Packages</a>
                <a class="nav-link" href="/contact">Contact</a>
            </div>
        </div>
    </nav>

    <!-- Package Hero -->
    <section class="package-hero d-flex align-items-center text-white">
        <div class="container">
            <div class="row">
                <div class="col-lg-8">
                    <h1 class="display-4 fw-bold mb-3">{{ package.title }}</h1>
                    <p class="lead mb-4">
                        <i class="fas fa-map-marker-alt me-2"></i>{{ package.destination }}
                        <i class="fas fa-calendar-alt ms-4 me-2"></i>{{ package.days }} Days
                    </p>
                </div>
            </div>
        </div>
    </section>

    <div class="container my-5">
        <div class="row">
            <!-- Package Details -->
            <div class="col-lg-8">
                <div class="card shadow-sm mb-4">
                    <div class="card-body">
                        <h3 class="card-title">Package Overview</h3>
                        <p class="lead">{{ package.description }}</p>
                    </div>
                </div>

                {% if package.highlights %}
                <div class="card shadow-sm mb-4">
                    <div class="card-body">
                        <h4 class="card-title">Highlights</h4>
                        <ul class="feature-list list-unstyled">
                            {% for highlight in package.highlights.split(',') %}
                            <li><i class="fas fa-check text-success me-2"></i>{{ highlight.strip() }}</li>
                            {% endfor %}
                        </ul>
                    </div>
                </div>
                {% endif %}

                {% if package.inclusions %}
                <div class="card shadow-sm mb-4">
                    <div class="card-body">
                        <h4 class="card-title">What's Included</h4>
                        <ul class="feature-list list-unstyled">
                            {% for inclusion in package.inclusions.split(',') %}
                            <li><i class="fas fa-plus text-success me-2"></i>{{ inclusion.strip() }}</li>
                            {% endfor %}
                        </ul>
                    </div>
                </div>
                {% endif %}

                {% if package.exclusions %}
                <div class="card shadow-sm mb-4">
                    <div class="card-body">
                        <h4 class="card-title">What's Not Included</h4>
                        <ul class="feature-list list-unstyled">
                            {% for exclusion in package.exclusions.split(',') %}
                            <li><i class="fas fa-minus text-danger me-2"></i>{{ exclusion.strip() }}</li>
                            {% endfor %}
                        </ul>
                    </div>
                </div>
                {% endif %}

                {% if package.itinerary %}
                <div class="card shadow-sm mb-4">
                    <div class="card-body">
                        <h4 class="card-title">Detailed Itinerary</h4>
                        <div class="itinerary-content">
                            {% for day in package.itinerary.split('\n') %}
                            {% if day.strip() %}
                            <div class="mb-3 p-3 bg-light rounded">
                                <p class="mb-0">{{ day.strip() }}</p>
                            </div>
                            {% endif %}
                            {% endfor %}
                        </div>
                    </div>
                </div>
                {% endif %}
            </div>

            <!-- Booking Sidebar -->
            <div class="col-lg-4">
                <div class="card shadow price-card">
                    <div class="card-body">
                        <div class="text-center mb-4">
                            {% if package.discount_price and package.discount_price < package.price %}
                                <div class="h2 text-primary fw-bold">₹{{ "{:,.0f}".format(package.discount_price) }}</div>
                                <div class="text-decoration-line-through text-muted">₹{{ "{:,.0f}".format(package.price) }}</div>
                                <div class="badge bg-danger">{{ "{:.0f}".format((package.price - package.discount_price) / package.price * 100) }}% OFF</div>
                            {% else %}
                                <div class="h2 text-primary fw-bold">₹{{ "{:,.0f}".format(package.price) }}</div>
                            {% endif %}
                            <div class="text-muted">per person</div>
                        </div>

                        <form id="bookingForm" action="/booking" method="POST" class="needs-validation" novalidate>
                            <input type="hidden" name="package_id" value="{{ package.id }}">
                            
                            <div class="mb-3">
                                <label class="form-label">Travel Date</label>
                                <input type="date" class="form-control" name="travel_date" required min="{{ today() }}">
                            </div>
                            
                            <div class="mb-3">
                                <label class="form-label">Number of Travelers</label>
                                <select class="form-select" name="travelers" required>
                                    <option value="">Select travelers</option>
                                    {% for i in range(1, 11) %}
                                    <option value="{{ i }}">{{ i }} {{ 'Person' if i == 1 else 'People' }}</option>
                                    {% endfor %}
                                </select>
                            </div>
                            
                            <div class="mb-3">
                                <label class="form-label">Full Name</label>
                                <input type="text" class="form-control" name="name" placeholder="Enter full name" required>
                            </div>
                            
                            <div class="mb-3">
                                <label class="form-label">Email</label>
                                <input type="email" class="form-control" name="email" placeholder="Enter email" required>
                            </div>
                            
                            <div class="mb-4">
                                <label class="form-label">Phone</label>
                                <input type="tel" class="form-control" name="phone" placeholder="Enter phone number" required>
                            </div>
                            
                            <button type="submit" class="btn btn-primary w-100 btn-lg">
                                <i class="fas fa-credit-card me-2"></i>Book Now
                            </button>
                        </form>
                        
                        <div class="text-center mt-3">
                            <small class="text-muted">
                                <i class="fas fa-shield-alt me-1"></i>Secure booking process
                            </small>
                        </div>
                    </div>
                </div>

                <!-- Contact Info -->
                <div class="card shadow mt-4">
                    <div class="card-body text-center">
                        <h5>Need Help?</h5>
                        <p class="text-muted">Our travel experts are here to help</p>
                        <div class="d-grid gap-2">
                            <a href="tel:+919999999999" class="btn btn-outline-primary">
                                <i class="fas fa-phone me-2"></i>Call Us
                            </a>
                            <a href="https://wa.me/919999999999" class="btn btn-outline-success">
                                <i class="fab fa-whatsapp me-2"></i>WhatsApp
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
    document.getElementById('bookingForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        
        try {
            const response = await fetch('/booking', {
                method: 'POST',
                body: formData
            });
            const result = await response.json();
            
            if (result.status === 'success') {
                alert('Booking submitted successfully! Booking ID: ' + result.booking_id + '. Total amount: ₹' + result.total_amount.toLocaleString());
                this.reset();
            } else {
                alert('Booking failed: ' + result.message);
            }
        } catch (error) {
            alert('Failed to submit booking. Please try again.');
        }
    });
    </script>
</body>
</html>
    """, package=pkg_data, today=lambda: datetime.now().strftime('%Y-%m-%d'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page"""
    if request.method == 'POST':
        # Handle contact form submission
        name = request.form.get('name', '')
        email = request.form.get('email', '')
        phone = request.form.get('phone', '')
        subject = request.form.get('subject', '')
        message = request.form.get('message', '')
        package_id = request.form.get('package_id', '')
        
        try:
            conn = get_db_connection()
            if conn:
                cur = conn.cursor()
                inquiry_id = f"inq_{int(datetime.now().timestamp())}"
                cur.execute("""
                    INSERT INTO inquiries (id, name, email, phone, subject, message, package_id, status, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, 'new', %s)
                """, (inquiry_id, name, email, phone, subject, message, package_id or None, datetime.now()))
                conn.commit()
                cur.close()
                conn.close()
                
                return jsonify({'status': 'success', 'message': 'Thank you! Your inquiry has been submitted successfully.'})
            else:
                return jsonify({'status': 'error', 'message': 'Database connection failed'})
        except Exception as e:
            print(f"Contact form error: {e}")
            return jsonify({'status': 'error', 'message': 'Failed to submit inquiry. Please try again.'})
    
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact Us - Apni Holidays</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
        <div class="container">
            <a class="navbar-brand fw-bold" href="/">
                <i class="fas fa-plane text-primary"></i> Apni Holidays
            </a>
            <div class="navbar-nav">
                <a class="nav-link" href="/">Home</a>
                <a class="nav-link" href="/packages">Packages</a>
                <a class="nav-link active" href="/contact">Contact</a>
            </div>
        </div>
    </nav>

    <div class="container my-5">
        <div class="row">
            <div class="col-lg-8 mx-auto">
                <div class="text-center mb-5">
                    <h1 class="display-5 fw-bold">Contact Us</h1>
                    <p class="lead text-muted">Get in touch with our travel experts</p>
                </div>

                <div class="card shadow">
                    <div class="card-body p-5">
                        <form id="contactForm" method="POST">
                            <div class="row g-3">
                                <div class="col-md-6">
                                    <label class="form-label">Full Name *</label>
                                    <input type="text" class="form-control" name="name" required>
                                </div>
                                <div class="col-md-6">
                                    <label class="form-label">Email Address *</label>
                                    <input type="email" class="form-control" name="email" required>
                                </div>
                                <div class="col-md-6">
                                    <label class="form-label">Phone Number *</label>
                                    <input type="tel" class="form-control" name="phone" required>
                                </div>
                                <div class="col-md-6">
                                    <label class="form-label">Subject</label>
                                    <input type="text" class="form-control" name="subject" placeholder="General Inquiry">
                                </div>
                                <div class="col-12">
                                    <label class="form-label">Message *</label>
                                    <textarea class="form-control" name="message" rows="5" required 
                                              placeholder="Tell us about your travel plans..."></textarea>
                                </div>
                                <div class="col-12">
                                    <button type="submit" class="btn btn-primary btn-lg">
                                        <i class="fas fa-paper-plane me-2"></i>Send Message
                                    </button>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>

                <div class="row mt-5">
                    <div class="col-md-4 text-center mb-4">
                        <div class="card h-100">
                            <div class="card-body">
                                <i class="fas fa-phone fa-2x text-primary mb-3"></i>
                                <h5>Call Us</h5>
                                <p class="text-muted">+91 99999 99999</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4 text-center mb-4">
                        <div class="card h-100">
                            <div class="card-body">
                                <i class="fas fa-envelope fa-2x text-primary mb-3"></i>
                                <h5>Email Us</h5>
                                <p class="text-muted">info@apniholidays.com</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4 text-center mb-4">
                        <div class="card h-100">
                            <div class="card-body">
                                <i class="fab fa-whatsapp fa-2x text-primary mb-3"></i>
                                <h5>WhatsApp</h5>
                                <p class="text-muted">+91 99999 99999</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
    document.getElementById('contactForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        
        try {
            const response = await fetch('/contact', {
                method: 'POST',
                body: formData
            });
            const result = await response.json();
            
            if (result.status === 'success') {
                alert('Thank you! Your message has been sent successfully.');
                this.reset();
            } else {
                alert('Error: ' + result.message);
            }
        } catch (error) {
            alert('Failed to send message. Please try again.');
        }
    });
    </script>
</body>
</html>
    """)

@app.route('/booking', methods=['POST'])
def booking():
    """Handle booking form submission"""
    try:
        package_id = request.form.get('package_id')
        travel_date = request.form.get('travel_date')
        travelers = int(request.form.get('travelers', 0))
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        
        # Get package details for pricing
        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT price, discount_price FROM packages WHERE id = %s", (package_id,))
            package = cur.fetchone()
            
            if package:
                price_per_person = package[1] if package[1] else package[0]
                total_amount = price_per_person * travelers
                
                booking_id = f"book_{int(datetime.now().timestamp())}"
                cur.execute("""
                    INSERT INTO bookings (id, package_id, traveler_name, traveler_email, traveler_phone,
                                        number_of_travelers, travel_date, total_amount, 
                                        payment_status, booking_status, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'pending', 'pending', %s)
                """, (booking_id, package_id, name, email, phone, travelers, travel_date, 
                      total_amount, datetime.now()))
                conn.commit()
                
                return jsonify({
                    'status': 'success',
                    'message': 'Booking request submitted successfully!',
                    'booking_id': booking_id,
                    'total_amount': total_amount
                })
            else:
                return jsonify({'status': 'error', 'message': 'Package not found'})
        else:
            return jsonify({'status': 'error', 'message': 'Database connection failed'})
            
    except Exception as e:
        print(f"Booking error: {e}")
        return jsonify({'status': 'error', 'message': 'Booking failed. Please try again.'})

@app.route('/auth/login', methods=['GET', 'POST'])
def auth_login():
    """User login page"""
    from flask import session
    error_message = ''
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            error_message = 'Please enter both email and password'
        else:
            try:
                # Use Firestore to authenticate user
                user = get_user_by_email(email)
                
                if user and user.get('status') == 'active':
                    stored_password = user.get('password_hash')
                    if stored_password:
                        from werkzeug.security import check_password_hash
                        if check_password_hash(stored_password, password):
                            # Set user session
                            session['user_id'] = user.get('id')
                            session['user_name'] = user.get('name')
                            session['user_email'] = user.get('email')
                            return redirect('/')
                        else:
                            error_message = 'Invalid email or password'
                    else:
                        error_message = 'Invalid email or password'
                else:
                    error_message = 'Invalid email or password'
            except Exception as e:
                print(f"Login error: {e}")
                error_message = 'Login failed. Please try again.'
    
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Apni Holidays</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="min-vh-100 d-flex align-items-center">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-md-6 col-lg-5">
                    <div class="card shadow">
                        <div class="card-body p-5">
                            <div class="text-center mb-4">
                                <a href="/" class="text-decoration-none">
                                    <i class="fas fa-plane text-primary" style="font-size: 3rem;"></i>
                                    <h3 class="fw-bold mt-3 text-primary">Apni Holidays</h3>
                                </a>
                                <p class="text-muted">Welcome back! Please sign in to your account</p>
                            </div>
                            
                            """ + (f'<div class="alert alert-danger">{error_message}</div>' if error_message else '') + """
                            
                            <div class="d-grid mb-3">
                                <button type="button" id="googleSignInBtn" class="btn btn-danger btn-lg">
                                    <i class="fab fa-google me-2"></i>Continue with Google
                                </button>
                            </div>
                            
                            <div class="text-center mb-3">
                                <small class="text-muted">OR</small>
                            </div>
                            
                            <form method="POST">
                                <div class="mb-3">
                                    <label class="form-label">Email Address</label>
                                    <input type="email" class="form-control" name="email" required>
                                </div>
                                
                                <div class="mb-4">
                                    <label class="form-label">Password</label>
                                    <input type="password" class="form-control" name="password" required>
                                </div>
                                
                                <button type="submit" class="btn btn-primary w-100 py-2 mb-3">
                                    <i class="fas fa-sign-in-alt me-2"></i>Sign In
                                </button>
                            </form>
                            
                            <div class="text-center">
                                <p class="text-muted mb-0">
                                    Don't have an account? 
                                    <a href="/auth/register" class="text-decoration-none">Sign up here</a>
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Firebase SDK -->
    <script src="https://www.gstatic.com/firebasejs/9.23.0/firebase-app-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/9.23.0/firebase-auth-compat.js"></script>
    
    <script>
        // Firebase configuration
        const firebaseConfig = """ + json.dumps(FIREBASE_CONFIG) + """;
        
        // Initialize Firebase
        firebase.initializeApp(firebaseConfig);
        const auth = firebase.auth();
        
        // Google sign-in
        document.getElementById('googleSignInBtn').addEventListener('click', function() {
            console.log('Current domain:', window.location.hostname);
            console.log('Current origin:', window.location.origin);
            const provider = new firebase.auth.GoogleAuthProvider();
            auth.signInWithPopup(provider)
                .then((result) => {
                    const user = result.user;
                    // Send user data to backend
                    fetch('/auth/google-login', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            uid: user.uid,
                            email: user.email,
                            name: user.displayName,
                            photo: user.photoURL
                        })
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.status === 'success') {
                            window.location.href = '/';
                        } else {
                            alert('Login failed: ' + data.message);
                        }
                    })
                    .catch((error) => {
                        console.error('Error:', error);
                        alert('Login failed. Please try again.');
                    });
                })
                .catch((error) => {
                    console.error('Google sign-in error:', error);
                    alert('Google sign-in failed: ' + error.message);
                });
        });
    </script>
</body>
</html>
    """, error_message=error_message)

@app.route('/auth/google-login', methods=['POST'])
def google_login():
    """Handle Google authentication"""
    try:
        data = request.get_json()
        uid = data.get('uid')
        email = data.get('email')
        name = data.get('name')
        photo = data.get('photo')
        
        if not uid or not email:
            return jsonify({'status': 'error', 'message': 'Invalid Google login data'})
        
        # Check if user exists or create new user in Firestore
        user = get_user_by_email(email)
        
        if user:
            # Update existing user
            user_id = user.get('id')
            user_name = user.get('name')
            # Update Firebase UID if not set
            if not user.get('firebase_uid'):
                update_user_data(user_id, {'firebase_uid': uid, 'last_login': datetime.now()})
        else:
            # Create new user
            user_id = f"user_google_{uid[-8:]}"
            user_data = {
                'id': user_id,
                'name': name,
                'email': email,
                'firebase_uid': uid,
                'status': 'active',
                'created_at': datetime.now(),
                'last_login': datetime.now()
            }
            create_user(user_data)
            user_name = name
            
            # Set session
            from flask import session
            session['user_id'] = user_id
            session['user_name'] = user_name
            session['user_email'] = email
            session['firebase_uid'] = uid
            
            return jsonify({'status': 'success', 'message': 'Login successful'})
            
    except Exception as e:
        print(f"Google login error: {e}")
        return jsonify({'status': 'error', 'message': 'Login failed. Please try again.'})

@app.route('/admin/google-login', methods=['POST'])
def admin_google_login():
    """Handle Admin Google authentication"""
    try:
        data = request.get_json()
        uid = data.get('uid')
        email = data.get('email')
        name = data.get('name')
        
        if not uid or not email:
            return jsonify({'status': 'error', 'message': 'Invalid Google login data'})
        
        # Check if the email is authorized for admin access using Firestore
        admin = get_user_by_email(email)
        
        if admin and admin.get('role') == 'admin':
            # Set admin session
            from flask import session
            session['is_admin'] = True
            session['admin_name'] = admin.get('name', name)
            session['admin_email'] = admin.get('email')
            session['firebase_uid'] = uid
            # Also set user session for navigation
            session['user_id'] = admin.get('id')
            session['user_name'] = admin.get('name', name)
            session['user_email'] = admin.get('email')
            
            return jsonify({'status': 'success', 'message': 'Admin login successful'})
        else:
            # Check if it's a known admin email
            known_admin_emails = ['rajesh4telecom@gmail.com', 'admin@apniholidays.com', 'rkm.ytw1@gmail.com']
            if email in known_admin_emails:
                # Set admin session for known admins
                from flask import session
                session['is_admin'] = True
                session['admin_name'] = name
                session['admin_email'] = email
                session['firebase_uid'] = uid
                # Also set user session for navigation
                session['user_id'] = f"admin_{uid[-8:]}"
                session['user_name'] = name
                session['user_email'] = email
                
                return jsonify({'status': 'success', 'message': 'Admin login successful'})
            else:
                return jsonify({'status': 'error', 'message': 'Email not authorized for admin access'})
            
    except Exception as e:
        print(f"Admin Google login error: {e}")
        return jsonify({'status': 'error', 'message': 'Admin login failed. Please try again.'})

@app.route('/auth/register')
def auth_register():
    """User registration page"""
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Register - Apni Holidays</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="min-vh-100 d-flex align-items-center">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-md-6 col-lg-5">
                    <div class="card shadow">
                        <div class="card-body p-5">
                            <div class="text-center mb-4">
                                <a href="/" class="text-decoration-none">
                                    <i class="fas fa-plane text-primary" style="font-size: 3rem;"></i>
                                    <h3 class="fw-bold mt-3 text-primary">Apni Holidays</h3>
                                </a>
                                <p class="text-muted">Create your account to start booking</p>
                            </div>
                            
                            <form>
                                <div class="mb-3">
                                    <label class="form-label">Full Name</label>
                                    <input type="text" class="form-control" required>
                                </div>
                                
                                <div class="mb-3">
                                    <label class="form-label">Email Address</label>
                                    <input type="email" class="form-control" required>
                                </div>
                                
                                <div class="mb-3">
                                    <label class="form-label">Phone Number</label>
                                    <input type="tel" class="form-control" required>
                                </div>
                                
                                <div class="mb-4">
                                    <label class="form-label">Password</label>
                                    <input type="password" class="form-control" required>
                                </div>
                                
                                <button type="submit" class="btn btn-primary w-100 py-2 mb-3">
                                    <i class="fas fa-user-plus me-2"></i>Create Account
                                </button>
                            </form>
                            
                            <div class="text-center my-3">
                                <span class="text-muted">OR</span>
                            </div>
                            
                            <div class="d-grid mb-3">
                                <button type="button" id="registerGoogleSignInBtn" class="btn btn-danger">
                                    <i class="fab fa-google me-2"></i>Sign up with Google
                                </button>
                            </div>
                            
                            <div class="text-center">
                                <p class="text-muted mb-0">
                                    Already have an account? 
                                    <a href="/auth/login" class="text-decoration-none">Sign in here</a>
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Firebase SDK -->
    <script src="https://www.gstatic.com/firebasejs/9.23.0/firebase-app-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/9.23.0/firebase-auth-compat.js"></script>
    
    <script>
        // Firebase configuration
        const firebaseConfig = """ + json.dumps(FIREBASE_CONFIG) + """;
        
        // Initialize Firebase
        firebase.initializeApp(firebaseConfig);
        const auth = firebase.auth();
        
        // Google sign-up
        document.getElementById('registerGoogleSignInBtn').addEventListener('click', function() {
            console.log('Register - Current domain:', window.location.hostname);
            console.log('Register - Current origin:', window.location.origin);
            const provider = new firebase.auth.GoogleAuthProvider();
            auth.signInWithPopup(provider)
                .then((result) => {
                    const user = result.user;
                    // Send user data to backend
                    fetch('/auth/google-login', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            uid: user.uid,
                            email: user.email,
                            name: user.displayName,
                            photo: user.photoURL
                        })
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.status === 'success') {
                            window.location.href = '/';
                        } else {
                            alert('Registration failed: ' + data.message);
                        }
                    })
                    .catch((error) => {
                        console.error('Error:', error);
                        alert('Registration failed. Please try again.');
                    });
                })
                .catch((error) => {
                    console.error('Google sign-in error:', error);
                    alert('Google sign-in failed: ' + error.message);
                });
        });
    </script>
</body>
</html>
    """)

@app.route('/admin')
def admin():
    """Admin panel redirect"""
    return redirect('/admin/login')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login"""
    error_message = ''
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check admin credentials using Firestore
        try:
            admin = get_user_by_email(email)
            
            if admin and admin.get('role') == 'admin' and admin.get('status') == 'active':
                stored_password = admin.get('password_hash') or admin.get('password')
                if stored_password:
                    # Verify password using werkzeug security
                    from werkzeug.security import check_password_hash
                    try:
                        if check_password_hash(stored_password, password):
                            from flask import session
                            # Set admin session
                            session['is_admin'] = True
                            session['admin_name'] = admin.get('name')
                            session['admin_email'] = admin.get('email')
                            # Also set user session for navigation
                            session['user_id'] = admin.get('id')
                            session['user_name'] = admin.get('name')
                            session['user_email'] = admin.get('email')
                            return redirect('/admin/dashboard')
                        else:
                            error_message = 'Invalid email or password'
                    except Exception as e:
                        print(f"Password verification error: {e}")
                        error_message = 'Invalid email or password'
                else:
                    error_message = 'Invalid email or password'
            else:
                error_message = 'Invalid email or password'
        except Exception as e:
            print(f"Admin login error: {e}")
            error_message = 'Login failed. Please try again.'
    
    error_div = f'<div class="alert alert-danger">{error_message}</div>' if error_message else ''
    return render_template_string(admin_login_template % {'error_div': error_div})

admin_login_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Login - Apni Holidays</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body class="bg-dark">
    <div class="min-vh-100 d-flex align-items-center">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-md-6 col-lg-4">
                    <div class="card shadow">
                        <div class="card-body p-5">
                            <div class="text-center mb-4">
                                <i class="fas fa-shield-alt text-primary" style="font-size: 3rem;"></i>
                                <h3 class="fw-bold mt-3">Admin Panel</h3>
                                <p class="text-muted">Apni Holidays Administration</p>
                            </div>
                            
                            %(error_div)s
                            
                            <form method="POST">
                                <div class="mb-3">
                                    <label class="form-label">Email Address</label>
                                    <input type="email" class="form-control" name="email" required 
                                           placeholder="Enter your admin email">
                                </div>
                                
                                <div class="mb-4">
                                    <label class="form-label">Password</label>
                                    <input type="password" class="form-control" name="password" required 
                                           placeholder="Enter your password">
                                </div>
                                
                                <button type="submit" class="btn btn-primary w-100 py-2">
                                    <i class="fas fa-sign-in-alt me-2"></i>Admin Login
                                </button>
                            </form>
                            
                            <div class="text-center my-3">
                                <span class="text-muted">OR</span>
                            </div>
                            
                            <div class="d-grid">
                                <button type="button" id="adminGoogleSignInBtn" class="btn btn-danger">
                                    <i class="fab fa-google me-2"></i>Continue with Google
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Firebase SDK -->
    <script src="https://www.gstatic.com/firebasejs/9.23.0/firebase-app-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/9.23.0/firebase-auth-compat.js"></script>
    
    <script>
        // Firebase configuration
        const firebaseConfig = """ + json.dumps(FIREBASE_CONFIG) + """;
        
        // Initialize Firebase
        firebase.initializeApp(firebaseConfig);
        const auth = firebase.auth();
        
        // Admin Google sign-in
        document.getElementById('adminGoogleSignInBtn').addEventListener('click', function() {
            console.log('Admin - Current domain:', window.location.hostname);
            console.log('Admin - Current origin:', window.location.origin);
            const provider = new firebase.auth.GoogleAuthProvider();
            auth.signInWithPopup(provider)
                .then((result) => {
                    const user = result.user;
                    // Send user data to backend for admin verification
                    fetch('/admin/google-login', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            uid: user.uid,
                            email: user.email,
                            name: user.displayName,
                            photo: user.photoURL
                        })
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.status === 'success') {
                            window.location.href = '/admin/dashboard';
                        } else {
                            alert('Admin login failed: ' + data.message);
                        }
                    })
                    .catch((error) => {
                        console.error('Error:', error);
                        alert('Admin login failed. Please try again.');
                    });
                })
                .catch((error) => {
                    console.error('Google sign-in error:', error);
                    alert('Google sign-in failed: ' + error.message);
                });
        });
    </script>
</body>
</html>
"""

@app.route('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard"""
    from flask import session
    if not session.get('is_admin'):
        return redirect('/admin/login')
    
    # Get statistics from Firestore
    try:
        packages = get_packages()
        users = get_all_users()
        
        stats = {
            'packages': len([p for p in packages if p.get('status') == 'active']),
            'users': len([u for u in users if u.get('status') == 'active']),
            'featured': len([p for p in packages if p.get('featured') == True and p.get('status') == 'active']),
            'inquiries': 0  # No inquiries collection yet
        }
    except Exception as e:
        print(f"Admin dashboard error: {e}")
        stats = {'packages': 0, 'users': 0, 'featured': 0, 'inquiries': 0}
    
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Dashboard - Apni Holidays</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand fw-bold" href="/admin/dashboard">
                <i class="fas fa-cog me-2"></i>Admin Panel
            </a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="/admin/logout">
                    <i class="fas fa-sign-out-alt me-1"></i>Logout
                </a>
            </div>
        </div>
    </nav>

    <div class="container-fluid py-4">
        <div class="row">
            <div class="col-12 mb-4">
                <h2>Welcome back, {{ session['admin_name'] }}!</h2>
                <p class="text-muted">Here's what's happening with your travel packages today.</p>
            </div>
        </div>
        
        <div class="row">
            <div class="col-xl-3 col-md-6 mb-4">
                <div class="card border-left-primary shadow h-100 py-2">
                    <div class="card-body">
                        <div class="row no-gutters align-items-center">
                            <div class="col mr-2">
                                <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">
                                    Total Packages</div>
                                <div class="h5 mb-0 font-weight-bold text-gray-800">{{ stats.packages }}</div>
                            </div>
                            <div class="col-auto">
                                <i class="fas fa-suitcase fa-2x text-gray-300"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="col-xl-3 col-md-6 mb-4">
                <div class="card border-left-success shadow h-100 py-2">
                    <div class="card-body">
                        <div class="row no-gutters align-items-center">
                            <div class="col mr-2">
                                <div class="text-xs font-weight-bold text-success text-uppercase mb-1">
                                    Featured Packages</div>
                                <div class="h5 mb-0 font-weight-bold text-gray-800">{{ stats.featured }}</div>
                            </div>
                            <div class="col-auto">
                                <i class="fas fa-star fa-2x text-gray-300"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="col-xl-3 col-md-6 mb-4">
                <div class="card border-left-info shadow h-100 py-2">
                    <div class="card-body">
                        <div class="row no-gutters align-items-center">
                            <div class="col mr-2">
                                <div class="text-xs font-weight-bold text-info text-uppercase mb-1">
                                    Total Users</div>
                                <div class="h5 mb-0 font-weight-bold text-gray-800">{{ stats.users }}</div>
                            </div>
                            <div class="col-auto">
                                <i class="fas fa-users fa-2x text-gray-300"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="col-xl-3 col-md-6 mb-4">
                <div class="card border-left-warning shadow h-100 py-2">
                    <div class="card-body">
                        <div class="row no-gutters align-items-center">
                            <div class="col mr-2">
                                <div class="text-xs font-weight-bold text-warning text-uppercase mb-1">
                                    New Inquiries</div>
                                <div class="h5 mb-0 font-weight-bold text-gray-800">{{ stats.inquiries }}</div>
                            </div>
                            <div class="col-auto">
                                <i class="fas fa-envelope fa-2x text-gray-300"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="row">
            <div class="col-12">
                <div class="card shadow">
                    <div class="card-header py-3">
                        <h6 class="m-0 font-weight-bold text-primary">Quick Actions</h6>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-3 mb-3">
                                <a href="/admin/packages/add" class="btn btn-primary w-100">
                                    <i class="fas fa-plus me-2"></i>Add Package
                                </a>
                            </div>
                            <div class="col-md-3 mb-3">
                                <a href="/admin/packages" class="btn btn-outline-primary w-100">
                                    <i class="fas fa-list me-2"></i>Manage Packages
                                </a>
                            </div>
                            <div class="col-md-3 mb-3">
                                <a href="/admin/users" class="btn btn-outline-success w-100">
                                    <i class="fas fa-users me-2"></i>Manage Users
                                </a>
                            </div>
                            <div class="col-md-3 mb-3">
                                <a href="/" class="btn btn-outline-info w-100" target="_blank">
                                    <i class="fas fa-globe me-2"></i>View Website
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <style>
    .border-left-primary { border-left: .25rem solid #4e73df!important; }
    .border-left-success { border-left: .25rem solid #1cc88a!important; }
    .border-left-info { border-left: .25rem solid #36b9cc!important; }
    .border-left-warning { border-left: .25rem solid #f6c23e!important; }
    </style>
</body>
</html>
    """, stats=stats, session=session)

@app.route('/auth/logout')
def auth_logout():
    """User logout"""
    from flask import session
    session.clear()
    return redirect('/')

@app.route('/profile')
def profile():
    """User profile page"""
    from flask import session
    if not session.get('user_id'):
        return redirect('/auth/login')
    
    user_id = session.get('user_id')
    user_name = session.get('user_name')
    user_email = session.get('user_email')
    
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Profile - Apni Holidays</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
        <div class="container">
            <a class="navbar-brand fw-bold" href="/">
                <i class="fas fa-plane text-primary"></i> Apni Holidays
            </a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="/">
                    <i class="fas fa-home me-1"></i>Home
                </a>
                <a class="nav-link" href="/auth/logout">
                    <i class="fas fa-sign-out-alt me-1"></i>Logout
                </a>
            </div>
        </div>
    </nav>

    <div class="container py-5">
        <div class="row">
            <div class="col-md-8 mx-auto">
                <div class="card shadow">
                    <div class="card-header bg-primary text-white">
                        <h4 class="mb-0">
                            <i class="fas fa-user me-2"></i>My Profile
                        </h4>
                    </div>
                    <div class="card-body p-4">
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label fw-bold">Name</label>
                                <p class="form-control-plaintext">{{ user_name }}</p>
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label fw-bold">Email</label>
                                <p class="form-control-plaintext">{{ user_email }}</p>
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label fw-bold">User ID</label>
                                <p class="form-control-plaintext">{{ user_id }}</p>
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label fw-bold">Account Status</label>
                                <p class="form-control-plaintext">
                                    <span class="badge bg-success">Active</span>
                                </p>
                            </div>
                        </div>
                        
                        <div class="mt-4">
                            <a href="/my-bookings" class="btn btn-primary me-2">
                                <i class="fas fa-suitcase me-2"></i>View My Bookings
                            </a>
                            <a href="/packages" class="btn btn-outline-primary">
                                <i class="fas fa-plane me-2"></i>Browse Packages
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
    """, user_name=user_name, user_email=user_email, user_id=user_id)

@app.route('/my-bookings')
def my_bookings():
    """User bookings page"""
    from flask import session
    if not session.get('user_id'):
        return redirect('/auth/login')
    
    user_id = session.get('user_id')
    user_name = session.get('user_name')
    
    # Get user bookings
    try:
        conn = get_db_connection()
        bookings = []
        if conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT b.id, b.traveler_name, b.traveler_email, b.number_of_travelers,
                       b.travel_date, b.total_amount, b.booking_status, b.created_at,
                       p.title, p.destination, p.days
                FROM bookings b
                LEFT JOIN packages p ON b.package_id = p.id
                WHERE b.user_id = %s
                ORDER BY b.created_at DESC
            """, (user_id,))
            bookings = cur.fetchall()
            cur.close()
            conn.close()
    except Exception as e:
        print(f"Error fetching bookings: {e}")
        bookings = []
    
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Bookings - Apni Holidays</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
        <div class="container">
            <a class="navbar-brand fw-bold" href="/">
                <i class="fas fa-plane text-primary"></i> Apni Holidays
            </a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="/">
                    <i class="fas fa-home me-1"></i>Home
                </a>
                <a class="nav-link" href="/profile">
                    <i class="fas fa-user me-1"></i>Profile
                </a>
                <a class="nav-link" href="/auth/logout">
                    <i class="fas fa-sign-out-alt me-1"></i>Logout
                </a>
            </div>
        </div>
    </nav>

    <div class="container py-5">
        <div class="row">
            <div class="col-12">
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h2><i class="fas fa-suitcase me-2"></i>My Bookings</h2>
                    <a href="/packages" class="btn btn-primary">
                        <i class="fas fa-plus me-2"></i>Book New Trip
                    </a>
                </div>
                
                {% if bookings %}
                <div class="row">
                    {% for booking in bookings %}
                    <div class="col-lg-6 mb-4">
                        <div class="card shadow-sm">
                            <div class="card-header d-flex justify-content-between align-items-center">
                                <h6 class="mb-0">{{ booking[8] }}</h6>
                                <span class="badge {% if booking[6] == 'confirmed' %}bg-success{% elif booking[6] == 'pending' %}bg-warning{% else %}bg-secondary{% endif %}">
                                    {{ booking[6].title() }}
                                </span>
                            </div>
                            <div class="card-body">
                                <p class="mb-2">
                                    <i class="fas fa-map-marker-alt text-primary me-2"></i>
                                    {{ booking[9] }} ({{ booking[10] }} days)
                                </p>
                                <p class="mb-2">
                                    <i class="fas fa-calendar text-primary me-2"></i>
                                    Travel Date: {{ booking[4] }}
                                </p>
                                <p class="mb-2">
                                    <i class="fas fa-users text-primary me-2"></i>
                                    Travelers: {{ booking[3] }}
                                </p>
                                <p class="mb-2">
                                    <i class="fas fa-rupee-sign text-primary me-2"></i>
                                    Total: ₹{{ "{:,.0f}".format(booking[5]) }}
                                </p>
                                <small class="text-muted">
                                    Booking ID: {{ booking[0] }} | Booked on: {{ booking[7].strftime('%d %b %Y') }}
                                </small>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
                {% else %}
                <div class="text-center py-5">
                    <i class="fas fa-suitcase fa-3x text-muted mb-3"></i>
                    <h4>No bookings yet</h4>
                    <p class="text-muted mb-4">Start planning your next adventure!</p>
                    <a href="/packages" class="btn btn-primary btn-lg">
                        <i class="fas fa-plane me-2"></i>Browse Travel Packages
                    </a>
                </div>
                {% endif %}
            </div>
        </div>
    </div>
</body>
</html>
    """, bookings=bookings, user_name=user_name)

# Admin routes for package management

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    from flask import session
    session.clear()
    return redirect('/admin/login')

@app.route('/admin/packages')
def admin_packages():
    """Admin packages management"""
    from flask import session
    if not session.get('is_admin'):
        return redirect('/admin/login')
    
    # Get all packages from Firestore
    try:
        packages = get_packages()
        # Sort by created_at descending - handle different date types
        packages.sort(key=lambda x: x.get('created_at', datetime.min) if isinstance(x.get('created_at'), datetime) else datetime.min, reverse=True)
    except Exception as e:
        print(f"Error fetching admin packages: {e}")
        packages = []
    
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Manage Packages - Admin Panel</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand fw-bold" href="/admin/dashboard">
                <i class="fas fa-cog me-2"></i>Admin Panel
            </a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="/admin/dashboard">Dashboard</a>
                <a class="nav-link" href="/admin/logout">
                    <i class="fas fa-sign-out-alt me-1"></i>Logout
                </a>
            </div>
        </div>
    </nav>

    <div class="container-fluid py-4">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2>Manage Packages</h2>
            <a href="/admin/packages/add" class="btn btn-primary">
                <i class="fas fa-plus me-2"></i>Add New Package
            </a>
        </div>
        
        <div class="card shadow">
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-hover">
                        <thead class="table-dark">
                            <tr>
                                <th>ID</th>
                                <th>Title</th>
                                <th>Destination</th>
                                <th>Days</th>
                                <th>Price</th>
                                <th>Status</th>
                                <th>Featured</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for package in packages %}
                            <tr>
                                <td>{{ package.id }}</td>
                                <td>{{ package.title }}</td>
                                <td>{{ package.destination }}</td>
                                <td>{{ package.days }} days</td>
                                <td>
                                    {% if package.discount_price %}
                                        <span class="text-decoration-line-through text-muted">₹{{ "{:,.0f}".format(package.price) }}</span><br>
                                        <strong>₹{{ "{:,.0f}".format(package.discount_price) }}</strong>
                                    {% else %}
                                        <strong>₹{{ "{:,.0f}".format(package.price) }}</strong>
                                    {% endif %}
                                </td>
                                <td>
                                    <span class="badge {% if package.status == 'active' %}bg-success{% else %}bg-secondary{% endif %}">
                                        {{ package.status.title() }}
                                    </span>
                                </td>
                                <td>
                                    <span class="badge {% if package.featured %}bg-warning text-dark{% else %}bg-light text-dark{% endif %}">
                                        {% if package.featured %}Featured{% else %}Regular{% endif %}
                                    </span>
                                </td>
                                <td>
                                    <div class="btn-group" role="group">
                                        <a href="/admin/packages/edit/{{ package.id }}" class="btn btn-sm btn-outline-primary">
                                            <i class="fas fa-edit"></i>
                                        </a>
                                        <button class="btn btn-sm btn-outline-danger" onclick="deletePackage({{ package.id }})">
                                            <i class="fas fa-trash"></i>
                                        </button>
                                        <a href="/package-details?id={{ package.id }}" class="btn btn-sm btn-outline-info" target="_blank">
                                            <i class="fas fa-eye"></i>
                                        </a>
                                    </div>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <script>
    function deletePackage(packageId) {
        if (confirm('Are you sure you want to delete this package?')) {
            fetch('/admin/packages/delete/' + packageId, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    alert('Error deleting package: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error deleting package');
            });
        }
    }
    </script>
</body>
</html>
    """, packages=packages)

@app.route('/admin/packages/delete/<package_id>', methods=['POST'])
def admin_delete_package(package_id):
    """Delete package"""
    from flask import session, jsonify
    if not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    try:
        success = delete_package(package_id)
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Failed to delete package'})
    except Exception as e:
        print(f"Error deleting package: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/packages/add', methods=['GET', 'POST'])
def admin_add_package():
    """Add new package"""
    from flask import session
    if not session.get('is_admin'):
        return redirect('/admin/login')
    
    if request.method == 'POST':
        # Get form data
        title = request.form.get('title')
        destination = request.form.get('destination')
        days = request.form.get('days')
        price = request.form.get('price')
        discount_price = request.form.get('discount_price')
        description = request.form.get('description')
        highlights = request.form.get('highlights')
        inclusions = request.form.get('inclusions')
        exclusions = request.form.get('exclusions')
        itinerary = request.form.get('itinerary')
        image_url = request.form.get('image_url')
        featured = 'featured' in request.form
        
        try:
            # Generate unique package ID
            package_id = f"pkg_{destination.lower().replace(' ', '_')}_{int(datetime.now().timestamp())}"
            
            # Create package data
            package_data = {
                'id': package_id,
                'title': title,
                'destination': destination,
                'days': int(days),
                'price': float(price),
                'discount_price': float(discount_price) if discount_price else None,
                'description': description,
                'highlights': highlights,
                'inclusions': inclusions,
                'exclusions': exclusions,
                'itinerary': itinerary,
                'image_url': image_url,
                'featured': featured,
                'status': 'active',
                'created_at': datetime.now()
            }
            
            # Add package to Firestore
            success = add_package(package_data)
            if success:
                return redirect('/admin/packages')
            else:
                return "Failed to add package", 500
        except Exception as e:
            print(f"Error adding package: {e}")
            return f"Error adding package: {e}", 500
    
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Add Package - Admin Panel</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand fw-bold" href="/admin/dashboard">
                <i class="fas fa-cog me-2"></i>Admin Panel
            </a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="/admin/packages">Back to Packages</a>
                <a class="nav-link" href="/admin/logout">Logout</a>
            </div>
        </div>
    </nav>

    <div class="container py-4">
        <h2 class="mb-4">Add New Package</h2>
        
        <div class="card shadow">
            <div class="card-body">
                <form method="POST">
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Package Title *</label>
                            <input type="text" class="form-control" name="title" required>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Destination *</label>
                            <input type="text" class="form-control" name="destination" required>
                        </div>
                        <div class="col-md-4 mb-3">
                            <label class="form-label">Duration (Days) *</label>
                            <input type="number" class="form-control" name="days" required>
                        </div>
                        <div class="col-md-4 mb-3">
                            <label class="form-label">Price (₹) *</label>
                            <input type="number" class="form-control" name="price" step="0.01" required>
                        </div>
                        <div class="col-md-4 mb-3">
                            <label class="form-label">Discount Price (₹)</label>
                            <input type="number" class="form-control" name="discount_price" step="0.01">
                        </div>
                        <div class="col-12 mb-3">
                            <label class="form-label">Image URL *</label>
                            <input type="url" class="form-control" name="image_url" required>
                        </div>
                        <div class="col-12 mb-3">
                            <label class="form-label">Description *</label>
                            <textarea class="form-control" name="description" rows="4" required></textarea>
                        </div>
                        <div class="col-12 mb-3">
                            <label class="form-label">Highlights (comma separated)</label>
                            <textarea class="form-control" name="highlights" rows="3"></textarea>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Inclusions (comma separated)</label>
                            <textarea class="form-control" name="inclusions" rows="4"></textarea>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Exclusions (comma separated)</label>
                            <textarea class="form-control" name="exclusions" rows="4"></textarea>
                        </div>
                        <div class="col-12 mb-3">
                            <label class="form-label">Itinerary (one day per line)</label>
                            <textarea class="form-control" name="itinerary" rows="6"></textarea>
                        </div>
                        <div class="col-12 mb-3">
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" name="featured" id="featured">
                                <label class="form-check-label" for="featured">
                                    Mark as Featured Package
                                </label>
                            </div>
                        </div>
                    </div>
                    
                    <div class="text-end">
                        <a href="/admin/packages" class="btn btn-secondary me-2">Cancel</a>
                        <button type="submit" class="btn btn-primary">
                            <i class="fas fa-save me-2"></i>Save Package
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</body>
</html>
    """)

@app.route('/admin/users')
def admin_users():
    """Admin users management"""
    from flask import session
    if not session.get('is_admin'):
        return redirect('/admin/login')
    
    # Get all users from Firestore
    try:
        users = get_all_users()
        # Convert date objects to strings for template rendering and sort safely
        for user in users:
            if user.get('created_at'):
                if hasattr(user['created_at'], 'strftime'):
                    user['created_at_str'] = user['created_at'].strftime('%d %b %Y')
                elif isinstance(user['created_at'], str):
                    user['created_at_str'] = user['created_at']
                else:
                    user['created_at_str'] = 'N/A'
            else:
                user['created_at_str'] = 'N/A'
                
        # Sort users by name instead of date to avoid timezone comparison issues
        try:
            users.sort(key=lambda x: str(x.get('name', '')).lower(), reverse=False)
        except Exception as sort_error:
            print(f"Sort error: {sort_error}")
            # If sorting fails, just use the list as-is
    except Exception as e:
        print(f"Error fetching users: {e}")
        users = []
    
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Manage Users - Admin Panel</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand fw-bold" href="/admin/dashboard">
                <i class="fas fa-cog me-2"></i>Admin Panel
            </a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="/admin/dashboard">Dashboard</a>
                <a class="nav-link" href="/admin/logout">Logout</a>
            </div>
        </div>
    </nav>

    <div class="container-fluid py-4">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2>Manage Users</h2>
            <div>
                <button class="btn btn-success me-2" onclick="showAddUserModal()">
                    <i class="fas fa-plus me-2"></i>Add New User
                </button>
                <button class="btn btn-info" onclick="showAdminUsersModal()">
                    <i class="fas fa-shield-alt me-2"></i>Manage Admins
                </button>
            </div>
        </div>
        
        <div class="card shadow">
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-hover">
                        <thead class="table-dark">
                            <tr>
                                <th>ID</th>
                                <th>Name</th>
                                <th>Email</th>
                                <th>Phone</th>
                                <th>Registration Date</th>
                                <th>Status</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for user in users %}
                            <tr>
                                <td>{{ user.id }}</td>
                                <td>{{ user.name }}</td>
                                <td>{{ user.email }}</td>
                                <td>{{ user.phone or 'N/A' }}</td>
                                <td>{{ user.created_at_str }}</td>
                                <td>
                                    <span class="badge {% if user.status == 'active' %}bg-success{% else %}bg-secondary{% endif %}">
                                        {{ user.status.title() }}
                                    </span>
                                </td>
                                <td>
                                    <div class="btn-group" role="group">
                                        <button class="btn btn-sm btn-outline-primary" onclick="editUser('{{ user.id }}', '{{ user.name }}', '{{ user.email }}', '{{ user.phone or '' }}', '{{ user.status }}')" title="Edit User">
                                            <i class="fas fa-edit"></i>
                                        </button>
                                        <button class="btn btn-sm btn-outline-warning" onclick="toggleUserStatus('{{ user.id }}', '{{ user.status }}')" title="Toggle Status">
                                            <i class="fas fa-toggle-on"></i>
                                        </button>
                                        <button class="btn btn-sm btn-outline-info" onclick="promoteToAdmin('{{ user.id }}', '{{ user.name }}', '{{ user.email }}')" title="Make Admin">
                                            <i class="fas fa-shield-alt"></i>
                                        </button>
                                        <button class="btn btn-sm btn-outline-danger" onclick="deleteUser('{{ user.id }}', '{{ user.name }}')" title="Delete User">
                                            <i class="fas fa-trash"></i>
                                        </button>
                                    </div>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <!-- Add User Modal -->
    <div class="modal fade" id="addUserModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Add New User</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <form id="addUserForm">
                        <div class="mb-3">
                            <label class="form-label">Name *</label>
                            <input type="text" class="form-control" name="name" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Email *</label>
                            <input type="email" class="form-control" name="email" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Phone</label>
                            <input type="tel" class="form-control" name="phone">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Password *</label>
                            <input type="password" class="form-control" name="password" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Status</label>
                            <select class="form-select" name="status">
                                <option value="active">Active</option>
                                <option value="inactive">Inactive</option>
                            </select>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-success" onclick="submitAddUser()">Add User</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Edit User Modal -->
    <div class="modal fade" id="editUserModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Edit User</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <form id="editUserForm">
                        <input type="hidden" name="user_id">
                        <div class="mb-3">
                            <label class="form-label">Name *</label>
                            <input type="text" class="form-control" name="name" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Email *</label>
                            <input type="email" class="form-control" name="email" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Phone</label>
                            <input type="tel" class="form-control" name="phone">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Status</label>
                            <select class="form-select" name="status">
                                <option value="active">Active</option>
                                <option value="inactive">Inactive</option>
                            </select>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-primary" onclick="submitEditUser()">Update User</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Admin Users Modal -->
    <div class="modal fade" id="adminUsersModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Manage Admin Users</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div id="adminUsersList">Loading...</div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
    // Show Add User Modal
    function showAddUserModal() {
        new bootstrap.Modal(document.getElementById('addUserModal')).show();
    }
    
    // Submit Add User Form
    function submitAddUser() {
        const form = document.getElementById('addUserForm');
        const formData = new FormData(form);
        
        fetch('/admin/users/add', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert('Error adding user: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error adding user');
        });
    }
    
    // Edit User
    function editUser(userId, name, email, phone, status) {
        const form = document.getElementById('editUserForm');
        form.querySelector('[name="user_id"]').value = userId;
        form.querySelector('[name="name"]').value = name;
        form.querySelector('[name="email"]').value = email;
        form.querySelector('[name="phone"]').value = phone;
        form.querySelector('[name="status"]').value = status;
        
        new bootstrap.Modal(document.getElementById('editUserModal')).show();
    }
    
    // Submit Edit User Form
    function submitEditUser() {
        const form = document.getElementById('editUserForm');
        const formData = new FormData(form);
        const userId = formData.get('user_id');
        
        fetch('/admin/users/edit/' + userId, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert('Error updating user: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error updating user');
        });
    }
    
    // Toggle User Status
    function toggleUserStatus(userId, currentStatus) {
        const newStatus = currentStatus === 'active' ? 'inactive' : 'active';
        if (confirm('Are you sure you want to ' + newStatus + ' this user?')) {
            fetch('/admin/users/toggle/' + userId, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({status: newStatus})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    alert('Error updating user status: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error updating user status');
            });
        }
    }
    
    // Promote User to Admin
    function promoteToAdmin(userId, name, email) {
        if (confirm('Are you sure you want to promote ' + name + ' to admin?')) {
            fetch('/admin/users/promote/' + userId, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({name: name, email: email})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('User promoted to admin successfully!');
                    location.reload();
                } else {
                    alert('Error promoting user: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error promoting user');
            });
        }
    }
    
    // Delete User
    function deleteUser(userId, name) {
        if (confirm('Are you sure you want to delete user: ' + name + '? This action cannot be undone!')) {
            fetch('/admin/users/delete/' + userId, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    alert('Error deleting user: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error deleting user');
            });
        }
    }
    
    // Show Admin Users Modal
    function showAdminUsersModal() {
        fetch('/admin/users/admins')
        .then(response => response.json())
        .then(data => {
            let html = '<div class="table-responsive"><table class="table table-sm"><thead><tr><th>Name</th><th>Email</th><th>Role</th><th>Status</th><th>Actions</th></tr></thead><tbody>';
            data.admins.forEach(admin => {
                html += `<tr>
                    <td>${admin.name}</td>
                    <td>${admin.email}</td>
                    <td><span class="badge bg-primary">${admin.role}</span></td>
                    <td><span class="badge ${admin.status === 'active' ? 'bg-success' : 'bg-secondary'}">${admin.status}</span></td>
                    <td>
                        <button class="btn btn-sm btn-outline-warning" onclick="toggleAdminStatus(${admin.id}, '${admin.status}')">
                            <i class="fas fa-toggle-on"></i>
                        </button>
                    </td>
                </tr>`;
            });
            html += '</tbody></table></div>';
            document.getElementById('adminUsersList').innerHTML = html;
        })
        .catch(error => {
            document.getElementById('adminUsersList').innerHTML = '<div class="alert alert-danger">Error loading admin users</div>';
        });
        
        new bootstrap.Modal(document.getElementById('adminUsersModal')).show();
    }
    
    // Toggle Admin Status
    function toggleAdminStatus(adminId, currentStatus) {
        const newStatus = currentStatus === 'active' ? 'inactive' : 'active';
        if (confirm('Are you sure you want to ' + newStatus + ' this admin?')) {
            fetch('/admin/users/admin-toggle/' + adminId, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({status: newStatus})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showAdminUsersModal(); // Refresh the modal
                } else {
                    alert('Error updating admin status: ' + data.message);
                }
            });
        }
    }
    </script>
</body>
</html>
    """, users=users)

@app.route('/admin/packages/edit/<package_id>', methods=['GET', 'POST'])
def admin_edit_package(package_id):
    """Edit package"""
    from flask import session
    if not session.get('is_admin'):
        return redirect('/admin/login')
    
    if request.method == 'POST':
        # Update package
        title = request.form.get('title')
        destination = request.form.get('destination')
        days = request.form.get('days')
        price = request.form.get('price')
        discount_price = request.form.get('discount_price')
        description = request.form.get('description')
        highlights = request.form.get('highlights')
        inclusions = request.form.get('inclusions')
        exclusions = request.form.get('exclusions')
        itinerary = request.form.get('itinerary')
        image_url = request.form.get('image_url')
        featured = 'featured' in request.form
        status = request.form.get('status', 'active')
        
        try:
            conn = get_db_connection()
            if conn:
                cur = conn.cursor()
                cur.execute("""
                    UPDATE packages SET 
                        title = %s, destination = %s, days = %s, price = %s, 
                        discount_price = %s, description = %s, highlights = %s, 
                        inclusions = %s, exclusions = %s, itinerary = %s, 
                        image_url = %s, featured = %s, status = %s
                    WHERE id = %s
                """, (title, destination, int(days), float(price), 
                     float(discount_price) if discount_price else None,
                     description, highlights, inclusions, exclusions, 
                     itinerary, image_url, featured, status, package_id))
                conn.commit()
                cur.close()
                conn.close()
                return redirect('/admin/packages')
        except Exception as e:
            print(f"Error updating package: {e}")
            return f"Error updating package: {e}", 500
    
    # Get package data for editing
    try:
        conn = get_db_connection()
        package = None
        if conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, title, destination, days, price, discount_price, 
                       description, highlights, inclusions, exclusions, 
                       itinerary, image_url, featured, status
                FROM packages WHERE id = %s
            """, (package_id,))
            package_data = cur.fetchone()
            if package_data:
                package = {
                    'id': package_data[0], 'title': package_data[1], 'destination': package_data[2],
                    'days': package_data[3], 'price': package_data[4], 'discount_price': package_data[5],
                    'description': package_data[6], 'highlights': package_data[7], 'inclusions': package_data[8],
                    'exclusions': package_data[9], 'itinerary': package_data[10], 'image_url': package_data[11],
                    'featured': package_data[12], 'status': package_data[13]
                }
            cur.close()
            conn.close()
    except Exception as e:
        print(f"Error fetching package: {e}")
        package = None
    
    if not package:
        return redirect('/admin/packages')
    
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Edit Package - Admin Panel</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand fw-bold" href="/admin/dashboard">
                <i class="fas fa-cog me-2"></i>Admin Panel
            </a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="/admin/packages">Back to Packages</a>
                <a class="nav-link" href="/admin/logout">Logout</a>
            </div>
        </div>
    </nav>

    <div class="container py-4">
        <h2 class="mb-4">Edit Package: {{ package.title }}</h2>
        
        <div class="card shadow">
            <div class="card-body">
                <form method="POST">
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Package Title *</label>
                            <input type="text" class="form-control" name="title" value="{{ package.title }}" required>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Destination *</label>
                            <input type="text" class="form-control" name="destination" value="{{ package.destination }}" required>
                        </div>
                        <div class="col-md-3 mb-3">
                            <label class="form-label">Duration (Days) *</label>
                            <input type="number" class="form-control" name="days" value="{{ package.days }}" required>
                        </div>
                        <div class="col-md-3 mb-3">
                            <label class="form-label">Price (₹) *</label>
                            <input type="number" class="form-control" name="price" value="{{ package.price }}" step="0.01" required>
                        </div>
                        <div class="col-md-3 mb-3">
                            <label class="form-label">Discount Price (₹)</label>
                            <input type="number" class="form-control" name="discount_price" value="{{ package.discount_price or '' }}" step="0.01">
                        </div>
                        <div class="col-md-3 mb-3">
                            <label class="form-label">Status</label>
                            <select class="form-control" name="status">
                                <option value="active" {{ 'selected' if package.status == 'active' else '' }}>Active</option>
                                <option value="inactive" {{ 'selected' if package.status == 'inactive' else '' }}>Inactive</option>
                                <option value="draft" {{ 'selected' if package.status == 'draft' else '' }}>Draft</option>
                            </select>
                        </div>
                        <div class="col-12 mb-3">
                            <label class="form-label">Image URL *</label>
                            <input type="url" class="form-control" name="image_url" value="{{ package.image_url }}" required>
                        </div>
                        <div class="col-12 mb-3">
                            <label class="form-label">Description *</label>
                            <textarea class="form-control" name="description" rows="4" required>{{ package.description }}</textarea>
                        </div>
                        <div class="col-12 mb-3">
                            <label class="form-label">Highlights (comma separated)</label>
                            <textarea class="form-control" name="highlights" rows="3">{{ package.highlights or '' }}</textarea>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Inclusions (comma separated)</label>
                            <textarea class="form-control" name="inclusions" rows="4">{{ package.inclusions or '' }}</textarea>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Exclusions (comma separated)</label>
                            <textarea class="form-control" name="exclusions" rows="4">{{ package.exclusions or '' }}</textarea>
                        </div>
                        <div class="col-12 mb-3">
                            <label class="form-label">Itinerary (one day per line)</label>
                            <textarea class="form-control" name="itinerary" rows="6">{{ package.itinerary or '' }}</textarea>
                        </div>
                        <div class="col-12 mb-3">
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" name="featured" id="featured" {{ 'checked' if package.featured else '' }}>
                                <label class="form-check-label" for="featured">
                                    Mark as Featured Package
                                </label>
                            </div>
                        </div>
                    </div>
                    
                    <div class="text-end">
                        <a href="/admin/packages" class="btn btn-secondary me-2">Cancel</a>
                        <button type="submit" class="btn btn-primary">
                            <i class="fas fa-save me-2"></i>Update Package
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</body>
</html>
    """, package=package)

@app.route('/admin/users/toggle/<user_id>', methods=['POST'])
def admin_toggle_user_status(user_id):
    """Toggle user status"""
    from flask import session, jsonify
    if not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    try:
        data = request.get_json()
        new_status = data.get('status', 'active')
        
        # Update user status in Firestore
        success = update_user_status(user_id, new_status)
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Failed to update user status'})
    except Exception as e:
        print(f"Error toggling user status: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/users/add', methods=['POST'])
def admin_add_user():
    """Add new user"""
    from flask import session, jsonify
    if not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone', '')
        status = request.form.get('status', 'active')
        
        if not name or not email:
            return jsonify({'success': False, 'message': 'Name and email are required'})
        
        # Check if email already exists
        existing_user = get_user_by_email(email)
        if existing_user:
            return jsonify({'success': False, 'message': 'Email already exists'})
        
        # Create new user with default password
        password_hash = generate_password_hash('Rajesh@123')
        user_id = f"usr_{int(datetime.now().timestamp())}"
        
        user_data = {
            'id': user_id,
            'name': name,
            'email': email,
            'phone': phone,
            'password': password_hash,
            'status': status,
            'role': 'user',
            'created_at': datetime.now(),
            'last_login': None
        }
        
        # Add user to Firestore
        success = create_user(user_data)
        if success:
            return jsonify({'success': True, 'message': 'User added successfully with password: Rajesh@123'})
        else:
            return jsonify({'success': False, 'message': 'Failed to create user'})
            
    except Exception as e:
        print(f"Error adding user: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/users/update', methods=['POST'])
def admin_update_user():
    """Update user"""
    from flask import session, jsonify
    if not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    try:
        user_id = request.form.get('user_id')
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone', '')
        status = request.form.get('status', 'active')
        
        if not name or not email or not user_id:
            return jsonify({'success': False, 'message': 'User ID, name and email are required'})
        
        # Check if email exists for other users
        existing_user = get_user_by_email(email)
        if existing_user and existing_user.get('id') != user_id:
            return jsonify({'success': False, 'message': 'Email already exists for another user'})
        
        # Update user in Firestore
        update_data = {
            'name': name,
            'email': email,
            'phone': phone,
            'status': status
        }
        
        success = update_user(user_id, update_data)
        if success:
            return jsonify({'success': True, 'message': 'User updated successfully'})
        else:
            return jsonify({'success': False, 'message': 'Failed to update user'})
            
    except Exception as e:
        print(f"Error updating user: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/users/delete/<user_id>', methods=['POST'])
def admin_delete_user(user_id):
    """Delete user"""
    from flask import session, jsonify
    if not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    try:
        # Delete user from Firestore
        success = delete_user(user_id)
        if success:
            return jsonify({'success': True, 'message': 'User deleted successfully'})
        else:
            return jsonify({'success': False, 'message': 'Failed to delete user'})
    except Exception as e:
        print(f"Error deleting user: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/users/promote/<user_id>', methods=['POST'])
def admin_promote_user(user_id):
    """Promote user to admin"""
    from flask import session, jsonify
    if not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        
        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            # Get user info
            cur.execute("SELECT name, email, password FROM users WHERE id = %s", (user_id,))
            user_data = cur.fetchone()
            
            if not user_data:
                cur.close()
                conn.close()
                return jsonify({'success': False, 'message': 'User not found'})
            
            # Check if already admin
            cur.execute("SELECT id FROM admin_users WHERE email = %s", (user_data[1],))
            if cur.fetchone():
                cur.close()
                conn.close()
                return jsonify({'success': False, 'message': 'User is already an admin'})
            
            # Add to admin_users table
            cur.execute("""
                INSERT INTO admin_users (name, email, password, role, status, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (user_data[0], user_data[1], user_data[2], 'admin', 'active', datetime.now()))
            
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({'success': True, 'message': 'User promoted to admin successfully'})
        else:
            return jsonify({'success': False, 'message': 'Database connection failed'})
    except Exception as e:
        print(f"Error promoting user: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/users/admins')
def admin_get_admins():
    """Get all admin users"""
    from flask import session, jsonify
    if not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    try:
        conn = get_db_connection()
        admins = []
        if conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, name, email, role, status, created_at 
                FROM admin_users 
                ORDER BY created_at DESC
            """)
            admin_rows = cur.fetchall()
            for row in admin_rows:
                admins.append({
                    'id': row[0], 'name': row[1], 'email': row[2], 
                    'role': row[3], 'status': row[4], 'created_at': row[5]
                })
            cur.close()
            conn.close()
        return jsonify({'success': True, 'admins': admins})
    except Exception as e:
        print(f"Error fetching admins: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/users/admin-toggle/<int:admin_id>', methods=['POST'])
def admin_toggle_admin_status(admin_id):
    """Toggle admin status"""
    from flask import session, jsonify
    if not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    try:
        data = request.get_json()
        new_status = data.get('status', 'active')
        
        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            cur.execute("UPDATE admin_users SET status = %s WHERE id = %s", (new_status, admin_id))
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Database connection failed'})
    except Exception as e:
        print(f"Error toggling admin status: {e}")
        return jsonify({'success': False, 'message': str(e)})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
