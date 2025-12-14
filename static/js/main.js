// Global cart functionality
let cart = [];
let cartModal;

document.addEventListener('DOMContentLoaded', function() {
    console.log('Main JS loaded');
    cartModal = new bootstrap.Modal(document.getElementById('cartModal'));
    loadCart();
    updateCartUI();
});

// Cart functions
async function addToCart(productId, quantity = 1) {
    console.log('Adding to cart:', productId, quantity);
    
    try {
        const response = await fetch('/api/cart/add_item/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                product_id: productId,
                quantity: quantity
            })
        });

        if (response.ok) {
            const data = await response.json();
            cart = data.items || [];
            updateCartUI();
            showToast('Product added to cart!', 'success');
        } else {
            showToast('Failed to add to cart', 'error');
        }
    } catch (error) {
        console.error('Error adding to cart:', error);
        showToast('Error adding to cart', 'error');
    }
}

async function removeFromCart(productId) {
    try {
        const response = await fetch(`/api/cart/remove_item/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                product_id: productId
            })
        });

        if (response.ok) {
            cart = cart.filter(item => item.product_id !== productId);
            updateCartUI();
            showToast('Product removed from cart', 'info');
        }
    } catch (error) {
        console.error('Error removing from cart:', error);
    }
}

async function updateCartItemQuantity(productId, quantity) {
    if (quantity <= 0) {
        removeFromCart(productId);
        return;
    }

    try {
        const response = await fetch('/api/cart/update_item/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                product_id: productId,
                quantity: quantity
            })
        });

        if (response.ok) {
            const data = await response.json();
            cart = data.items || [];
            updateCartUI();
        }
    } catch (error) {
        console.error('Error updating cart:', error);
    }
}

function updateCartUI() {
    const cartCount = document.getElementById('cartCount');
    const cartItems = document.getElementById('cartItems');
    const cartTotal = document.getElementById('cartTotal');

    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    const totalPrice = cart.reduce((sum, item) => sum + (item.product.price * item.quantity), 0);

    cartCount.textContent = totalItems;
    cartTotal.textContent = totalPrice.toFixed(2);

    if (cart.length === 0) {
        cartItems.innerHTML = '<p>Your cart is empty</p>';
        return;
    }

    cartItems.innerHTML = cart.map(item => `
        <div class="cart-item d-flex align-items-center mb-3">
            <img src="${item.product.primary_image ? item.product.primary_image.image : '/static/images/placeholder.jpg'}" 
                 alt="${item.product.name}" class="me-3" style="width: 50px; height: 50px; object-fit: cover;">
            <div class="flex-grow-1">
                <h6>${item.product.name}</h6>
                <div class="d-flex align-items-center">
                    <button class="btn btn-sm btn-outline-secondary me-2" onclick="updateCartItemQuantity(${item.product_id}, ${item.quantity - 1})">-</button>
                    <span>${item.quantity}</span>
                    <button class="btn btn-sm btn-outline-secondary ms-2" onclick="updateCartItemQuantity(${item.product_id}, ${item.quantity + 1})">+</button>
                </div>
            </div>
            <div class="text-end">
                <strong>$${(item.product.price * item.quantity).toFixed(2)}</strong>
                <button class="btn btn-sm btn-outline-danger ms-2" onclick="removeFromCart(${item.product_id})">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `).join('');
}

function toggleCart() {
    cartModal.toggle();
}

function checkout() {
    window.location.href = '/checkout/';
}

// Utility functions
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function showToast(message, type = 'info') {
    console.log('Toast:', message, type);
    // You can implement a toast notification here if needed
}