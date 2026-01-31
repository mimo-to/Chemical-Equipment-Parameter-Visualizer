# Authentication Behavior and Boundaries

## Authentication Requirement

**Mandate:** Basic authentication must protect API endpoints

**Method:** Token-based authentication using Django REST Framework

**Scope:** All endpoints except login endpoint

## Authentication System

### Technology

**Framework:** Django REST Framework (DRF)

**Auth Class:** `TokenAuthentication`

**Token Storage:** Database table managed by `rest_framework.authtoken` app

### User Model

**Model:** Django's built-in `User` model

**Import:** `from django.contrib.auth.models import User`

**Fields Used:**

- `username`: String, unique
- `password`: String, hashed
- `id`: Integer, auto-increment

## Token Generation

### Login Endpoint

**Endpoint:** POST /api/login/

**Authentication Required:** No

**Purpose:** Generate authentication token for valid credentials

### Request Format

**Headers:**

```
Content-Type: application/json
```

**Body:**

```json
{
    "username": "testuser",
    "password": "testpassword"
}
```

### Validation Process

**Step 1:** Extract username and password from request body

**Step 2:** Validate both fields are present

**Error if missing:** 400 Bad Request

```json
{
    "error": "Username and password required"
}
```

**Step 3:** Authenticate using Django's authenticate function

```python
from django.contrib.auth import authenticate

user = authenticate(username=username, password=password)
```

**Step 4:** Check if authentication succeeded

**If user is None:** 401 Unauthorized

```json
{
    "error": "Invalid credentials"
}
```

**Step 5:** Retrieve or create token for authenticated user

```python
from rest_framework.authtoken.models import Token

token, created = Token.objects.get_or_create(user=user)
```

**Step 6:** Return token in response

### Success Response

**Status Code:** 200 OK

**Body:**

```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "user_id": 1,
    "username": "testuser"
}
```

**Token Format:** 40-character hexadecimal string

## Token Usage

### Request Header

**Header Name:** `Authorization`

**Header Value:** `Token <token_value>`

**Example:**

```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

### Token Validation Process

**Step 1:** DRF extracts Authorization header from request

**Step 2:** Parse header to extract token value

**Step 3:** Query database for matching token

```python
token_obj = Token.objects.get(key=token_value)
```

**Step 4:** Retrieve associated user

```python
user = token_obj.user
```

**Step 5:** Attach user to request object

```python
request.user = user
```

**Step 6:** Allow request to proceed to view

### Token Validation Failure

**Missing Header:** 401 Unauthorized

```json
{
    "error": "Authentication credentials were not provided"
}
```

**Invalid Token:** 401 Unauthorized

```json
{
    "error": "Invalid token"
}
```

**Malformed Header:** 401 Unauthorized

```json
{
    "error": "Invalid token header"
}
```

## Protected Endpoints

### Endpoints Requiring Authentication

- POST /api/upload/
- GET /api/history/
- GET /api/dataset/<int:id>/
- GET /api/dataset/<int:id>/visualization/
- GET /api/report/<int:id>/

### Authentication Enforcement

**Configuration:** Apply `authentication_classes` and `permission_classes` to views

```python
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class UploadView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
```

**Behavior:**

- Request without valid token: 401 Unauthorized
- Request with valid token: Proceed to view logic

## Unprotected Endpoints

### Login Endpoint Only

**Endpoint:** POST /api/login/

**Reason:** Must allow unauthenticated access to obtain token

**Configuration:** No authentication_classes or permission_classes

```python
class LoginView(APIView):
    pass
```

## User Creation

### Development Setup

**Requirement:** Create at least one user for testing

**Method:** Django management command

```bash
python manage.py createsuperuser
```

**Prompts:**

- Username
- Email (optional)
- Password

**Alternative:** Create user programmatically in Django shell

```python
from django.contrib.auth.models import User

user = User.objects.create_user(
    username='testuser',
    password='testpassword'
)
```

### Production Considerations

**Not Specified:** Task does not require user registration endpoint

**Acceptable:** Manually create users via Django admin or management command

## Token Lifecycle

### Token Creation

**Trigger:** First successful login for user

**Storage:** Persisted in `authtoken_token` table

**Reuse:** Same token returned for subsequent logins

### Token Expiration

**Not Required:** Task does not specify token expiration

**Behavior:** Tokens remain valid indefinitely

**Optional Enhancement:** May implement expiration if desired

### Token Revocation

**Not Required:** Task does not specify logout or token deletion

**Behavior:** Tokens cannot be revoked through API

**Manual Revocation:** Delete token from database using Django admin or shell

## Frontend Authentication Flow

### Web Frontend (React)

**Step 1:** Display login form

**Step 2:** User enters username and password

**Step 3:** Send POST to /api/login/

**Step 4:** Receive token in response

**Step 5:** Store token in browser (localStorage or sessionStorage)

**Step 6:** Include token in Authorization header for all subsequent requests

**Step 7:** On 401 response, redirect to login

### Desktop Frontend (PyQt5)

**Step 1:** Display login dialog

**Step 2:** User enters username and password

**Step 3:** Send POST to /api/login/

**Step 4:** Receive token in response

**Step 5:** Store token in memory or application settings

**Step 6:** Include token in Authorization header for all subsequent requests

**Step 7:** On 401 response, show login dialog again

## Security Considerations

### Password Storage

**Method:** Django's default password hashing (PBKDF2)

**Configuration:** Automatic, no additional setup required

**Security:** Passwords never stored in plaintext

### Token Security

**Transmission:** HTTPS recommended in production

**Storage:** Client-side storage (localStorage, memory)

**Exposure Risk:** Token grants full access until revoked

### CORS Configuration

**Requirement:** Configure allowed origins for web frontend

**Setting:** CORS_ALLOWED_ORIGINS in Django settings

**Development Example:**

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
```

## Error Response Standardization

### Authentication Errors

All authentication failures return 401 Unauthorized with JSON body containing error message.

**Examples:**

```json
{
    "error": "Authentication credentials were not provided"
}
```

```json
{
    "error": "Invalid token"
}
```

```json
{
    "error": "Invalid credentials"
}
```

## Multi-User Support

### User Isolation

[Clarification Added: Explicit specification of dataset visibility scope]

**Dataset Visibility:** All datasets are globally visible to all authenticated users

**Behavior:** Any authenticated user can access, view, and download reports for any dataset uploaded by any user

**Implication:** Datasets are shared across all authenticated users; there is no user-specific data isolation

**Specification Basis:** Task does not require user-specific data filtering or ownership

### Alternative Interpretation

**If Desired:** Filter datasets by user who uploaded them

**Implementation:** Add `user` foreign key to EquipmentDataset model

**Query Modification:** Filter by `request.user` in views

**Note:** Task specification does not require this

## Testing Authentication

### Test User Creation

Create test user before running tests:

```bash
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.create_user('testuser', password='testpassword')
```

### Test Login

```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpassword"}'
```

Expected response:

```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "user_id": 1,
    "username": "testuser"
}
```

### Test Protected Endpoint

```bash
curl -X GET http://localhost:8000/api/history/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

Expected: 200 OK with history data

### Test Unauthorized Access

```bash
curl -X GET http://localhost:8000/api/history/
```

Expected: 401 Unauthorized

## Django Settings Configuration

### Required Settings

**INSTALLED_APPS:** Include `rest_framework.authtoken`

```python
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'rest_framework',
    'rest_framework.authtoken',
    'api',
]
```

**REST_FRAMEWORK:** Configure default authentication

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}
```

### Database Migration

Run migration to create authtoken table:

```bash
python manage.py migrate
```

This creates `authtoken_token` table with columns:

- key: 40-character token string
- user_id: Foreign key to auth_user table
- created: Timestamp

## Authentication Boundary Summary

### What IS Required

- Token-based authentication
- Login endpoint to obtain token
- All endpoints except login require authentication
- 401 error for unauthenticated requests
- Token returned on successful login

### What IS NOT Required

- Token expiration
- Token refresh
- Logout endpoint
- User registration endpoint
- Password reset
- Multi-factor authentication
- Role-based access control
- User-specific data filtering
