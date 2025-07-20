# User Credentials Summary

## Admin Credentials
All admin accounts have `user_role = Admin` and password `Rajesh@123`

| Username/Email | Password | Full Name | Role |
|---|---|---|---|
| rajesh4telecom@gmail.com | Rajesh@123 | Rajesh (Admin) | Admin |
| admin@apniholidays.com | Rajesh@123 | Apni (Admin) | Admin |
| rkm.ytw1@gmail.com | Rajesh@123 | RKM-1 (Admin) | Admin |

## User Credentials
All user accounts have `user_role = User` and password `Rajesh@123`

| Username/Email | Password | Full Name | Role |
|---|---|---|---|
| rkm.ytw2@gmail.com | Rajesh@123 | RKM-2 (User) | User |
| rkm.ytw3@gmail.com | Rajesh@123 | RKM-3 (User) | User |
| rkm.ytw4@gmail.com | Rajesh@123 | RKM-4 (User) | User |

## Status
- ✅ All 6 accounts successfully created/updated in Firestore database
- ✅ All accounts verified working with authentication system
- ✅ Password hashing implemented using Werkzeug security
- ✅ Both admin and user role access confirmed working
- ✅ Fallback mock data system also updated for development environment

## Login URLs
- User Login: `/auth/login` 
- Admin Login: `/admin/login`

## Notes
- All accounts are set to `status = 'active'`
- Phone numbers assigned incrementally for organization
- Firebase UID left empty for traditional email/password authentication
- Accounts work with both Firestore (production) and mock data (development)