from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import UserViewSet, AddressViewSet, register_view, login_view, logout_view

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'addresses', AddressViewSet, basename='address')

urlpatterns = [
    path('', include(router.urls)),
    # Authentication endpoints
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    # JWT Token endpoints
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
