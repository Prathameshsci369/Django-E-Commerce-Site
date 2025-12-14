# Django E-Commerce Platform

<div align="center">

![Django E-Commerce](https://img.shields.io/badge/Django-5.2.8-green?style=flat-square&logo=django)
![Python](https://img.shields.io/badge/Python-3.13+-blue?style=flat-square&logo=python)
![REST API](https://img.shields.io/badge/REST%20API-DRF-red?style=flat-square)
![JWT Auth](https://img.shields.io/badge/JWT-simplejwt-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

A full-featured, production-ready e-commerce platform built with Django and Django REST Framework. Features JWT-based authentication, product catalog management, shopping cart, order processing, and a responsive Bootstrap 5 UI.

[🌐 Live Demo](#) • [📖 Documentation](#documentation) • [🚀 Quick Start](#quick-start) • [🛠️ Tech Stack](#tech-stack)

</div>

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Frontend Features](#frontend-features)
- [Database Models](#database-models)
- [Authentication & Authorization](#authentication--authorization)
- [Testing](#testing)
- [Deployment](#deployment)
- [Documentation](#documentation)
- [Tech Stack](#tech-stack)
- [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## 🎯 Project Overview

**Django E-Commerce Platform** is a comprehensive, scalable e-commerce solution that enables businesses to manage products, process orders, and provide customers with a seamless shopping experience. Built with industry best practices, the platform includes:

- **Full-Stack Solution**: Backend REST API + Frontend UI
- **Stateless Authentication**: JWT tokens for persistent sessions
- **Product Management**: Categories, products, images, pricing
- **Shopping Cart**: Real-time cart updates with quantity management
- **Order Management**: Complete order lifecycle from creation to delivery
- **User Accounts**: Registration, login, address management
- **Admin Dashboard**: Django admin for complete control
- **Mobile-Friendly**: Responsive Bootstrap 5 design
- **Secure**: CORS, CSRF protection, JWT authentication

### Use Cases

✅ B2C E-Commerce Stores  
✅ Multi-Vendor Marketplaces  
✅ Product Catalogs  
✅ Order Management Systems  
✅ Customer Account Management  
✅ Subscription Services  

---

## ✨ Key Features

### 1. **User Authentication & Authorization**
- Custom User model with email-based login
- Registration with validation
- JWT token-based authentication (persistent across sessions)
- Automatic token refresh every 50 minutes
- Session management with 7-day refresh token lifetime
- Role-based access control (admin, staff, regular users)

### 2. **Product Management**
- Category hierarchy (parent/child categories)
- Product creation with SKU tracking
- Multiple product images with primary image selection
- Product variants support
- Price tracking (current vs. compare price)
- Quantity management and stock tracking
- Featured products display
- Product search and filtering
- Auto-generated URL slugs

### 3. **Shopping Cart**
- Real-time cart management
- Add/remove items
- Quantity adjustments
- Cart persistence across sessions
- Automatic price calculation
- Cart summary in navbar

### 4. **Order Management**
- Complete order lifecycle
- Automatic order number generation
- Order status tracking (pending, processing, shipped, delivered, canceled)
- Order items with pricing snapshots
- Shipping address management
- Order notes and comments
- Tax and subtotal calculations

### 5. **User Account Management**
- User profile management
- Multiple shipping/billing addresses
- Address management (create, update, delete)
- Order history
- Account preferences

### 6. **API Features**
- RESTful API with DRF
- JSON response format
- Pagination for list endpoints
- Search and filtering
- Ordering and sorting
- Comprehensive error handling
- Request validation

### 7. **Frontend Features**
- Responsive Bootstrap 5 design
- Product browsing and filtering
- Product detail pages
- Shopping cart interface
- User authentication pages
- Account management
- Mobile-optimized layout
- Real-time UI updates via Fetch API

### 8. **Security**
- CORS protection with whitelist
- CSRF token validation
- Password hashing with Django security
- Secure JWT token handling
- HTTPS ready
- SQL injection protection (ORM)
- XSS protection

---

## 📁 Project Structure

```
django-ecommerce/
├── django_ecommerce/                 # Main project directory
│   ├── django_ecommerce/             # Project config
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py               # Django settings
│   │   ├── urls.py                   # Main URL routing
│   │   ├── views.py                  # Main views (Home, Login, Register, ProductDetail)
│   │   └── wsgi.py
│   │
│   ├── accounts/                     # User management app
│   │   ├── models.py                 # User model, Address model
│   │   ├── views.py                  # Auth endpoints (register, login, logout)
│   │   ├── serializers.py            # User, Address serializers
│   │   ├── urls.py                   # Auth URLs
│   │   ├── admin.py
│   │   └── migrations/
│   │
│   ├── products/                     # Product catalog app
│   │   ├── models.py                 # Category, Product, ProductImage models
│   │   ├── views.py                  # Product viewsets, filtering
│   │   ├── serializers.py            # Product serializers
│   │   ├── urls.py                   # Product URLs
│   │   ├── admin.py
│   │   └── migrations/
│   │
│   ├── cart/                         # Shopping cart app
│   │   ├── models.py                 # Cart, CartItem models
│   │   ├── views.py                  # Cart viewsets (add, remove, update)
│   │   ├── serializers.py            # Cart serializers
│   │   ├── urls.py                   # Cart URLs
│   │   ├── context_processors.py     # Template context
│   │   ├── admin.py
│   │   └── migrations/
│   │
│   ├── orders/                       # Order management app
│   │   ├── models.py                 # Order, OrderItem models
│   │   ├── views.py                  # Order viewsets
│   │   ├── serializers.py            # Order serializers
│   │   ├── urls.py                   # Order URLs
│   │   ├── admin.py
│   │   └── migrations/
│   │
│   ├── templates/                    # Django templates
│   │   ├── base.html                 # Base template (navbar, footer, scripts)
│   │   ├── home.html                 # Product listing page
│   │   ├── login.html                # Login form
│   │   ├── register.html             # Registration form
│   │   └── product_detail.html       # Product detail page
│   │
│   ├── static/                       # Static files
│   │   ├── css/
│   │   │   └── style.css             # Custom styles
│   │   ├── js/
│   │   │   ├── jwt-auth.js           # JWT token management
│   │   │   └── home.js               # Home page interactions
│   │   └── images/
│   │       └── placeholder.svg       # Placeholder image
│   │
│   ├── media/                        # User uploads
│   │   ├── products/                 # Product images
│   │   └── categories/               # Category images
│   │
│   ├── db.sqlite3                    # SQLite database
│   ├── manage.py                     # Django management
│   └── requirements.txt              # Python dependencies
│
├── JWT_IMPLEMENTATION.md             # JWT detailed documentation
├── JWT_QUICK_START.md                # JWT quick start guide
├── IMPLEMENTATION_SUMMARY.md         # Implementation overview
└── README.md                         # This file
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip or poetry
- Virtual environment (recommended)

### Installation (5 minutes)

```bash
# 1. Clone repository
git clone https://github.com/yourusername/django-ecommerce.git
cd django-ecommerce

# 2. Create virtual environment
python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Navigate to project
cd django_ecommerce

# 5. Run migrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Start development server
python manage.py runserver

# 8. Access application
# Frontend: http://localhost:8000
# Admin: http://localhost:8000/admin
# API: http://localhost:8000/api/
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (optional for SQLite)
# DATABASE_URL=postgres://user:password@localhost:5432/dbname

# Email Configuration (optional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-password

# JWT Configuration (optional)
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_LIFETIME=3600  # seconds (1 hour)
JWT_REFRESH_TOKEN_LIFETIME=604800  # seconds (7 days)
```

### Settings Configuration

Key settings in `django_ecommerce/settings.py`:

```python
# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 12,
}

# JWT Configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}
```

---

## 📡 API Documentation

### Authentication Endpoints

#### Register User
```bash
POST /api/accounts/register/
Content-Type: application/json

{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepass123",
    "password_confirm": "securepass123",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+1234567890"
}

Response:
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
    "message": "User registered successfully."
}
```

#### Login
```bash
POST /api/accounts/login/
Content-Type: application/json

{
    "email": "john@example.com",
    "password": "securepass123"
}

Response: (Same as register)
```

#### Logout
```bash
POST /api/accounts/logout/
Authorization: Bearer {access_token}

Response:
{
    "message": "Logout successful."
}
```

#### Refresh Token
```bash
POST /api/accounts/token/refresh/
Content-Type: application/json

{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

Response:
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Product Endpoints

#### Get All Products
```bash
GET /api/products/products/
GET /api/products/products/?page=1&page_size=12
GET /api/products/products/?category=electronics
GET /api/products/products/?featured=true
GET /api/products/products/?ordering=-created_at
GET /api/products/products/?search=laptop

Response:
{
    "count": 50,
    "next": "http://localhost:8000/api/products/products/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Yoga Mat",
            "slug": "yoga-mat",
            "description": "Premium yoga mat...",
            "price": "29.99",
            "compare_price": "39.99",
            "sku": "YM-001",
            "quantity": 100,
            "is_featured": true,
            "category": 1,
            "created_at": "2024-12-13T10:30:00Z",
            "updated_at": "2024-12-13T10:30:00Z"
        }
    ]
}
```

#### Get Product Detail
```bash
GET /api/products/products/{id}/

Response:
{
    "id": 1,
    "name": "Yoga Mat",
    "slug": "yoga-mat",
    "description": "Premium yoga mat...",
    "price": "29.99",
    "compare_price": "39.99",
    "sku": "YM-001",
    "quantity": 100,
    "is_featured": true,
    "category": 1,
    "images": [
        {
            "id": 1,
            "image": "http://localhost:8000/media/products/yoga-mat.jpg",
            "is_primary": true
        }
    ],
    "reviews": [
        {
            "id": 1,
            "user": "john_doe",
            "rating": 5,
            "comment": "Great product!",
            "created_at": "2024-12-13T10:30:00Z"
        }
    ]
}
```

#### Get Categories
```bash
GET /api/products/categories/

Response:
{
    "count": 5,
    "results": [
        {
            "id": 1,
            "name": "Electronics",
            "slug": "electronics",
            "description": "Electronic devices...",
            "image": "http://localhost:8000/media/categories/electronics.jpg",
            "is_active": true
        }
    ]
}
```

### Cart Endpoints

#### Get Cart
```bash
GET /api/cart/cart/
Authorization: Bearer {access_token}

Response:
{
    "id": 1,
    "user": 1,
    "items": [
        {
            "id": 1,
            "cart": 1,
            "product": 1,
            "product_name": "Yoga Mat",
            "quantity": 2,
            "price": "29.99",
            "total_price": "59.98"
        }
    ],
    "total_price": "59.98",
    "total_quantity": 2,
    "created_at": "2024-12-13T10:30:00Z"
}
```

#### Add to Cart
```bash
POST /api/cart/cart/add_item/
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "product_id": 1,
    "quantity": 2
}

Response:
{
    "message": "Item added to cart"
}
```

#### Remove from Cart
```bash
POST /api/cart/cart/remove_item/
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "product_id": 1
}

Response:
{
    "message": "Item removed from cart"
}
```

#### Update Cart Item
```bash
POST /api/cart/cart/update_item/
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "product_id": 1,
    "quantity": 5
}

Response:
{
    "message": "Cart updated"
}
```

### Order Endpoints

#### Get Orders
```bash
GET /api/orders/orders/
Authorization: Bearer {access_token}

Response:
{
    "count": 5,
    "results": [
        {
            "id": 1,
            "order_number": "ORD12345",
            "user": 1,
            "status": "shipped",
            "subtotal": "99.99",
            "tax": "10.00",
            "total": "109.99",
            "items": [
                {
                    "id": 1,
                    "order": 1,
                    "product": 1,
                    "quantity": 1,
                    "price": "99.99",
                    "total": "99.99"
                }
            ],
            "created_at": "2024-12-13T10:30:00Z"
        }
    ]
}
```

#### Create Order
```bash
POST /api/orders/orders/
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "shipping_address": 1,
    "notes": "Please deliver before 5 PM"
}

Response:
{
    "id": 1,
    "order_number": "ORD12345",
    "user": 1,
    "status": "pending",
    "subtotal": "99.99",
    "tax": "10.00",
    "total": "109.99",
    "items": [...]
}
```

---

## 🎨 Frontend Features

### Pages

#### Home Page (`/`)
- Product listing with pagination
- Category filtering (sidebar)
- Product search
- Sort by price, newest, popularity
- Featured products display
- Add to cart from grid

#### Product Detail Page (`/product/<slug>/`)
- Product images carousel
- Product specifications
- Price comparison
- Stock availability
- Quantity selector
- Add to cart with quantity
- Related products
- Customer reviews (if available)

#### Login Page (`/login/`)
- Email-based login
- Remember me option
- Register link
- Error messages
- JWT token storage on success

#### Register Page (`/register/`)
- User registration form
- Password confirmation
- Validation feedback
- Auto-login after registration
- Redirect to home on success

#### Shopping Cart (Modal)
- View cart items
- Update quantities
- Remove items
- View total
- Checkout button

### UI Components
- Responsive Bootstrap 5 navbar
- Product cards with images
- Search bar
- Category sidebar
- Pagination controls
- Shopping cart modal
- Toast notifications
- Loading spinners

### JavaScript Features
- Fetch API for AJAX requests
- JWT token management
- Automatic token refresh
- Product filtering and search
- Cart operations
- Form validation
- Error handling

---

## 🗄️ Database Models

### User Model (Custom)
```python
class User(AbstractUser):
    email = EmailField(unique=True)
    phone = CharField(max_length=20)
    is_verified = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'  # Login with email instead of username
```

### Address Model
```python
class Address(Model):
    user = ForeignKey(User)
    address_type = CharField(choices=['shipping', 'billing'])
    first_name, last_name, company = CharField()
    address_line_1, address_line_2 = CharField()
    city, state, country, postal_code = CharField()
    phone = CharField()
    is_default = BooleanField()
    created_at, updated_at = DateTimeField()
```

### Category Model
```python
class Category(Model):
    name = CharField(max_length=100)
    slug = SlugField(unique=True)
    description = TextField()
    image = ImageField()
    parent = ForeignKey('self', null=True)  # Hierarchical categories
    is_active = BooleanField(default=True)
    created_at, updated_at = DateTimeField()
```

### Product Model
```python
class Product(Model):
    name = CharField(max_length=200)
    slug = SlugField(unique=True)
    description = TextField()
    price = DecimalField(max_digits=10, decimal_places=2)
    compare_price = DecimalField()  # Original price for discounts
    sku = CharField(unique=True)
    track_quantity = BooleanField(default=True)
    quantity = IntegerField(default=0)
    weight = DecimalField()
    is_active = BooleanField(default=True)
    is_featured = BooleanField(default=False)
    category = ForeignKey(Category)
    created_at, updated_at = DateTimeField()
```

### ProductImage Model
```python
class ProductImage(Model):
    product = ForeignKey(Product)
    image = ImageField(upload_to='products/')
    is_primary = BooleanField(default=False)
    created_at, updated_at = DateTimeField()
```

### Cart Model
```python
class Cart(Model):
    user = OneToOneField(User)
    created_at, updated_at = DateTimeField()
```

### CartItem Model
```python
class CartItem(Model):
    cart = ForeignKey(Cart)
    product = ForeignKey(Product)
    quantity = IntegerField(default=1)
    created_at, updated_at = DateTimeField()
    
    class Meta:
        unique_together = ('cart', 'product')
```

### Order Model
```python
class Order(Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]
    
    order_number = CharField(max_length=20, unique=True)
    user = ForeignKey(User)
    status = CharField(max_length=20, choices=STATUS_CHOICES)
    subtotal = DecimalField()
    tax = DecimalField()
    total = DecimalField()
    shipping_address = ForeignKey(Address)
    notes = TextField()
    created_at, updated_at = DateTimeField()
```

### OrderItem Model
```python
class OrderItem(Model):
    order = ForeignKey(Order)
    product = ForeignKey(Product)
    quantity = IntegerField()
    price = DecimalField()  # Price at time of order
    total = DecimalField()
    created_at = DateTimeField()
```

---

## 🔐 Authentication & Authorization

### JWT Authentication Flow

1. **Registration/Login**
   - User credentials → Backend validation
   - Generate access token (60 min) + refresh token (7 days)
   - Tokens stored in localStorage

2. **API Requests**
   - Include `Authorization: Bearer {access_token}`
   - Backend validates JWT signature and expiration
   - Request processed if valid, 401 if invalid

3. **Token Refresh**
   - Access token expires in 60 minutes
   - Frontend automatically refreshes every 50 minutes
   - Uses refresh token to get new access token
   - Seamless user experience

4. **Logout**
   - Clear tokens from localStorage
   - Optional: invalidate refresh token on backend
   - User redirected to login page

### Permission Classes

```python
IsAuthenticated          # Must be logged in
IsAuthenticatedOrReadOnly # Can read without login, need auth for write
IsAdminUser             # Must be admin/staff
```

### Role-Based Access

- **Anonymous Users**: Can browse products, categories
- **Authenticated Users**: Can add to cart, view orders, manage addresses
- **Admin Users**: Full access to admin panel, manage products

---

## 🧪 Testing

### Manual Testing

#### 1. Register New User
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

#### 2. Login
```bash
curl -X POST http://localhost:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

#### 3. Browse Products
```bash
curl http://localhost:8000/api/products/products/
```

#### 4. Add to Cart
```bash
curl -X POST http://localhost:8000/api/cart/cart/add_item/ \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "quantity": 2
  }'
```

#### 5. View Cart
```bash
curl http://localhost:8000/api/cart/cart/ \
  -H "Authorization: Bearer {access_token}"
```

### Browser Testing

1. Open http://localhost:8000
2. Click "Register"
3. Fill form and submit
4. Browse products
5. Click product to view details
6. Add to cart
7. Check cart modal
8. Close browser and reopen
9. Verify still logged in

### Test Coverage

- [ ] User registration
- [ ] User login
- [ ] Product browsing
- [ ] Product filtering
- [ ] Product search
- [ ] Add to cart
- [ ] Remove from cart
- [ ] Update cart quantity
- [ ] View cart
- [ ] JWT token persistence
- [ ] Token refresh
- [ ] User logout
- [ ] Admin panel access

---

## 🚢 Deployment

### Production Checklist

- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set strong `SECRET_KEY`
- [ ] Use environment variables for sensitive data
- [ ] Configure HTTPS/SSL
- [ ] Set up proper database (PostgreSQL recommended)
- [ ] Configure static files serving
- [ ] Configure media files storage
- [ ] Set up logging
- [ ] Configure email backend
- [ ] Run migrations
- [ ] Create superuser
- [ ] Collect static files: `python manage.py collectstatic`
- [ ] Test in production mode

### Deployment Platforms

#### Heroku
```bash
# Install Heroku CLI
# Login and create app
heroku create your-app-name

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False

# Deploy
git push heroku main
```

#### PythonAnywhere
1. Upload project files
2. Create virtual environment
3. Install dependencies
4. Configure web app settings
5. Point domain to PythonAnywhere
6. Run migrations on web console

#### AWS/DigitalOcean
Use Docker for containerization and deployment.

---

## 📚 Documentation

### Detailed Documentation

- **[JWT_IMPLEMENTATION.md](JWT_IMPLEMENTATION.md)** - Complete JWT authentication guide
- **[JWT_QUICK_START.md](JWT_QUICK_START.md)** - Quick start for JWT
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Implementation overview

### API Documentation

Full API documentation available at:
- Swagger UI: `/api/schema/swagger/` (if installed)
- ReDoc: `/api/schema/redoc/` (if installed)

### Code Comments

Each major class and function includes docstrings explaining:
- Purpose
- Parameters
- Return values
- Usage examples

---

## 🛠️ Tech Stack

<div align="center">

### Backend

| Technology | Version | Purpose |
|:---:|:---:|:---|
| **Django** | 5.2.8 | Web framework |
| **Python** | 3.13+ | Programming language |
| **Django REST Framework** | 3.16.1 | REST API framework |
| **djangorestframework-simplejwt** | 5.5.1 | JWT authentication |
| **django-cors-headers** | 4.9.0 | CORS handling |
| **SQLite/PostgreSQL** | - | Database |
| **Pillow** | - | Image processing |
| **python-dotenv** | 1.0.1 | Environment variables |

### Frontend

| Technology | Version | Purpose |
|:---:|:---:|:---|
| **HTML5** | - | Markup |
| **CSS3** | - | Styling |
| **JavaScript (ES6+)** | - | Interactivity |
| **Bootstrap** | 5.1.3 | UI Framework |
| **Font Awesome** | 6.0.0 | Icons |
| **Fetch API** | - | HTTP requests |

### Development Tools

| Tool | Purpose |
|:---:|:---|
| **Git** | Version control |
| **Virtual Environment** | Dependency isolation |
| **pip** | Package manager |
| **Django Admin** | Database management |
| **SQLite Browser** | Database inspection |

</div>

---

## 📊 Tech Stack Detailed Explanation

### Backend Architecture

#### **Django 5.2.8 - Web Framework**
```
├── Request → URL Routing
├── Views → Business Logic
├── Models → Database Schema
├── Serializers → Data Validation
└── Response → JSON/HTML
```

**Why Django:**
- ✅ Batteries included (admin, auth, ORM)
- ✅ Large ecosystem and community
- ✅ Production-ready
- ✅ Excellent documentation
- ✅ Security best practices built-in

#### **Django REST Framework (DRF) 3.16.1 - API Framework**
```
├── ViewSets → API endpoints
├── Serializers → Request/response validation
├── Permissions → Access control
├── Authentication → User identification
├── Pagination → Large dataset handling
└── Filtering → Query optimization
```

**Why DRF:**
- ✅ Industry standard for Django APIs
- ✅ Automatic API documentation
- ✅ Built-in authentication/permissions
- ✅ Comprehensive error handling
- ✅ Browsable API for testing

#### **djangorestframework-simplejwt 5.5.1 - JWT Authentication**
```
Token Flow:
1. User logs in → Backend validates credentials
2. Server creates JWT tokens (access + refresh)
3. Client stores tokens in localStorage
4. Client sends token with each request
5. Server validates token signature
6. Access granted if valid, 401 if invalid
7. Auto-refresh token every 50 minutes
```

**JWT Components:**
```
Access Token: eyJ0eXAiOiJKV1QiLCJhbGc... (expires 60 min)
├── Header: Algorithm (HS256) + Type (JWT)
├── Payload: user_id, exp, iat, jti
└── Signature: HMAC(header.payload, secret)

Refresh Token: eyJ0eXAiOiJKV1QiLCJhbGc... (expires 7 days)
└── Used only for getting new access token
```

**Why JWT:**
- ✅ Stateless authentication (no server session needed)
- ✅ Scalable across multiple servers
- ✅ Standard format (RFC 7519)
- ✅ Works with mobile and SPAs
- ✅ Token rotation for security

#### **SQLite Database**
```
Features:
├── File-based database (no server needed)
├── Suitable for development/testing
├── SQL queries via Django ORM
├── ACID compliance
└── Easy backup (single file)
```

**Why SQLite (for development):**
- ✅ Zero configuration
- ✅ No external database server
- ✅ Easy to inspect and debug
- ✅ Great for testing

**For Production:** Use PostgreSQL
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ecommerce_db',
        'USER': 'postgres',
        'PASSWORD': 'secure_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

#### **django-cors-headers 4.9.0 - CORS Protection**
```
Request: Frontend → Backend
├── Browser checks Origin header
├── Server checks CORS whitelist
├── If allowed: Response sent
└── If denied: CORS error returned

Configuration:
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://yourdomain.com",
]
```

**Why CORS:**
- ✅ Security: Only whitelisted domains can access API
- ✅ Prevents unauthorized cross-origin requests
- ✅ Works with cookies and authentication

---

### Frontend Architecture

#### **HTML5 - Markup**
```html
<!-- Semantic structure -->
<header>     <!-- Navigation -->
<main>       <!-- Content -->
<sidebar>    <!-- Filters, sidebar -->
<footer>     <!-- Footer -->
```

#### **CSS3 - Styling**
```css
/* Feature-rich styling */
├── Flexbox/Grid layout
├── Media queries (responsive)
├── CSS variables
├── Animations
└── Bootstrap classes
```

#### **JavaScript (ES6+) - Interactivity**
```javascript
/* Modern JavaScript features */
├── Async/await (Fetch API)
├── Classes (JWTManager)
├── Arrow functions
├── Template literals
├── Destructuring
└── Fetch API (no jQuery)
```

#### **Bootstrap 5.1.3 - UI Framework**
```
Components Used:
├── Navbar with collapse
├── Cards for products
├── Forms with validation
├── Modals for cart
├── Alerts for feedback
├── Pagination controls
├── Responsive grid system (12 columns)
└── Utility classes for styling
```

**Why Bootstrap:**
- ✅ Responsive design out-of-the-box
- ✅ Pre-built components
- ✅ Mobile-first approach
- ✅ Large community and documentation
- ✅ Professional appearance

#### **Fetch API - HTTP Requests**
```javascript
/* No jQuery needed */
const response = await fetch('/api/endpoint/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify(data)
});
```

**Modern Alternative to:**
- ✅ XMLHttpRequest (older)
- ✅ jQuery.ajax() (jQuery dependency)
- ✅ Axios (external library)

---

### Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    USER BROWSER                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ HTML (Templates) + CSS (Bootstrap) + JS (Fetch API)   │   │
│  │  - home.html (product listing)                         │   │
│  │  - login.html (authentication)                         │   │
│  │  - product_detail.html (product view)                 │   │
│  │  - jwt-auth.js (token management)                     │   │
│  │  - home.js (product & cart logic)                     │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                          ↕ HTTP/JSON
┌─────────────────────────────────────────────────────────────┐
│                   DJANGO BACKEND                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ URLs (Routing) → Views → Serializers → Models         │   │
│  │                                                        │   │
│  │ /api/accounts/     → Authentication endpoints          │   │
│  │   ├── register/    → Create user + JWT tokens         │   │
│  │   ├── login/       → Validate + JWT tokens            │   │
│  │   ├── logout/      → Clear session                    │   │
│  │   ├── token/refresh/ → New access token               │   │
│  │   └── token/verify/  → Validate token                │   │
│  │                                                        │   │
│  │ /api/products/     → Product endpoints                │   │
│  │   ├── products/    → List/search products             │   │
│  │   ├── categories/  → Get categories                   │   │
│  │   └── images/      → Product images                   │   │
│  │                                                        │   │
│  │ /api/cart/         → Shopping cart                    │   │
│  │   ├── cart/        → Get user's cart                 │   │
│  │   ├── add_item/    → Add product to cart             │   │
│  │   ├── remove_item/ → Remove from cart                │   │
│  │   └── update_item/ → Update quantity                 │   │
│  │                                                        │   │
│  │ /api/orders/       → Order management                 │   │
│  │   ├── orders/      → List user orders                │   │
│  │   └── create/      → Create new order                │   │
│  │                                                        │   │
│  │ Templates:         → HTML rendering                   │   │
│  │   ├── base.html    → Master template                  │   │
│  │   ├── home.html    → Home page                        │   │
│  │   ├── login.html   → Login form                       │   │
│  │   ├── register.html → Register form                   │   │
│  │   └── product_detail.html → Product detail           │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                          ↕ SQL
┌─────────────────────────────────────────────────────────────┐
│                   SQLite DATABASE                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Tables:                                              │   │
│  │  ├── accounts_user (Custom user model)               │   │
│  │  ├── accounts_address (Shipping/billing addresses)   │   │
│  │  ├── products_category (Product categories)          │   │
│  │  ├── products_product (Products)                     │   │
│  │  ├── products_productimage (Product images)          │   │
│  │  ├── cart_cart (Shopping carts)                      │   │
│  │  ├── cart_cartitem (Items in cart)                   │   │
│  │  ├── orders_order (Orders)                           │   │
│  │  ├── orders_orderitem (Items in orders)              │   │
│  │  └── [Django auth tables]                            │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

### Request/Response Cycle Example

**Add to Cart Request:**
```
1. USER CLICKS "Add to Cart"
   └─→ JavaScript triggers addToCart(productId)

2. FRONTEND PREPARATION
   └─→ Get JWT token from localStorage
   └─→ Build request headers with Authorization
   └─→ Prepare JSON body with product_id & quantity

3. HTTP REQUEST SENT
   POST /api/cart/cart/add_item/
   Headers: Authorization: Bearer eyJ0eXAi...
            Content-Type: application/json
   Body: {"product_id": 1, "quantity": 2}

4. DJANGO PROCESSES REQUEST
   ├─→ URL router matches /api/cart/cart/add_item/
   ├─→ JWTAuthentication validates token
   ├─→ IsAuthenticated permission checks user
   ├─→ CartViewSet.add_item() method executes
   ├─→ CartItemSerializer validates data
   ├─→ Product model checks availability
   ├─→ CartItem model saves to database
   └─→ Response prepared

5. RESPONSE SENT
   Status: 200 OK
   Body: {"message": "Item added to cart"}

6. FRONTEND HANDLES RESPONSE
   ├─→ Parse JSON response
   ├─→ Show success toast
   ├─→ Reload page or update cart count
   └─→ User sees updated cart
```

---

### Architecture Advantages

| Aspect | Benefit |
|:---:|:---|
| **JWT Tokens** | Stateless, scalable, mobile-friendly |
| **REST API** | Standard format, easy integration, frontend-agnostic |
| **Django ORM** | SQL injection protection, database agnostic |
| **Serializers** | Data validation, permission checking, documentation |
| **ViewSets** | CRUD operations automatically, DRY principle |
| **Middleware** | Consistent request/response handling |
| **Templates** | Server-side rendering, full control |
| **Static Files** | CSS/JS served efficiently, caching support |

---

### Security Architecture

```
Request → Middleware Stack
├─→ CORS middleware (check origin)
├─→ Security middleware (add headers)
├─→ Session middleware (session management)
├─→ CSRF middleware (form protection)
├─→ Auth middleware (identify user)
└─→ Message middleware (flash messages)
      ↓
   View/ViewSet
├─→ JWTAuthentication (validate token)
├─→ Permission class (check access)
├─→ Serializer validation (check data)
└─→ Business logic (process request)
      ↓
   Database
├─→ ORM query (prevent SQL injection)
├─→ Model validation (business rules)
└─→ Transaction management (consistency)
      ↓
   Response
├─→ Content-Type validation
├─→ Status code selection
└─→ JSON serialization
```

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork repository
2. Create feature branch: `git checkout -b feature/my-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to branch: `git push origin feature/my-feature`
5. Submit pull request

### Code Style
- Follow PEP 8 for Python
- Use Django conventions
- Add docstrings to functions
- Use type hints where possible

### Adding Features
1. Create feature branch
2. Update models if needed
3. Create migrations
4. Update serializers
5. Create/update views
6. Update URLs
7. Update frontend
8. Add documentation
9. Test thoroughly
10. Submit PR

---

## 🐛 Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
python manage.py runserver 8001
```

#### Migration Errors
```bash
# Reset migrations (development only!)
python manage.py migrate zero accounts

# Create new migration
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

#### Static Files Not Loading
```bash
# Collect static files
python manage.py collectstatic

# Check STATIC_ROOT and STATICFILES_DIRS
python manage.py findstatic style.css --verbosity 2
```

#### JWT Token Issues
```bash
# Check token in browser console
localStorage.getItem('access_token')

# Decode token (copy to jwt.io)
# Verify expiration: exp > current_time_in_seconds
```

#### Database Issues
```bash
# Reset database
rm db.sqlite3

# Recreate
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### Debug Mode

Enable Django debug toolbar:
```bash
pip install django-debug-toolbar

# Add to INSTALLED_APPS
'debug_toolbar',

# Add to MIDDLEWARE
'debug_toolbar.middleware.DebugToolbarMiddleware',

# Add to URLs
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
```

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 👨‍💻 Author

**Developed by:** Prathamesh Anand  
**Contact:** [prathameshsci963@gmail.com]  
**GitHub:** [https://github.com/Prathameshsci369]  

---

## 🙏 Acknowledgments

- Django & DRF communities
- Bootstrap team
- simplejwt developers
- All contributors

---

## 📞 Support

Need help? Check these resources:

1. **Documentation**
   - [Django Docs](https://docs.djangoproject.com/)
   - [DRF Docs](https://www.django-rest-framework.org/)
   - [JWT Docs](https://django-rest-framework-simplejwt.readthedocs.io/)

2. **Project Documentation**
   - `JWT_IMPLEMENTATION.md` - JWT authentication guide
   - `JWT_QUICK_START.md` - Quick start guide
   - `IMPLEMENTATION_SUMMARY.md` - Implementation overview

3. **Community**
   - Django Community Forum
   - Stack Overflow
   - GitHub Issues

---

<div align="center">

**⭐ If you found this helpful, please star the repository! ⭐**

Made with ❤️ by [Prathamesh Anand]

</div>
