# Auth Testing Playbook

## Test Steps

1. **Backend Auth Testing**: Test JWT auth endpoints and Google OAuth flow
2. **Session Management**: Test session creation, validation, and expiry
3. **Protected Endpoints**: Test that protected routes require authentication

## Test Credentials
See `/app/memory/test_credentials.md` for login credentials

## Backend Auth Endpoints to Test
- POST `/api/auth/signup` - Create new user with email/password
- POST `/api/auth/login` - Login with email/password
- POST `/api/auth/google/session` - Exchange Google session_id for app session
- GET `/api/auth/me` - Get current user (requires auth)
- POST `/api/auth/logout` - Logout and clear session
