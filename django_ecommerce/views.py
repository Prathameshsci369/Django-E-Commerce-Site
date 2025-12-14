from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from products.models import Product

class HomeView(TemplateView):
    template_name = 'home.html'


class LoginPageView(View):
    """Render the login page."""
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, 'login.html')


class RegisterPageView(View):
    """Render the registration page."""
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, 'register.html')


class ProductDetailView(View):
    """Display detailed view of a single product."""
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug, is_active=True)
        # Get related products from the same category
        related_products = Product.objects.filter(
            category=product.category,
            is_active=True
        ).exclude(id=product.id)[:4]
        
        context = {
            'product': product,
            'related_products': related_products,
        }
        return render(request, 'product_detail.html', context)
