let currentPage = 1;
let currentFilters = {};
let hasMoreProducts = true;
let allCategories = []; // Store all categories globally

/**
 * Get headers with JWT token if available
 */
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

document.addEventListener('DOMContentLoaded', function() {
    console.log('Home page loaded');
    loadCategories();
    loadProducts();
    setupEventListeners();
});

function setupEventListeners() {
    document.getElementById('searchInput').addEventListener('keyup', function(e) {
        if (e.key === 'Enter') {
            searchProducts();
        }
    });

    document.getElementById('sortBy').addEventListener('change', function() {
        currentFilters.ordering = this.value;
        resetAndLoadProducts();
    });

    document.getElementById('featuredOnly').addEventListener('change', function() {
        currentFilters.featured = this.checked;
        resetAndLoadProducts();
    });
}

async function loadCategories() {
    try {
        console.log('Loading categories...');
        const response = await fetch('/api/products/categories/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Categories loaded:', data);
        allCategories = data.results || data; // Store categories globally
        
        const categoryFilters = document.getElementById('categoryFilters');
        categoryFilters.innerHTML = `
            <div class="form-check">
                <input class="form-check-input" type="radio" name="category" id="allCategories" value="" checked>
                <label class="form-check-label" for="allCategories">
                    All Categories
                </label>
            </div>
        `;

        // Add category options
        if (allCategories && allCategories.length > 0) {
            allCategories.forEach(category => {
                categoryFilters.innerHTML += `
                    <div class="form-check">
                        <input class="form-check-input" type="radio" name="category" id="category_${category.id}" value="${category.slug}">
                        <label class="form-check-label" for="category_${category.id}">
                            ${category.name} (${category.product_count || 0})
                        </label>
                    </div>
                `;
            });

            // Add event listeners to category radio buttons
            document.querySelectorAll('input[name="category"]').forEach(radio => {
                radio.addEventListener('change', function() {
                    currentFilters.category = this.value;
                    resetAndLoadProducts();
                });
            });
        }
    } catch (error) {
        console.error('Error loading categories:', error);
        showToast('Error loading categories', 'error');
    }
}

async function loadProducts(append = false) {
    if (!append) {
        currentPage = 1;
        hasMoreProducts = true;
    }

    showLoading(true);
    console.log('Loading products with filters:', currentFilters);

    try {
        const params = new URLSearchParams({
            page: currentPage,
            ...currentFilters
        });

        const response = await fetch(`/api/products/products/?${params}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Products loaded:', data);
        
        if (append) {
            appendProducts(data.results || data);
        } else {
            displayProducts(data.results || data);
        }

        updateProductCount(data.count || data.results?.length || 0);
        
        hasMoreProducts = data.next !== null;
        document.getElementById('loadMoreBtn').style.display = hasMoreProducts ? 'block' : 'none';
        
        currentPage++;
    } catch (error) {
        console.error('Error loading products:', error);
        showToast('Error loading products', 'error');
    } finally {
        showLoading(false);
    }
}

function displayProducts(products) {
    const productsGrid = document.getElementById('productsGrid');
    
    if (!products || products.length === 0) {
        productsGrid.innerHTML = '<div class="col-12"><p>No products found</p></div>';
        return;
    }

    console.log('Displaying products:', products);
    productsGrid.innerHTML = products.map(product => createProductCard(product)).join('');
}

function appendProducts(products) {
    const productsGrid = document.getElementById('productsGrid');
    products.forEach(product => {
        productsGrid.insertAdjacentHTML('beforeend', createProductCard(product));
    });
}

function createProductCard(product) {
    console.log('Creating product card for:', product);
    
    const discountPercentage = product.discount_percentage > 0 ? 
        `<span class="badge bg-danger">-${product.discount_percentage}%</span>` : '';
    
    const comparePrice = product.compare_price ? 
        `<span class="text-muted text-decoration-line-through">$${product.compare_price}</span>` : '';

    const featuredBadge = product.is_featured ? 
        '<span class="badge bg-warning">Featured</span>' : '';

    const stockStatus = product.quantity > 0 ? 
        `<span class="text-success">${product.quantity} in stock</span>` : 
        '<span class="text-danger">Out of stock</span>';

    // Handle primary image
    let imageUrl = '/static/images/placeholder.svg';
    if (product.primary_image && product.primary_image.image) {
        imageUrl = product.primary_image.image;
    } else if (product.images && product.images.length > 0) {
        imageUrl = product.images[0].image;
    }

    return `
        <div class="col-md-6 col-lg-4 mb-4">
            <div class="card h-100">
                <div class="position-relative">
                    <img src="${imageUrl}" 
                         class="card-img-top" alt="${product.name}" style="height: 200px; object-fit: cover;">
                    <div class="position-absolute top-0 start-0 p-2">
                        ${discountPercentage}
                        ${featuredBadge}
                    </div>
                </div>
                <div class="card-body d-flex flex-column">
                    <h5 class="card-title">${product.name}</h5>
                    <p class="card-text flex-grow-1">${product.description ? product.description.substring(0, 100) + '...' : ''}</p>
                    <div class="mb-2">
                        <small class="text-muted">${product.category ? product.category.name : 'No Category'}</small>
                    </div>
                    <div class="mb-2">
                        <strong>$${product.price}</strong> ${comparePrice}
                    </div>
                    <div class="mb-2">
                        <small>${stockStatus}</small>
                    </div>
                    <div class="d-flex gap-2">
                        <button class="btn btn-primary flex-grow-1" 
                                onclick="addToCart(${product.id})"
                                ${product.quantity === 0 ? 'disabled' : ''}>
                            <i class="fas fa-shopping-cart"></i> Add to Cart
                        </button>
                        <a href="/product/${product.slug}/" class="btn btn-outline-secondary">
                            <i class="fas fa-eye"></i>
                        </a>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function updateProductCount(count) {
    const productCount = document.getElementById('productCount');
    if (productCount) {
        productCount.textContent = `${count} products found`;
    }
}

function searchProducts() {
    const searchTerm = document.getElementById('searchInput').value.trim();
    currentFilters.search = searchTerm || undefined;
    resetAndLoadProducts();
}

function resetAndLoadProducts() {
    currentPage = 1;
    hasMoreProducts = true;
    loadProducts(false);
}

function loadMoreProducts() {
    if (hasMoreProducts) {
        loadProducts(true);
    }
}

function showLoading(show) {
    const spinner = document.getElementById('loadingSpinner');
    spinner.style.display = show ? 'block' : 'none';
}

function showToast(message, type = 'info') {
    console.log('Toast:', message, type);
    // You can implement a toast notification here if needed
}

// Helper to get CSRF token from cookies
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

// Add to Cart functionality
async function addToCart(productId) {
    try {
        const response = await fetch('/api/cart/cart/add_item/', {
            method: 'POST',
            headers: getAuthHeaders(),
            credentials: 'include',
            body: JSON.stringify({
                product_id: productId,
                quantity: 1
            })
        });

        const data = await response.json();
        
        if (response.ok) {
            showToast('Product added to cart successfully!', 'success');
            location.reload();
        } else if (response.status === 401) {
            alert('Please login to add items to cart');
            window.location.href = '/login/';
        } else {
            const errorMsg = data.error || data.non_field_errors?.[0] || 'Failed to add to cart';
            showToast('Error: ' + errorMsg, 'error');
        }
    } catch (error) {
        console.error('Error adding to cart:', error);
        showToast('An error occurred while adding to cart', 'error');
    }
}

// Remove from Cart functionality
async function removeFromCart(productId) {
    try {
        const response = await fetch('/api/cart/cart/remove_item/', {
            method: 'POST',
            headers: getAuthHeaders(),
            credentials: 'include',
            body: JSON.stringify({
                product_id: productId
            })
        });

        if (response.ok) {
            showToast('Product removed from cart', 'success');
            location.reload();
        } else {
            showToast('Failed to remove product from cart', 'error');
        }
    } catch (error) {
        console.error('Error removing from cart:', error);
        showToast('An error occurred', 'error');
    }
}

// Update Cart Item Quantity
async function updateCartItemQuantity(productId, newQuantity) {
    if (newQuantity < 1) {
        removeFromCart(productId);
        return;
    }

    try {
        const response = await fetch('/api/cart/cart/update_item/', {
            method: 'POST',
            headers: getAuthHeaders(),
            credentials: 'include',
            body: JSON.stringify({
                product_id: productId,
                quantity: newQuantity
            })
        });

        if (response.ok) {
            location.reload();
        } else {
            showToast('Failed to update cart', 'error');
        }
    } catch (error) {
        console.error('Error updating cart:', error);
        showToast('An error occurred', 'error');
    }
}