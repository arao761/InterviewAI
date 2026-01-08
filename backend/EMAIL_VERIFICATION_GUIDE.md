# Email Verification Troubleshooting Guide

## Problem Prevention

This guide helps prevent and resolve email verification issues.

## New Features Added

### 1. **Email Status in Registration Response**
   - Registration now returns `email_sent: boolean` status
   - Frontend can detect if email failed to send
   - Allows for better user feedback

### 2. **Admin Endpoints** (`/api/v1/admin/`)
   - `POST /admin/verify-user` - Manually verify a user
   - `GET /admin/unverified-users` - List all unverified users
   - `GET /admin/smtp-health` - Check SMTP configuration
   - `GET /admin/user/{email}` - Get user info by email

### 3. **Manual Verification Scripts**
   - `manually_verify_user.py` - Verify users from command line
   - `get_verification_token.py` - Get verification tokens/URLs

## How to Use

### Check SMTP Health
```bash
curl http://localhost:8000/api/v1/admin/smtp-health
```

### Manually Verify a User (API)
```bash
curl -X POST http://localhost:8000/api/v1/admin/verify-user \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com"}'
```

### Manually Verify a User (Script)
```bash
cd backend
python manually_verify_user.py user@example.com
```

### List Unverified Users
```bash
curl http://localhost:8000/api/v1/admin/unverified-users
```

### Get Verification Token
```bash
cd backend
python get_verification_token.py user@example.com
```

## Monitoring & Prevention

### 1. **Regular SMTP Health Checks**
   - Set up a cron job or monitoring service to check `/admin/smtp-health`
   - Alert if SMTP is not configured or cannot connect

### 2. **Monitor Unverified Users**
   - Regularly check `/admin/unverified-users`
   - If many unverified users accumulate, investigate SMTP issues

### 3. **Check Backend Logs**
   - Look for warnings: "Verification email NOT sent (SMTP not configured)"
   - Look for errors: "SMTP Authentication failed" or "SMTP error"

### 4. **Environment Variables**
   Ensure these are set in production (Render dashboard):
   - `SMTP_USER` - Your email address
   - `SMTP_PASSWORD` - Your email app password
   - `FROM_EMAIL` - Sender email (defaults to SMTP_USER)
   - `FRONTEND_URL` - Frontend URL for verification links

## Production Checklist

- [ ] SMTP environment variables configured in Render
- [ ] SMTP health check returns `configured: true, can_connect: true`
- [ ] Test registration and verify email is received
- [ ] Set up monitoring for SMTP health
- [ ] Document admin endpoint access (add authentication in production)

## Troubleshooting Steps

1. **Check SMTP Health**
   ```bash
   curl https://your-backend.onrender.com/api/v1/admin/smtp-health
   ```

2. **Check Unverified Users**
   ```bash
   curl https://your-backend.onrender.com/api/v1/admin/unverified-users
   ```

3. **Manually Verify Affected Users**
   ```bash
   curl -X POST https://your-backend.onrender.com/api/v1/admin/verify-user \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com"}'
   ```

4. **Check Render Logs**
   - Go to Render dashboard → Your service → Logs
   - Search for "SMTP" or "verification email"

## Security Note

⚠️ **Important**: The admin endpoints are currently unprotected. In production, you should:
- Add authentication/authorization middleware
- Restrict access to admin users only
- Use API keys or JWT tokens
- Consider IP whitelisting

Example protection:
```python
from fastapi import Depends, HTTPException, status
from app.utils.auth import get_current_user

@router.post("/verify-user")
async def manually_verify_user(
    request: ManualVerifyRequest,
    current_user: User = Depends(get_current_user),  # Require auth
    db: Session = Depends(get_db)
):
    # Add admin check
    if not current_user.is_admin:  # Add this field to User model
        raise HTTPException(status_code=403, detail="Admin access required")
    # ... rest of function
```

