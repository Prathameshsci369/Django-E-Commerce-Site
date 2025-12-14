# 🚀 Quick Reference Guide

A cheat sheet for common tasks and commands in the Django E-Commerce Platform.

---

## 📦 Installation & Setup

```bash
# Clone repository
git clone https://github.com/yourusername/django-ecommerce.git
cd django-ecommerce

# Create virtual environment
python -m venv myenv
source myenv/bin/activate  # Windows: myenv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Navigate to project
cd django_ecommerce

# Migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Start server
python manage.py runserver
```

---

## 🔑 Common Django Commands

```bash
# Database
python manage.py migrate              # Apply migrations
python manage.py makemigrations       # Create migrations
python manage.py migrate zero app     # Revert migrations

# Users
python manage.py createsuperuser      # Create admin
python manage.py changepassword user  # Change password

# Server
python manage.py runserver            # Start dev server
python manage.py runserver 0.0.0.0:8000  # Listen all interfaces
python manage.py runserver 8001       # Different port

# Static Files
python manage.py collectstatic        # Collect static files
python manage.py findstatic file.css  # Find static file

# Shell
python manage.py shell                # Django interactive shell

# Testing
python manage.py test                 # Run tests
python manage.py test app.TestClass   # Run specific test
```

---

## 🌐 API Endpoints Reference

### Authentication
| Endpoint | Method | Purpose |
|:---:|:---:|:---|
| `/api/accounts/register/` | POST | Register user |
| `/api/accounts/login/` | POST | Login user |
| `/api/accounts/logout/` | POST | Logout user |
| `/api/accounts/token/refresh/` | POST | Refresh token |
| `/api/accounts/token/verify/` | POST | Verify token |

### Products
| Endpoint | Method | Purpose |
|:---:|:---:|:---|
| `/api/products/products/` | GET | List products |
| `/api/products/products/{id}/` | GET | Get product |
| `/api/products/categories/` | GET | List categories |

### Cart
| Endpoint | Method | Purpose |
|:---:|:---:|:---|
| `/api/cart/cart/` | GET | Get cart |
| `/api/cart/cart/add_item/` | POST | Add to cart |
| `/api/cart/cart/remove_item/` | POST | Remove from cart |
| `/api/cart/cart/update_item/` | POST | Update quantity |

### Orders
| Endpoint | Method | Purpose |
|:---:|:---:|:---|
| `/api/orders/orders/` | GET | List orders |
| `/api/orders/orders/` | POST | Create order |
| `/api/orders/orders/{id}/` | GET | Get order |

---

## 💻 cURL Commands

### Register User
```bash
curl -X POST http://localhost:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123",
    "first_name": "Test",
    "last_name": "User",
    "phone": "+1234567890"
  }'
```

### Login User
```bash
curl -X POST http://localhost:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

### Get Products
```bash
curl http://localhost:8000/api/products/products/

# With filtering
curl "http://localhost:8000/api/products/products/?category=electronics&page=1"
curl "http://localhost:8000/api/products/products/?search=yoga"
curl "http://localhost:8000/api/products/products/?featured=true"
```

### Add to Cart
```bash
curl -X POST http://localhost:8000/api/cart/cart/add_item/ \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "quantity": 2
  }'
```

### Get Cart
```bash
curl http://localhost:8000/api/cart/cart/ \
  -H "Authorization: Bearer {access_token}"
```

### Refresh Token
```bash
curl -X POST http://localhost:8000/api/accounts/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "{refresh_token}"
  }'
```

---

## 🎨 Frontend Code Snippets

### Get Auth Headers (with JWT)
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

### Make Authenticated Request
```javascript
const response = await fetch('/api/endpoint/', {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(data)
});
```

### Store JWT Token
```javascript
if (data.tokens) {
    jwtManager.setTokens(
        data.tokens.access,
        data.tokens.refresh
    );
}
```

### Check if Authenticated
```javascript
if (jwtManager.isAuthenticated()) {
    // User is logged in
}
```

### Logout
```javascript
jwtManager.logout();
localStorage.removeItem('user');
window.location.href = '/';
```

---

## 🔧 Database

### View SQLite Database
```bash
# Using SQLite CLI
sqlite3 db.sqlite3

# Common queries
.tables                           # List tables
.schema accounts_user             # Show schema
SELECT * FROM accounts_user;      # View users
DELETE FROM accounts_user;        # Clear table

# Using GUI
# Download SQLite Browser and open db.sqlite3
```

### Reset Database
```bash
# Delete database file
rm db.sqlite3

# Recreate
python manage.py migrate

# Create new superuser
python manage.py createsuperuser
```

---

## 📝 File Structure Quick Access

```
Project Root
├── README.md                    # Main documentation
├── JWT_IMPLEMENTATION.md        # JWT guide
├── JWT_QUICK_START.md          # JWT quickstart
├── DOCUMENTATION_INDEX.md       # Doc index
└── django_ecommerce/
    ├── manage.py
    ├── db.sqlite3
    ├── django_ecommerce/
    │   ├── settings.py         # Configuration
    │   ├── urls.py             # URL routing
    │   └── views.py            # Main views
    ├── accounts/
    │   ├── models.py           # User model
    │   ├── views.py            # Auth endpoints
    │   └── urls.py             # Auth URLs
    ├── products/
    │   ├── models.py           # Product model
    │   ├── views.py            # Product endpoints
    │   └── urls.py             # Product URLs
    ├── cart/
    │   ├── models.py           # Cart model
    │   ├── views.py            # Cart endpoints
    │   └── urls.py             # Cart URLs
    ├── orders/
    │   ├── models.py           # Order model
    │   ├── views.py            # Order endpoints
    │   └── urls.py             # Order URLs
    ├── templates/              # HTML templates
    ├── static/                 # CSS, JS, images
    │   ├── css/style.css
    │   ├── js/jwt-auth.js      # JWT management
    │   ├── js/home.js          # Frontend logic
    │   └── images/placeholder.svg
    └── media/                  # User uploads
```

---

## 🧪 Testing

### Test User Registration
1. Go to http://localhost:8000/register/
2. Fill form with valid data
3. Submit
4. Should be redirected to home
5. Check localStorage for tokens (F12 → Application → LocalStorage)

### Test Product Browsing
1. Go to http://localhost:8000
2. Filter by category
3. Search for product
4. Click product name to view detail

### Test Add to Cart
1. Login to account
2. Go to product detail
3. Click "Add to Cart"
4. Click cart icon to view cart

### Test API with Postman
1. Install Postman
2. Create POST request to `/api/accounts/login/`
3. Add JSON body with email and password
4. Send request
5. Copy access token
6. Use token in Authorization header for other requests

---

## 🐛 Debug Mode

### Enable Print Statements
```python
# In views.py
def some_view(request):
    print(f"User: {request.user}")  # Will show in console
    print(f"Request data: {request.data}")
```

### Check Request Data
```python
import json
from django.http import JsonResponse

def debug_view(request):
    print(f"Method: {request.method}")
    print(f"Headers: {request.headers}")
    print(f"Body: {request.body}")
    print(f"Data: {request.data}")
    return JsonResponse({"status": "ok"})
```

### View Database Queries
```python
from django.db import connection
from django.test.utils import CaptureQueriesContext

with CaptureQueriesContext(connection) as ctx:
    products = Product.objects.all()
    print(f"Queries executed: {len(ctx.captured_queries)}")
    for query in ctx.captured_queries:
        print(query['sql'])
```

---

## 🔐 Security Checklist

### Development
- [ ] DEBUG = True (OK for development)
- [ ] SECRET_KEY is dummy (OK for development)
- [ ] Database is SQLite (OK for development)

### Before Production
- [ ] DEBUG = False
- [ ] SECRET_KEY is strong and secret
- [ ] ALLOWED_HOSTS configured
- [ ] Database changed to PostgreSQL
- [ ] HTTPS enabled
- [ ] Static files collected
- [ ] Admin site accessible only to admins
- [ ] Email backend configured
- [ ] Logging configured
- [ ] Rate limiting configured

---

## 📊 Performance Tips

### Database Optimization
```python
# Use select_related for ForeignKey
products = Product.objects.select_related('category')

# Use prefetch_related for ManyToMany/Reverse FK
products = Product.objects.prefetch_related('images')

# Use values_list for specific fields only
names = Product.objects.values_list('name', flat=True)

# Use filter before other operations
Product.objects.filter(is_active=True).count()
```

### Caching
```python
from django.core.cache import cache

# Cache for 1 hour
cache.set('products_list', products, 3600)

# Retrieve from cache
products = cache.get('products_list')
```

### Pagination
```python
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
```

---

## 📚 Learning Resources

| Resource | Type | Purpose |
|:---:|:---:|:---|
| README.md | Documentation | Complete guide |
| Django Docs | Official | Framework docs |
| DRF Docs | Official | API framework docs |
| JWT Docs | Official | Authentication docs |
| Stack Overflow | Community | Problem solving |
| Real Python | Tutorial | In-depth tutorials |

---

## 🆘 Troubleshooting Quick Fixes

| Issue | Solution |
|:---|:---|
| Port 8000 in use | Kill process: `lsof -ti:8000 \| xargs kill -9` |
| Import errors | Reinstall: `pip install -r requirements.txt` |
| Migration errors | Revert and retry: `python manage.py migrate zero app` |
| Static files 404 | Run: `python manage.py collectstatic` |
| Database locked | Delete and recreate: `rm db.sqlite3 && python manage.py migrate` |
| Token not working | Clear localStorage: `localStorage.clear()` |
| CORS errors | Check CORS_ALLOWED_ORIGINS in settings.py |
| 403 Forbidden | Check permissions in ViewSet |
| 401 Unauthorized | Token missing or expired, login again |

---

## 🔗 Important URLs

### Development
```
Frontend:    http://localhost:8000
Admin:       http://localhost:8000/admin
API Root:    http://localhost:8000/api/
API Docs:    http://localhost:8000/api/schema/
```

### API Endpoints
```
Register:    http://localhost:8000/api/accounts/register/
Login:       http://localhost:8000/api/accounts/login/
Products:    http://localhost:8000/api/products/products/
Categories:  http://localhost:8000/api/products/categories/
Cart:        http://localhost:8000/api/cart/cart/
Orders:      http://localhost:8000/api/orders/orders/
```

### Pages
```
Home:        http://localhost:8000/
Login:       http://localhost:8000/login/
Register:    http://localhost:8000/register/
Product:     http://localhost:8000/product/<slug>/
```

---

## ⌨️ Keyboard Shortcuts

### Django Shell
```python
python manage.py shell

# Useful commands
from django.contrib.auth import get_user_model
User = get_user_model()
users = User.objects.all()
user = User.objects.create_user(
    username='test',
    email='test@test.com',
    password='password'
)
```

### Browser Developer Tools (F12)
```
Ctrl+Shift+C    # Element inspector
F12             # Open dev tools
Ctrl+Shift+K    # Console
Ctrl+Shift+I    # Dev tools toggle
Ctrl+Shift+J    # Open console directly
Ctrl+Shift+M    # Toggle responsive design
```

---

## 📊 Model Relationships

```
User (1) ──────────────── (1) Cart
 │
 ├─── (1) ──────────────── (Many) Address
 │
 ├─── (1) ──────────────── (Many) Order
 │
 └─── (1) ──────────────── (Many) Review

Order (1) ──────────────── (Many) OrderItem
 │
 └─── (1) ──────────────── (Many) Product

Cart (1) ──────────────── (Many) CartItem
 │
 └─── (Many) ──────────────── (1) Product

Category (1) ──────────────── (Many) Product
 │
 └─── (Many) ──────────────── (Many) Product (Parent/Child)

Product (1) ──────────────── (Many) ProductImage
```

---

## 🎯 Common Tasks

### Add a New Product
```bash
python manage.py shell

from products.models import Product, Category

category = Category.objects.first()
product = Product.objects.create(
    name="New Product",
    description="Product description",
    price=29.99,
    category=category,
    sku="PROD-001"
)
```

### Create User Programmatically
```python
from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.create_user(
    username='john',
    email='john@example.com',
    password='securepass123'
)
```

### Query Products
```python
from products.models import Product

# All active products
products = Product.objects.filter(is_active=True)

# Featured products
featured = Product.objects.filter(is_featured=True)

# By category
electronics = Product.objects.filter(category__slug='electronics')

# Search
results = Product.objects.filter(name__icontains='yoga')
```

### Get User's Orders
```python
from orders.models import Order

orders = Order.objects.filter(user=request.user)
recent = orders.latest('created_at')
```

---

## 📈 Git Commands

```bash
# Basic workflow
git add .                              # Stage changes
git commit -m "Description"            # Commit
git push origin main                   # Push to GitHub
git pull origin main                   # Pull latest

# Branches
git checkout -b feature/my-feature     # Create feature branch
git checkout main                      # Switch branch
git merge feature/my-feature           # Merge branch

# History
git log                                # View commits
git status                             # Check status
git diff                               # View changes

# Undo
git reset --hard HEAD                  # Discard changes
git revert commit_hash                 # Undo commit
```

---

<div align="center">

**💡 Pro Tip: Bookmark this page for quick reference!**

**❓ Can't find something? Check the [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)**

Made with ❤️ for developers

</div>
