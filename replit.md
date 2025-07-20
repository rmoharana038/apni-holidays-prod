# Apni Holidays - Travel Booking Website

## Overview

Apni Holidays is a Flask-based travel booking website originally designed for GoDaddy hosting but now running on Replit with PostgreSQL. The system provides a complete travel package management platform with admin controls, user authentication, and responsive design. The current implementation uses Flask/Python backend with PostgreSQL database and Bootstrap frontend.

## Recent Changes

**July 20, 2025:**
- ✅ Converted from PHP/MySQL to Flask/PostgreSQL architecture
- ✅ Set up PostgreSQL database with complete schema and sample data
- ✅ Fixed user authentication system with password hashing
- ✅ Fixed admin login system with proper credential validation
- ✅ Added user profile pages and session management
- ✅ Implemented user logout, profile, and bookings pages
- ✅ Navigation now shows logged-in user state with dropdown menu
- ✅ All login systems working: user and admin authentication
- ✅ Integrated Firebase Google Sign-In for both user and admin authentication
- ✅ Added Google authentication buttons to login, registration, and admin login pages
- ✅ Firebase configuration properly integrated with project ID "apni-holidays-prod"
- ✅ **MIGRATED TO FIRESTORE**: Successfully migrated from PostgreSQL to Firestore database
- ✅ Created comprehensive mock data system for development environment
- ✅ Implemented firestore_utils.py with fallback to mock data when Firestore unavailable
- ✅ All 5 travel packages (Thailand, Dubai, Phuket, Bali, Singapore) migrated from PostgreSQL
- ✅ All user accounts (3 regular users + 3 admin users) migrated with password hashes
- ✅ Homepage now loads successfully with featured packages from Firestore/mock data
- ✅ **FIXED AUTHENTICATION**: Updated all login/registration functions to use Firestore
- ✅ Fixed "Database connection failed" errors by replacing PostgreSQL calls with Firestore
- ✅ Google Sign-In backend handlers now properly connect to Firestore database
- ✅ Firebase service account credentials configured and working
- ✅ **CREATED USER ACCOUNTS**: Added/updated all requested admin and user accounts with specified credentials
- ✅ All accounts use password "Rajesh@123" and are stored in Firestore with proper password hashing
- ✅ **UPDATED USER CREDENTIALS**: Successfully updated all 6 user accounts with exact specifications:
  - Admin: rajesh4telecom@gmail.com (Rajesh Admin), admin@apniholidays.com (Apni Admin), rkm.ytw1@gmail.com (RKM-1 Admin)
  - Users: rkm.ytw2@gmail.com (RKM-2 User), rkm.ytw3@gmail.com (RKM-3 User), rkm.ytw4@gmail.com (RKM-4 User)
- ✅ All accounts verified working with "Rajesh@123" password in both Firestore and mock data systems

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Technology Stack**: HTML5, CSS3 (with CSS custom properties), Bootstrap framework, vanilla JavaScript
- **Design Pattern**: Progressive enhancement with responsive design
- **Component Structure**: Modular CSS and JavaScript files for maintainability
- **Loading Strategy**: Lazy loading for images and progressive loading with spinner

### Backend Architecture
- **Core Technology**: Flask/Python with Firestore integration
- **Hosting Platform**: Replit cloud hosting with PostgreSQL and Firestore support
- **Database**: Firestore (NoSQL) with mock data fallback for development
- **Architecture Pattern**: Flask MVC with Firestore utilities layer
- **Session Management**: Flask sessions for user state

### Data Storage Solutions
- **Primary Database**: Google Firestore for core data (packages, users, bookings)
- **Development Fallback**: Mock data system in Python when Firestore unavailable
- **File Storage**: External image hosting (ImgBB) for scalability
- **Authentication**: Firebase Authentication with email/password and Google Sign-In
- **Configuration**: Environment variables and Firebase configuration

## Key Components

### Admin Panel
- **DataTables Integration**: Advanced table management with search, sort, pagination
- **Bulk Operations**: Mass actions for efficient data management
- **Image Upload System**: Multi-service image hosting support
- **User Management**: Complete CRUD operations for user accounts
- **Package Management**: Full travel package lifecycle management

### Frontend Features
- **Responsive Design**: Mobile-first approach with Bootstrap integration
- **Interactive Elements**: Enhanced UI with tooltips, modals, and form validation
- **Search Functionality**: Real-time search capabilities
- **Performance Optimization**: Image lazy loading and progressive enhancement

### Authentication System
- **Optional Firebase Integration**: Modern authentication with fallback to PHP sessions
- **Role-based Access**: Admin and user role separation
- **Session Security**: Secure session management for user state persistence

## Data Flow

### User Journey
1. **Landing Page**: Users browse available travel packages
2. **Package Selection**: Detailed package views with booking capabilities
3. **User Registration/Login**: Account creation or authentication
4. **Booking Process**: Package reservation and payment handling
5. **Account Management**: User dashboard for booking history

### Admin Workflow
1. **Package Management**: Create, edit, delete travel packages
2. **User Administration**: Monitor and manage user accounts
3. **Booking Oversight**: Track and manage customer bookings
4. **Content Management**: Update website content and images

### Database Operations
- **Read Operations**: Package listings, user data retrieval
- **Write Operations**: New bookings, user registrations, package updates
- **Image Management**: Upload to external services, store references in database

## External Dependencies

### Required Services
- **Domain & Hosting**: apniholidays.com domain with GoDaddy shared hosting
- **Database**: MySQL/MariaDB via cPanel
- **Image Hosting**: ImgBB or Cloudinary for image storage and CDN

### Optional Integrations
- **Firebase**: Enhanced authentication and real-time features
- **Payment Gateways**: Integration ready for payment processing
- **Email Services**: SMTP configuration for notifications

### Frontend Libraries
- **Bootstrap**: Responsive framework and UI components
- **DataTables**: Advanced table functionality for admin panel
- **Font Awesome/Icons**: Icon system for enhanced UI

## Deployment Strategy

### Hosting Environment
- **Platform**: GoDaddy shared hosting with cPanel access
- **PHP Version**: 8.2+ required for optimal performance
- **Database**: MySQL setup via cPanel database management
- **File Structure**: Standard web hosting directory structure

### Configuration Requirements
- **Environment Setup**: PHP configuration for shared hosting limits
- **Database Connection**: cPanel MySQL credentials configuration
- **File Permissions**: Proper permissions for upload directories
- **SSL Certificate**: HTTPS configuration for secure operations

### Performance Considerations
- **Shared Hosting Optimization**: Code optimized for shared server limitations
- **Image Optimization**: External CDN usage to reduce server load
- **Caching Strategy**: Browser caching and static asset optimization
- **Database Optimization**: Efficient queries designed for shared hosting performance

### Maintenance Strategy
- **Backup Procedures**: Regular database and file backups
- **Update Management**: Version control for code updates
- **Monitoring**: Basic monitoring suitable for shared hosting environment
- **Security**: Regular security updates and vulnerability patching