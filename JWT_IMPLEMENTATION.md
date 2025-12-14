# JWT Token Authentication Implementation

## Overview

This Django e-commerce application now uses **JWT (JSON Web Tokens)** for persistent session management across the application. JWT tokens allow users to remain authenticated even after closing the browser, as long as the token hasn't expired.

## Features

### 1. **JWT Token Generation & Storage**
- Tokens are generated on user registration and login
- Both **access tokens** (60 minutes) and **refresh tokens** (7 days) are provided
- Tokens are stored in browser's `localStorage` for persistence across sessions

### 2. **Automatic Token Refresh**
- Access tokens expire in 60 minutes
- A background timer refreshes the access token every 50 minutes
- If refresh token expires, user is automatically logged out
- No manual logout needed due to token expiration

### 3. **Token-Based API Authentication**
- All API requests automatically include the JWT token in the `Authorization` header
- Format: `Authorization: Bearer <access_token>`
- Requests fall back to session authentication if no JWT token is available

### 4. **Logout Management**
- User can manually logout, which clears both JWT tokens and session
- Logout is permanent - tokens are removed from localStorage immediately
- User must login again to continue using authenticated features

---

## Implementation Details

### 1. **Backend Setup (Django)**

#### Installed Package
```bash
pip install djangorestframework-simplejwt
```

#### Settings Configuration (`django_ecommerce/settings.py`)

**Added to INSTALLED_APPS:**
```python
INSTALLED_APPS = [
    ...
    'rest_framework_simplejwt',
    ...
]
```

**Updated REST_FRAMEWORK authentication:**
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    ...
}
```

**JWT Configuration:**
```python
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

#### API Endpoints

**New JWT endpoints** (`/api/accounts/`):
- `POST /api/accounts/login/` - Login and get tokens
- `POST /api/accounts/register/` - Register and get tokens
- `POST /api/accounts/logout/` - Logout and invalidate tokens
- `POST /api/accounts/token/refresh/` - Refresh expired access token
- `POST /api/accounts/token/verify/` - Verify token validity

**Login Response Example:**
```json
{
    "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe"
    },
    "tokens": {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
    },
    "message": "Login successful."
}
```

#### Backend Views (`accounts/views.py`)

Updated `register_view()` and `login_view()` to return JWT tokens:

```python
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            },
            'message': 'Login successful.'
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

---

### 2. **Frontend Implementation (JavaScript)**

#### JWT Manager (`static/js/jwt-auth.js`)

A comprehensive JWT token management class:

**Key Methods:**
- `setTokens(accessToken, refreshToken)` - Store tokens in localStorage
- `getAccessToken()` - Retrieve access token
- `getRefreshToken()` - Retrieve refresh token
- `isAuthenticated()` - Check if user has valid token
- `refreshAccessToken()` - Refresh expired access token
- `logout()` - Clear all tokens
- `isTokenExpired(token)` - Check token expiration
- `decodeToken(token)` - Decode JWT payload without verification

**Automatic Token Refresh:**
```javascript
startTokenRefreshTimer() {
    // Refresh token every 50 minutes (before 60-min expiration)
    this.tokenCheckInterval = setInterval(() => {
        this.refreshAccessToken();
    }, 50 * 60 * 1000);
}
```

**Token Refresh Endpoint:**
```javascript
async refreshAccessToken() {
    const response = await fetch('/api/accounts/token/refresh/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh: this.getRefreshToken() })
    });
    // ...
}
```

#### Updated Templates

**Login Template** (`templates/login.html`):
```javascript
if (response.ok) {
    localStorage.setItem('user', JSON.stringify(data.user));
    // Store JWT tokens
    if (data.tokens) {
        jwtManager.setTokens(data.tokens.access, data.tokens.refresh);
    }
    window.location.href = '/';
}
```

**Register Template** (`templates/register.html`):
- Similar implementation to login
- Automatically logs user in after successful registration
- Redirects to home page instead of login page

#### API Request Enhancement (`static/js/home.js`)

Helper function to include JWT token in all API requests:

```javascript
function getAuthHeaders() {
    const headers = {
        'Content-Type': 'application/json',
    };
    
    const accessToken = localStorage.getItem('access_token');
    if (accessToken) {
        headers['Authorization'] = `Bearer ${accessToken}`;
    }
    
    return headers;
}
```

**Updated API Calls:**
```javascript
async function addToCart(productId) {
    const response = await fetch('/api/cart/cart/add_item/', {
        method: 'POST',
        headers: getAuthHeaders(),  // Includes JWT token
        credentials: 'include',
        body: JSON.stringify({
            product_id: productId,
            quantity: 1
        })
    });
    // ...
}
```

#### Logout Enhancement (`templates/base.html`)

Updated logout function to clear JWT tokens:

```javascript
async function logout() {
    const response = await fetch('/api/accounts/logout/', {
        method: 'POST',
        headers: headers,
        credentials: 'include',
    });
    
    if (response.ok) {
        if (typeof jwtManager !== 'undefined') {
            jwtManager.logout();  // Clear tokens
        }
        localStorage.removeItem('user');
        window.location.href = '/';
    }
}
```

---

## User Flow

### 1. **Registration Flow**
```
User fills registration form
    ↓
POST /api/accounts/register/
    ↓
Backend creates user and generates JWT tokens
    ↓
Frontend stores tokens in localStorage
    ↓
Auto-redirect to home page (already authenticated)
```

### 2. **Login Flow**
```
User enters email & password
    ↓
POST /api/accounts/login/
    ↓
Backend authenticates and generates JWT tokens
    ↓
Frontend stores tokens in localStorage
    ↓
JWT Manager starts token refresh timer
    ↓
Auto-redirect to home page (authenticated)
```

### 3. **Authenticated API Requests**
```
User clicks "Add to Cart"
    ↓
Frontend retrieves access token from localStorage
    ↓
Includes in header: Authorization: Bearer <token>
    ↓
POST /api/cart/cart/add_item/
    ↓
Backend validates JWT token
    ↓
If valid: Process request
If invalid: Return 401 Unauthorized
    ↓
Frontend catches 401 and redirects to login
```

### 4. **Token Refresh Flow**
```
JWT Manager timer fires every 50 minutes
    ↓
Frontend sends refresh token to /api/accounts/token/refresh/
    ↓
Backend validates refresh token and issues new access token
    ↓
Frontend updates access token in localStorage
    ↓
Token refresh timer restarts
```

### 5. **Logout Flow**
```
User clicks "Logout" button
    ↓
POST /api/accounts/logout/
    ↓
Backend invalidates session (optional)
    ↓
Frontend clears localStorage (JWT tokens)
    ↓
JWT Manager stops refresh timer
    ↓
Redirect to home page (unauthenticated)
```

---

## Token Details

### Access Token
- **Lifetime**: 60 minutes
- **Purpose**: Authenticate API requests
- **Storage**: localStorage as `access_token`
- **Used in**: `Authorization: Bearer <token>` header

### Refresh Token
- **Lifetime**: 7 days
- **Purpose**: Obtain new access token when it expires
- **Storage**: localStorage as `refresh_token`
- **Rotation**: Enabled - new refresh token issued on each refresh
- **Used in**: POST /api/accounts/token/refresh/

### Token Payload (Access Token)
```json
{
    "token_type": "access",
    "exp": 1702486200,        // Expiration timestamp (60 min from now)
    "iat": 1702482600,        // Issued at timestamp
    "jti": "abc123...",       // JWT ID
    "user_id": 1              // User ID
}
```

---

## Security Considerations

### 1. **HTTPS in Production**
- Always use HTTPS in production
- JWT tokens should only be sent over encrypted connections
- Set `Secure` flag on cookies if using session auth alongside JWT

### 2. **Token Storage**
- Tokens are stored in localStorage (accessible to JavaScript)
- Alternative: Store in HTTP-only cookies (safer but requires different implementation)
- Current implementation: Suitable for SPAs where XSS protection is in place

### 3. **Token Expiration**
- Access tokens expire in 60 minutes
- Automatic refresh ensures seamless user experience
- Refresh tokens expire in 7 days - require re-login after that

### 4. **CSRF Protection**
- Django CSRF middleware still active
- Session authentication still available as fallback
- Forms and POST requests include CSRF token

### 5. **Logout Implementation**
- Logout clears tokens from frontend
- Backend invalidates session (if session auth is used)
- Refresh token rotation adds extra security

---

## Testing JWT Authentication

### 1. **Manual Testing with curl**

**Register:**
```bash
curl -X POST http://localhost:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

**Use Access Token:**
```bash
curl -X GET http://localhost:8000/api/cart/cart/ \
  -H "Authorization: Bearer <access_token>"
```

**Refresh Token:**
```bash
curl -X POST http://localhost:8000/api/accounts/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "<refresh_token>"}'
```

### 2. **Browser Testing**

1. Open Developer Tools (F12)
2. Go to Application → LocalStorage
3. Register or login
4. Verify `access_token` and `refresh_token` are stored
5. Open Console and check for token refresh logs
6. Test authenticated operations (add to cart, etc.)
7. Logout and verify tokens are cleared

### 3. **Token Expiration Testing**

In jwt-auth.js, temporarily change:
```javascript
'ACCESS_TOKEN_LIFETIME': timedelta(minutes=1),  // 1 minute for testing
```

Then:
1. Login
2. Wait 2+ minutes
3. Verify automatic token refresh occurs
4. Check new token in localStorage

---

## Troubleshooting

### Issue: "401 Unauthorized" on API requests
- **Cause**: Token expired or not included in request
- **Solution**: 
  - Logout and login again
  - Check browser console for errors
  - Verify `getAuthHeaders()` is being used

### Issue: Token doesn't refresh automatically
- **Cause**: JWT Manager not initialized
- **Solution**: 
  - Ensure jwt-auth.js is loaded before home.js
  - Check browser console for initialization messages
  - Verify localStorage contains tokens

### Issue: "Cannot read property 'refresh' of undefined"
- **Cause**: Refresh endpoint not returning new token
- **Solution**:
  - Verify SIMPLE_JWT config in settings.py
  - Check Django server logs for errors
  - Ensure djangorestframework-simplejwt is installed

### Issue: User stays logged in after closing browser
- **Expected**: This is correct behavior!
- **Info**: Tokens in localStorage persist across sessions
- **How to clear**: User must explicitly logout or clear browser data

---

## Configuration

### Customizing Token Lifetime

Edit `django_ecommerce/settings.py`:

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),   # Shorter expiration
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),     # Longer refresh period
    'ROTATE_REFRESH_TOKENS': True,                    # Rotate on each refresh
    ...
}
```

Then update the refresh timer in `static/js/jwt-auth.js`:

```javascript
// Adjust to match ACCESS_TOKEN_LIFETIME (use 80% of lifetime)
setInterval(() => {
    this.refreshAccessToken();
}, 24 * 60 * 1000);  // 24 minutes for 30-min tokens
```

### Using HTTP-Only Cookies (Advanced)

For better security, store tokens in HTTP-only cookies instead of localStorage:

1. Update backend settings
2. Remove localStorage usage from jwt-auth.js
3. Implement cookie extraction for Authorization header
4. Requires backend to set Set-Cookie headers

---

## Files Modified/Created

### Created:
- `static/js/jwt-auth.js` - JWT token management class

### Modified:
- `django_ecommerce/settings.py` - JWT configuration
- `accounts/views.py` - Updated login/register to return tokens
- `accounts/urls.py` - Added token refresh/verify endpoints
- `templates/login.html` - Store JWT tokens after login
- `templates/register.html` - Store JWT tokens after registration
- `templates/base.html` - Include jwt-auth.js, update logout
- `templates/product_detail.html` - Use JWT tokens in API calls
- `static/js/home.js` - Add getAuthHeaders() helper, use JWT in API calls

---

## Summary

This implementation provides:
- ✅ Persistent authentication across sessions
- ✅ Automatic token refresh without user intervention
- ✅ Secure token storage in localStorage
- ✅ Seamless user experience with 60-minute token lifetime
- ✅ Backward compatibility with session authentication
- ✅ Proper logout and token cleanup
- ✅ Clear separation between frontend and backend authentication

Users can now:
- Stay logged in for 7 days (refresh token lifetime)
- Automatic token refresh every 50 minutes
- Manual logout to clear tokens immediately
- Authenticated API requests using JWT bearer tokens
