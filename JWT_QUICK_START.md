# Quick Start Guide - JWT Authentication

## What Changed?

Your e-commerce application now uses **JWT (JSON Web Tokens)** for authentication instead of just session-based auth. This means users stay logged in even after closing their browser!

---

## How It Works (For Users)

### Before (Session-Based)
```
User logs in → Session created → Close browser → Session lost → Must login again
```

### Now (JWT-Based)
```
User logs in → Tokens stored locally → Close browser → Reopen → Still logged in! ✅
```

---

## User Experience

### Registration
1. Fill out registration form
2. Click "Register"
3. **Automatically logged in** and redirected to home page
4. No need to manually login after registration

### Login
1. Enter email and password
2. Click "Login"
3. **Immediately logged in** with JWT tokens stored
4. Tokens persist across browser sessions

### Shopping
1. Browse products normally
2. Click "Add to Cart" - works with JWT authentication
3. Your authentication stays active for up to **7 days**

### Logout
1. Click "Logout" button
2. JWT tokens immediately cleared
3. Session ended
4. Must login again to access protected features

---

## What Are These Tokens?

### Access Token
- **How long it lasts**: 60 minutes
- **What it does**: Proves you're logged in for API requests
- **Automatically refreshed**: Every 50 minutes (you won't notice!)

### Refresh Token
- **How long it lasts**: 7 days
- **What it does**: Gets you a new access token when it expires
- **Storage**: Saved in your browser

### Token Storage
- Tokens are stored in browser's `localStorage`
- Persists across sessions
- Automatically cleared on logout

---

## Technical Details (For Developers)

### Installation
The JWT library is already installed:
```
djangorestframework-simplejwt
```

### Configuration
Located in `django_ecommerce/settings.py`:

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
}
```

### API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/accounts/register/` | POST | Register new user (returns tokens) |
| `/api/accounts/login/` | POST | Login user (returns tokens) |
| `/api/accounts/logout/` | POST | Logout user |
| `/api/accounts/token/refresh/` | POST | Get new access token |
| `/api/accounts/token/verify/` | POST | Verify token validity |

### Response Format

**Login Response:**
```json
{
    "user": {
        "id": 1,
        "email": "user@example.com",
        "username": "john_doe",
        "first_name": "John"
    },
    "tokens": {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
    },
    "message": "Login successful."
}
```

---

## Key JavaScript Files

### `static/js/jwt-auth.js` (NEW)
- Manages token storage and refresh
- Automatically refreshes tokens before expiration
- Handles token encoding/decoding

**Main Functions:**
```javascript
jwtManager.setTokens(access, refresh)      // Store tokens
jwtManager.getAccessToken()                 // Get current token
jwtManager.isAuthenticated()               // Check if logged in
jwtManager.refreshAccessToken()            // Refresh token manually
jwtManager.logout()                        // Clear tokens
```

### `static/js/home.js` (UPDATED)
- New `getAuthHeaders()` function
- Automatically adds JWT token to API requests
- All cart operations now use JWT tokens

### `templates/base.html` (UPDATED)
- Now loads `jwt-auth.js` first
- Updated logout function to clear JWT tokens
- Token refresh timer starts on page load

---

## Testing the Implementation

### 1. Check If Tokens Are Stored
1. Open Developer Tools (F12)
2. Go to **Application** → **LocalStorage**
3. Look for `access_token` and `refresh_token` after login

### 2. Check Token Refresh
1. Open **Console** tab
2. Look for message: "Attempting to refresh token..." every 50 minutes
3. Or manually refresh by waiting 60+ minutes and making an API call

### 3. Test API With Token
```bash
# Get your access token from browser localStorage
ACCESS_TOKEN="your_token_here"

# Make authenticated request
curl -X GET http://localhost:8000/api/cart/cart/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

### 4. Test Token Refresh
```bash
REFRESH_TOKEN="your_refresh_token_here"

curl -X POST http://localhost:8000/api/accounts/token/refresh/ \
  -H "Content-Type: application/json" \
  -d "{\"refresh\": \"$REFRESH_TOKEN\"}"
```

---

## Common Questions

### Q: Why do I need two tokens?
**A**: Access tokens expire quickly (60 min) for security. Refresh tokens (7 days) let you get new access tokens without re-entering your password.

### Q: Are my tokens safe in localStorage?
**A**: They're as safe as the browser. HTTPS encryption protects them in transit. If someone gains access to your browser, they can get your tokens.

### Q: What happens if I close my browser?
**A**: Your tokens remain in localStorage. When you reopen the browser, you're still logged in! Close the tab, clear browser data, or explicitly logout to log out.

### Q: How long can I stay logged in?
**A**: Up to 7 days (refresh token lifetime). After 7 days, you must login again.

### Q: What if my token expires?
**A**: It's automatically refreshed every 50 minutes. You won't notice!

### Q: How do I logout?
**A**: Click the "Logout" button. Your tokens are immediately deleted from localStorage.

### Q: Can I logout from multiple devices?
**A**: Each device has its own tokens. You must logout from each device separately.

---

## Troubleshooting

### Problem: "401 Unauthorized" errors
```
Solution:
1. Check console for errors (F12 → Console)
2. Verify token exists in localStorage (F12 → Application)
3. Try logging out and logging back in
4. Clear browser cache and retry
```

### Problem: Token not refreshing
```
Solution:
1. Check console for "Attempting to refresh token..." message
2. Verify backend is running
3. Check Django logs for errors
4. Restart server with: python manage.py runserver
```

### Problem: Can't login after registration
```
Solution:
1. Check email address is correct
2. Verify password was typed correctly
3. Check browser console for errors
4. Try clearing browser cache
5. Check Django logs for database errors
```

### Problem: Still logged in after logout
```
Solution:
This means logout didn't complete. Try:
1. Manually clear localStorage: F12 → Application → LocalStorage → Delete All
2. Close all tabs and reopen
3. Try logout again
```

---

## Configuration Changes

### To Change Token Lifetime

Edit `django_ecommerce/settings.py`:

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),   # Change from 60 to 30
    'REFRESH_TOKEN_LIFETIME': timedelta(days=14),    # Change from 7 to 14
}
```

Then update `static/js/jwt-auth.js`:

```javascript
// Change 50 * 60 * 1000 to match your new lifetime
// (use 80-90% of ACCESS_TOKEN_LIFETIME)
this.tokenCheckInterval = setInterval(() => {
    this.refreshAccessToken();
}, 24 * 60 * 1000);  // 24 minutes for 30-min tokens
```

### To Use HTTP-Only Cookies (More Secure)

This requires backend changes to store tokens in cookies instead of localStorage. Contact development team for assistance.

---

## Summary

✅ **What's New:**
- Users stay logged in for up to 7 days
- Automatic token refresh every 50 minutes
- No more "Session Expired" messages
- Seamless shopping experience
- Better security with token rotation

✅ **What's the Same:**
- Same login/register forms
- Same product browsing
- Same add-to-cart functionality
- Same checkout process

✅ **What's Better:**
- More secure authentication
- Persistent sessions
- Better mobile experience
- Scales better with multiple devices

---

## Next Steps

1. **Test the new authentication**
   - Register a new account
   - Login and add items to cart
   - Close browser and reopen
   - Verify you're still logged in

2. **Monitor token refresh**
   - Open console (F12)
   - Look for refresh messages
   - Verify tokens in localStorage

3. **Test logout**
   - Click logout button
   - Verify tokens are deleted
   - Try accessing protected features (should redirect to login)

---

For more technical details, see `JWT_IMPLEMENTATION.md`
