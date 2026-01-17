# Security Documentation - PrepWise

This document outlines the security measures implemented in the PrepWise application and provides guidelines for maintaining security best practices.

## Table of Contents

1. [Security Features Implemented](#security-features-implemented)
2. [OWASP Top 10 Compliance](#owasp-top-10-compliance)
3. [API Security](#api-security)
4. [Authentication & Authorization](#authentication--authorization)
5. [Data Protection](#data-protection)
6. [File Upload Security](#file-upload-security)
7. [Security Configuration](#security-configuration)
8. [Deployment Security Checklist](#deployment-security-checklist)
9. [Incident Response](#incident-response)
10. [Security Contacts](#security-contacts)

---

## Security Features Implemented

### 1. Rate Limiting (OWASP API4:2023)

**Location**: `/backend/app/middleware/rate_limit.py`

Comprehensive rate limiting on all endpoints to prevent:
- Brute force attacks on authentication endpoints
- Denial of Service (DoS) attacks
- API abuse and resource exhaustion

**Rate Limits**:
- Login attempts: 10 requests/minute per IP
- Registration: 5 requests/5 minutes per IP
- Password reset: 3 requests/hour per IP
- File uploads: 20 requests/hour per IP
- AI endpoints: 30-50 requests/hour per IP
- Authenticated endpoints: 100 requests/minute per IP
- Public endpoints: 30 requests/minute per IP

**Features**:
- IP-based rate limiting
- User-based rate limiting for authenticated endpoints
- Graceful 429 responses with `Retry-After` headers
- Rate limit information in response headers

### 2. Input Validation & Sanitization (OWASP API8:2023)

**Location**: `/backend/app/schemas/`

All user inputs are validated using Pydantic schemas with:

**Authentication Inputs**:
- Email: Valid format, max 255 characters
- Name: 1-255 characters, alphanumeric + safe chars only
- Password: 8-72 characters, complexity requirements, weak password detection
- Tokens: Alphanumeric only, length validation

**AI Inputs**:
- Transcript: Max 50,000 characters to prevent memory exhaustion
- Company name: Alphanumeric + safe characters only
- Question count: Limited to 1-20 questions
- No unexpected fields accepted (`extra='forbid'`)

**Payment Inputs**:
- URL validation to prevent open redirect attacks
- Plan validation against enum values
- Strict type checking on all fields

**File Uploads**:
- Filename sanitization (prevent path traversal)
- File type whitelist (PDF, DOC, DOCX)
- File size limits (10MB max)
- Magic number validation (prevent malicious files)
- Content-type verification

### 3. Secure API Key Handling

**Actions Taken**:
1. ✓ Removed all hardcoded API keys from `.env` files
2. ✓ Created comprehensive `.env.example` files with placeholders
3. ✓ Added security warnings in environment files
4. ✓ Documented key rotation policies
5. ✓ Separated frontend (public) and backend (private) keys

**Key Rotation Policy**:
- Rotate all API keys every 90 days
- Immediately rotate if key is exposed or compromised
- Use separate keys for development, staging, and production
- Monitor API usage for anomalies

**Environment Variables**:
- Backend: All sensitive keys in `.env` (NEVER committed)
- Frontend: Only public configuration in `NEXT_PUBLIC_*` variables
- Production: Use AWS Secrets Manager or similar service

### 4. Security Headers (OWASP A05:2021)

**Location**: `/backend/main.py` - `add_security_headers` middleware

Implements comprehensive security headers:

```
X-Content-Type-Options: nosniff              # Prevent MIME sniffing
X-Frame-Options: DENY                        # Prevent clickjacking
X-XSS-Protection: 1; mode=block             # Enable XSS filter
Content-Security-Policy: ...                 # Prevent XSS attacks
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), ...      # Restrict browser features
Strict-Transport-Security: max-age=31536000  # Force HTTPS (production only)
```

### 5. CORS Protection

**Location**: `/backend/main.py`

- Whitelist approach for allowed origins
- No wildcard (`*`) in production
- Explicit allowed methods only
- Credentials support with strict origin validation
- Warning logged if wildcard used in production

### 6. File Upload Security

**Location**: `/backend/app/utils/file_utils.py`

**Security Measures**:
1. **Filename Sanitization**:
   - Remove path traversal attempts (`../`, etc.)
   - Strip null bytes
   - Allow only safe characters
   - Prevent hidden files

2. **File Type Validation**:
   - Whitelist approach (PDF, DOC, DOCX only)
   - Extension validation
   - Magic number verification
   - Content-type checking

3. **File Size Limits**:
   - 10MB maximum per file
   - 413 Payload Too Large response

4. **Path Traversal Prevention**:
   - Validate final path within upload directory
   - Sanitize subdirectory names
   - Use absolute path resolution

5. **Secure Storage**:
   - Unique UUID-based filenames
   - Restrictive file permissions (0o600)
   - Cleanup on save failure

### 7. Authentication Security

**JWT Token Security**:
- HS256 algorithm (configurable)
- 30-minute token expiration
- Secure token payload (minimal data)
- Token validation on every request

**Password Security**:
- bcrypt hashing (cost factor: default)
- 72-byte maximum (bcrypt limit)
- 8-character minimum
- Weak password detection
- No password storage in logs

**Session Security**:
- HTTP-only cookies (when applicable)
- Secure flag in production
- SameSite attribute
- Session timeout: 24 hours

---

## OWASP Top 10 Compliance

### Implemented Protections

| OWASP Risk | Implementation | Location |
|------------|----------------|----------|
| **A01:2021 - Broken Access Control** | JWT authentication, user validation on protected routes | `/backend/app/api/routes/auth.py` |
| **A02:2021 - Cryptographic Failures** | bcrypt password hashing, secure token generation | `/backend/app/utils/auth.py` |
| **A03:2021 - Injection** | Pydantic validation, parameterized queries (SQLAlchemy ORM) | `/backend/app/schemas/` |
| **A04:2021 - Insecure Design** | Rate limiting, input validation, secure file handling | Throughout |
| **A05:2021 - Security Misconfiguration** | Security headers, strict CORS, environment-based config | `/backend/main.py` |
| **A06:2021 - Vulnerable Components** | Regular dependency updates via `requirements.txt` | `/backend/requirements.txt` |
| **A07:2021 - Authentication Failures** | Strong password policy, rate limiting, token expiration | `/backend/app/api/routes/auth.py` |
| **A08:2021 - Data Integrity Failures** | Input validation, schema enforcement | `/backend/app/schemas/` |
| **A09:2021 - Logging Failures** | Comprehensive logging, security event tracking | `/backend/app/core/logging.py` |
| **A10:2021 - SSRF** | URL validation, restricted file access | `/backend/app/schemas/payment_schemas.py` |

### OWASP API Security Top 10

| API Risk | Implementation | Status |
|----------|----------------|--------|
| **API1:2023 - Broken Object Level Authorization** | User ID validation in all endpoints | ✓ |
| **API2:2023 - Broken Authentication** | JWT, rate limiting, strong passwords | ✓ |
| **API3:2023 - Broken Object Property Level Authorization** | Pydantic schemas with `extra='forbid'` | ✓ |
| **API4:2023 - Unrestricted Resource Consumption** | Rate limiting, file size limits | ✓ |
| **API5:2023 - Broken Function Level Authorization** | Role-based access checks | ✓ |
| **API6:2023 - Unrestricted Access to Sensitive Flows** | Rate limiting on sensitive endpoints | ✓ |
| **API7:2023 - Server Side Request Forgery** | URL validation in payment callbacks | ✓ |
| **API8:2023 - Security Misconfiguration** | Security headers, strict config | ✓ |
| **API9:2023 - Improper Inventory Management** | API documentation, version control | ✓ |
| **API10:2023 - Unsafe Consumption of APIs** | API key restrictions, monitoring | ✓ |

---

## API Security

### Endpoint Security Levels

**Public Endpoints** (No authentication required):
- `/health` - Health check
- `/api/v1/auth/login` - Login (rate limited: 10/min)
- `/api/v1/auth/register` - Registration (rate limited: 5/5min)
- `/api/v1/auth/forgot-password` - Password reset (rate limited: 3/hour)

**Authenticated Endpoints** (JWT required):
- `/api/v1/auth/me` - User profile
- `/api/v1/ai/*` - AI operations (rate limited)
- `/api/v1/payments/*` - Payment operations (rate limited)
- `/api/v1/dashboard/*` - Dashboard data

**Webhook Endpoints** (Signature verification):
- `/api/v1/payments/webhook` - Stripe webhooks (signature verified)

### API Key Security

**Backend API Keys** (NEVER exposed to client):
- `OPENAI_API_KEY` - OpenAI API access
- `STRIPE_SECRET_KEY` - Stripe payment processing
- `AWS_SECRET_ACCESS_KEY` - AWS services
- `SECRET_KEY` - JWT signing

**Frontend API Keys** (Client-exposed, restricted):
- `NEXT_PUBLIC_FOUNDRY_ENDPOINT` - Microsoft Foundry project endpoint URL
- `NEXT_PUBLIC_FOUNDRY_API_KEY` - Microsoft Foundry API key (with domain restrictions)
- `NEXT_PUBLIC_AZURE_SPEECH_KEY` - Azure Speech Services key (with domain restrictions)
- `NEXT_PUBLIC_AZURE_SPEECH_REGION` - Azure Speech Services region

**Security Measures**:
- Enable API key restrictions (IP whitelist, domain restrictions)
- Monitor usage and set alerts
- Rotate keys on schedule or if exposed
- Use separate keys per environment

---

## Authentication & Authorization

### Authentication Flow

1. **Registration**:
   - Email verification required
   - Password hashed with bcrypt
   - Verification token sent via email
   - Token expires in 24 hours

2. **Login**:
   - Email verification check
   - Password verification
   - JWT token generation
   - Token includes user ID and email
   - 30-minute token expiration

3. **Password Reset**:
   - Rate limited (3/hour)
   - Reset token via email
   - Token expires in 1 hour
   - One-time use token

### Authorization Patterns

```python
# Protecting endpoints with JWT
from app.api.routes.auth import get_current_user

@router.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    # Only authenticated users can access
    return {"user_id": current_user.id}
```

---

## Data Protection

### Sensitive Data Handling

**Passwords**:
- Never stored in plaintext
- bcrypt hashing with salt
- Never logged or exposed in responses
- 72-byte maximum (bcrypt limit)

**Personal Information**:
- Email addresses validated and normalized
- Names sanitized for safe characters
- No sensitive data in logs or error messages
- GDPR-compliant data handling

**API Keys & Secrets**:
- Stored in environment variables
- Never committed to version control
- Separate keys per environment
- Regular rotation schedule

### Database Security

**SQLAlchemy ORM Benefits**:
- Automatic SQL injection prevention via parameterized queries
- Type safety and validation
- No raw SQL queries exposed

**Connection Security**:
- PostgreSQL with SSL in production
- Strong database passwords
- Limited database user permissions
- Regular backups

---

## File Upload Security

### Allowed File Types

**Resume Uploads**:
- PDF (`.pdf`)
- Word Documents (`.doc`, `.docx`)

**Audio Files** (for voice responses):
- MP3 (`.mp3`)
- WAV (`.wav`)
- WebM (`.webm`)

### Security Validations

1. **Extension Check**: Whitelist approach
2. **Magic Number Validation**: Verify file content matches extension
3. **Size Limit**: 10MB maximum
4. **Filename Sanitization**: Remove dangerous characters
5. **Path Traversal Prevention**: Validate final path
6. **Unique Naming**: UUID-based filenames
7. **Permissions**: Restricted file permissions (0o600)

### Upload Directory Structure

```
./uploads/
  ├── resumes/
  │   └── resume_<uuid>.pdf
  ├── responses/
  │   └── response_<uuid>.mp3
  └── ...
```

---

## Security Configuration

### Environment Variables

**Required for Production**:
```bash
# CRITICAL - Change these!
SECRET_KEY=<strong-random-value>
DATABASE_URL=postgresql://...
OPENAI_API_KEY=sk-...
STRIPE_SECRET_KEY=sk_live_...

# Security Settings
DEBUG=False
ENVIRONMENT=production
CORS_ORIGINS=https://yourdomain.com
TRUSTED_HOSTS=yourdomain.com
```

**Generate Secure Secret Key**:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Production Configuration Checklist

- [ ] `DEBUG=False`
- [ ] `ENVIRONMENT=production`
- [ ] Strong `SECRET_KEY`
- [ ] Production database (PostgreSQL with SSL)
- [ ] Specific `CORS_ORIGINS` (no wildcards)
- [ ] `TRUSTED_HOSTS` configured
- [ ] HTTPS enabled
- [ ] Production API keys (Stripe `sk_live_`, etc.)
- [ ] Email service configured (AWS SES)
- [ ] Redis for caching and rate limiting
- [ ] Monitoring and alerting set up
- [ ] Regular backups enabled
- [ ] SSL certificate valid

---

## Deployment Security Checklist

### Pre-Deployment

- [ ] Security audit completed
- [ ] Dependencies updated and scanned
- [ ] Environment variables validated
- [ ] API keys rotated
- [ ] HTTPS certificate obtained
- [ ] Firewall rules configured
- [ ] Database backups tested

### Post-Deployment

- [ ] Security headers verified (check with securityheaders.com)
- [ ] Rate limiting tested
- [ ] SSL/TLS configuration verified (check with ssllabs.com)
- [ ] CORS policy tested
- [ ] Error handling reviewed (no sensitive data in errors)
- [ ] Logging and monitoring active
- [ ] Incident response plan documented

### Ongoing Security

- [ ] Weekly dependency updates
- [ ] Monthly security audits
- [ ] Quarterly API key rotation
- [ ] Regular penetration testing
- [ ] Security awareness training
- [ ] Incident response drills

---

## Incident Response

### If API Key is Exposed

1. **Immediate Actions**:
   - Rotate the exposed key immediately
   - Revoke the old key in the provider's dashboard
   - Update all environments with new key
   - Review API usage logs for unauthorized access

2. **Investigation**:
   - Identify how the key was exposed
   - Check for unauthorized API usage
   - Review access logs for suspicious activity
   - Document the incident

3. **Remediation**:
   - Fix the exposure vector
   - Implement additional safeguards
   - Update documentation
   - Team notification and training

### If Security Breach Detected

1. **Contain**: Isolate affected systems
2. **Assess**: Determine scope and impact
3. **Eradicate**: Remove threat and vulnerabilities
4. **Recover**: Restore systems from clean backups
5. **Document**: Record incident details
6. **Review**: Post-incident analysis and improvements

### Security Contacts

**Report Security Issues**:
- Email: security@yourdomain.com
- Encrypted: PGP key available at /security/pgp-key.txt
- Response Time: 24 hours for critical issues

**Responsible Disclosure**:
We appreciate responsible disclosure of security vulnerabilities.
Please do not publicly disclose until we've had time to address.

---

## Security Monitoring

### Logging

**Security Events Logged**:
- Failed login attempts
- Rate limit violations
- Invalid file uploads
- Authentication failures
- API key usage anomalies
- Database query errors

**Log Retention**:
- Production: 90 days minimum
- Security events: 1 year minimum

### Monitoring Alerts

**Critical Alerts**:
- Multiple failed login attempts
- Rate limit threshold exceeded
- Unusual API usage patterns
- Database connection failures
- SSL certificate expiration

---

## Security Tools & Resources

### Recommended Tools

**Static Analysis**:
- `bandit` - Python security linter
- `safety` - Dependency vulnerability scanner
- `npm audit` - Node.js dependency scanner

**Dynamic Testing**:
- OWASP ZAP - Web application security scanner
- Burp Suite - Security testing platform

**Monitoring**:
- Sentry - Error tracking
- DataDog - Application monitoring
- CloudFlare - DDoS protection

### Security References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [CWE Top 25](https://cwe.mitre.org/top25/)

---

## Updates & Changelog

### Security Updates

**2026-01-10**:
- ✓ Implemented comprehensive rate limiting
- ✓ Enhanced input validation on all schemas
- ✓ Secured API key handling
- ✓ Added security headers
- ✓ Implemented file upload security
- ✓ Created security documentation

**Future Enhancements**:
- [ ] Implement Redis-backed rate limiting for distributed deployments
- [ ] Add two-factor authentication (2FA)
- [ ] Implement API key rotation automation
- [ ] Add security scanning in CI/CD pipeline
- [ ] Implement Content Security Policy reporting
- [ ] Add automated vulnerability scanning

---

## License & Compliance

This security documentation is part of the PrepWise project and is subject to the same license terms.

**Compliance**:
- GDPR considerations for EU users
- CCPA compliance for California users
- PCI DSS for payment processing (via Stripe)
- SOC 2 considerations for enterprise customers

---

**Last Updated**: 2026-01-10
**Next Review**: 2026-02-10
**Version**: 1.0
