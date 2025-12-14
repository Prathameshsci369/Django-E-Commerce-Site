// JWT Token Management
// Stores access and refresh tokens in localStorage
// Automatically refreshes expired tokens

class JWTManager {
    constructor() {
        this.accessToken = localStorage.getItem('access_token');
        this.refreshToken = localStorage.getItem('refresh_token');
        this.tokenCheckInterval = null;
    }

    /**
     * Store tokens in localStorage
     */
    setTokens(accessToken, refreshToken) {
        this.accessToken = accessToken;
        this.refreshToken = refreshToken;
        localStorage.setItem('access_token', accessToken);
        localStorage.setItem('refresh_token', refreshToken);
        console.log('Tokens stored in localStorage');
        this.startTokenRefreshTimer();
    }

    /**
     * Get access token
     */
    getAccessToken() {
        return localStorage.getItem('access_token');
    }

    /**
     * Get refresh token
     */
    getRefreshToken() {
        return localStorage.getItem('refresh_token');
    }

    /**
     * Check if user is authenticated
     */
    isAuthenticated() {
        return !!localStorage.getItem('access_token');
    }

    /**
     * Refresh access token using refresh token
     */
    async refreshAccessToken() {
        try {
            const refreshToken = this.getRefreshToken();
            if (!refreshToken) {
                console.log('No refresh token available');
                return false;
            }

            const response = await fetch('/api/accounts/token/refresh/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    refresh: refreshToken
                })
            });

            if (response.ok) {
                const data = await response.json();
                this.accessToken = data.access;
                localStorage.setItem('access_token', data.access);
                
                // If new refresh token is provided, store it
                if (data.refresh) {
                    this.refreshToken = data.refresh;
                    localStorage.setItem('refresh_token', data.refresh);
                }
                
                console.log('Access token refreshed successfully');
                return true;
            } else if (response.status === 401) {
                // Refresh token is invalid or expired
                console.log('Refresh token expired. Please login again.');
                this.logout();
                return false;
            } else {
                console.error('Failed to refresh token:', response.statusText);
                return false;
            }
        } catch (error) {
            console.error('Error refreshing token:', error);
            return false;
        }
    }

    /**
     * Clear all tokens (logout)
     */
    logout() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        this.accessToken = null;
        this.refreshToken = null;
        this.stopTokenRefreshTimer();
        console.log('Tokens cleared');
    }

    /**
     * Start timer to refresh token before expiration
     * JWT tokens typically expire in 1 hour, so refresh every 50 minutes
     */
    startTokenRefreshTimer() {
        // Clear any existing timer
        this.stopTokenRefreshTimer();
        
        // Set timer to refresh token every 50 minutes (3000 seconds)
        this.tokenCheckInterval = setInterval(() => {
            console.log('Attempting to refresh token...');
            this.refreshAccessToken();
        }, 50 * 60 * 1000);
    }

    /**
     * Stop token refresh timer
     */
    stopTokenRefreshTimer() {
        if (this.tokenCheckInterval) {
            clearInterval(this.tokenCheckInterval);
            this.tokenCheckInterval = null;
        }
    }

    /**
     * Decode JWT token (simple decoder, doesn't verify signature)
     */
    decodeToken(token) {
        try {
            const base64Url = token.split('.')[1];
            const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
            const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
                return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
            }).join(''));
            return JSON.parse(jsonPayload);
        } catch (error) {
            console.error('Error decoding token:', error);
            return null;
        }
    }

    /**
     * Check if token is expired
     */
    isTokenExpired(token) {
        const payload = this.decodeToken(token);
        if (!payload || !payload.exp) return true;
        
        const currentTime = Math.floor(Date.now() / 1000);
        return payload.exp < currentTime;
    }
}

// Create global JWT manager instance
const jwtManager = new JWTManager();

// Check if token is already stored on page load and start refresh timer
document.addEventListener('DOMContentLoaded', function() {
    if (jwtManager.isAuthenticated()) {
        const token = jwtManager.getAccessToken();
        if (jwtManager.isTokenExpired(token)) {
            console.log('Token is expired, attempting refresh...');
            jwtManager.refreshAccessToken();
        } else {
            jwtManager.startTokenRefreshTimer();
        }
    }
});
