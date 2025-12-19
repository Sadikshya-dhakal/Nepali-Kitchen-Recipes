// PahiloKhana - Custom JavaScript

// ============================================
// Mobile Menu Toggle
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }
});

// ============================================
// Star Rating System
// ============================================
function initStarRating() {
    const stars = document.querySelectorAll('.star-rating i');
    
    stars.forEach((star, index) => {
        star.addEventListener('click', function() {
            // Remove active class from all stars
            stars.forEach(s => s.classList.remove('fas', 'text-yellow-400'));
            stars.forEach(s => s.classList.add('far', 'text-gray-300'));
            
            // Add active class to clicked star and all previous stars
            for (let i = 0; i <= index; i++) {
                stars[i].classList.remove('far', 'text-gray-300');
                stars[i].classList.add('fas', 'text-yellow-400');
            }
            
            // Store rating value (index + 1)
            const rating = index + 1;
            console.log('Rating:', rating);
            // You can send this to your backend here
        });
        
        // Hover effect
        star.addEventListener('mouseenter', function() {
            for (let i = 0; i <= index; i++) {
                if (!stars[i].classList.contains('fas')) {
                    stars[i].classList.add('text-yellow-400');
                }
            }
        });
        
        star.addEventListener('mouseleave', function() {
            stars.forEach(s => {
                if (!s.classList.contains('fas')) {
                    s.classList.remove('text-yellow-400');
                }
            });
        });
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', initStarRating);

// ============================================
// Servings Adjuster
// ============================================
function adjustServings(action) {
    const servingsDisplay = document.querySelector('#servings-display');
    let currentServings = parseInt(servingsDisplay.textContent);
    
    if (action === 'increase') {
        currentServings++;
    } else if (action === 'decrease' && currentServings > 1) {
        currentServings--;
    }
    
    servingsDisplay.textContent = currentServings;
    
    // Update ingredient quantities
    updateIngredients(currentServings);
}

function updateIngredients(newServings) {
    const baseServings = 4; // Default servings
    const multiplier = newServings / baseServings;
    
    const ingredients = document.querySelectorAll('.ingredient-amount');
    ingredients.forEach(ingredient => {
        const baseAmount = parseFloat(ingredient.dataset.base);
        const newAmount = (baseAmount * multiplier).toFixed(1);
        ingredient.textContent = newAmount.replace('.0', '');
    });
}

// ============================================
// Search Functionality
// ============================================
function searchRecipes() {
    const searchInput = document.querySelector('#recipe-search');
    const searchTerm = searchInput.value.toLowerCase();
    
    // In Django, you would submit the form or make an AJAX request
    console.log('Searching for:', searchTerm);
    
    // Example: Redirect to search results page
    // window.location.href = `/search?q=${encodeURIComponent(searchTerm)}`;
}

// ============================================
// Like/Save Recipe
// ============================================
function toggleLike(recipeId) {
    const likeBtn = document.querySelector(`#like-btn-${recipeId}`);
    const icon = likeBtn.querySelector('i');
    
    if (icon.classList.contains('far')) {
        icon.classList.remove('far');
        icon.classList.add('fas', 'text-red-500');
        showToast('Recipe saved to favorites!');
        
        // Send to backend
        saveRecipe(recipeId);
    } else {
        icon.classList.remove('fas', 'text-red-500');
        icon.classList.add('far');
        showToast('Recipe removed from favorites');
        
        // Send to backend
        unsaveRecipe(recipeId);
    }
}

function saveRecipe(recipeId) {
    // Django AJAX request example
    // fetch(`/api/recipes/${recipeId}/save/`, {
    //     method: 'POST',
    //     headers: {
    //         'X-CSRFToken': getCookie('csrftoken'),
    //         'Content-Type': 'application/json'
    //     }
    // });
    console.log('Saving recipe:', recipeId);
}

function unsaveRecipe(recipeId) {
    // Django AJAX request example
    console.log('Unsaving recipe:', recipeId);
}

// ============================================
// Toast Notification
// ============================================
function showToast(message, duration = 3000) {
    // Create toast element
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `
        <div class="flex items-center gap-3">
            <i class="fas fa-check-circle text-green-500 text-xl"></i>
            <span class="text-gray-800">${message}</span>
        </div>
    `;
    
    document.body.appendChild(toast);
    
    // Show toast
    setTimeout(() => {
        toast.classList.add('show');
    }, 100);
    
    // Hide and remove toast
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, duration);
}

// ============================================
// Smooth Scroll to Section
// ============================================
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

// ============================================
// Print Recipe
// ============================================
function printRecipe() {
    window.print();
}

// ============================================
// Share Recipe
// ============================================
function shareRecipe(title, url) {
    if (navigator.share) {
        navigator.share({
            title: title,
            url: url
        }).then(() => {
            console.log('Recipe shared successfully');
        }).catch(console.error);
    } else {
        // Fallback: Copy to clipboard
        navigator.clipboard.writeText(url);
        showToast('Link copied to clipboard!');
    }
}

// ============================================
// Image Gallery (Recipe Detail)
// ============================================
function initImageGallery() {
    const mainImage = document.querySelector('#main-recipe-image');
    const thumbnails = document.querySelectorAll('.recipe-thumbnail');
    
    if (mainImage && thumbnails.length > 0) {
        thumbnails.forEach(thumbnail => {
            thumbnail.addEventListener('click', function() {
                mainImage.src = this.src;
                
                // Remove active class from all thumbnails
                thumbnails.forEach(t => t.classList.remove('ring-2', 'ring-orange-500'));
                
                // Add active class to clicked thumbnail
                this.classList.add('ring-2', 'ring-orange-500');
            });
        });
    }
}

document.addEventListener('DOMContentLoaded', initImageGallery);

// ============================================
// Form Validation
// ============================================
function validateContactForm(event) {
    event.preventDefault();
    
    const name = document.querySelector('#contact-name').value.trim();
    const email = document.querySelector('#contact-email').value.trim();
    const message = document.querySelector('#contact-message').value.trim();
    
    if (!name || !email || !message) {
        showToast('Please fill in all required fields', 3000);
        return false;
    }
    
    if (!isValidEmail(email)) {
        showToast('Please enter a valid email address', 3000);
        return false;
    }
    
    // Submit form
    event.target.submit();
    showToast('Message sent successfully!', 3000);
}

function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// ============================================
// Lazy Load Images
// ============================================
function lazyLoadImages() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

document.addEventListener('DOMContentLoaded', lazyLoadImages);

// ============================================
// Filter Recipes by Difficulty
// ============================================
function filterByDifficulty(difficulty) {
    const recipes = document.querySelectorAll('.recipe-card');
    
    recipes.forEach(recipe => {
        if (difficulty === 'all') {
            recipe.style.display = 'block';
        } else {
            const recipeDifficulty = recipe.dataset.difficulty;
            recipe.style.display = recipeDifficulty === difficulty ? 'block' : 'none';
        }
    });
}

// ============================================
// Sort Recipes
// ============================================
function sortRecipes(sortBy) {
    // In Django, you would typically do this server-side
    // But here's a client-side example
    console.log('Sorting by:', sortBy);
    
    // Redirect with sort parameter
    const url = new URL(window.location);
    url.searchParams.set('sort', sortBy);
    window.location.href = url.toString();
}

// ============================================
// Get CSRF Token (Django)
// ============================================
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

// ============================================
// Scroll to Top Button
// ============================================
function initScrollToTop() {
    const scrollBtn = document.createElement('button');
    scrollBtn.id = 'scroll-to-top';
    scrollBtn.className = 'fixed bottom-8 right-8 bg-orange-500 text-white w-12 h-12 rounded-full shadow-lg hover:bg-orange-600 transition-all hidden z-50';
    scrollBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
    document.body.appendChild(scrollBtn);
    
    // Show/hide button based on scroll position
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            scrollBtn.classList.remove('hidden');
        } else {
            scrollBtn.classList.add('hidden');
        }
    });
    
    // Scroll to top when clicked
    scrollBtn.addEventListener('click', function() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

document.addEventListener('DOMContentLoaded', initScrollToTop);

// ============================================
// Recipe Comment Form
// ============================================
function submitComment(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    
    // Django AJAX request example
    // fetch(form.action, {
    //     method: 'POST',
    //     body: formData,
    //     headers: {
    //         'X-CSRFToken': getCookie('csrftoken')
    //     }
    // })
    // .then(response => response.json())
    // .then(data => {
    //     showToast('Comment posted successfully!');
    //     form.reset();
    //     // Reload comments section
    // });
    
    showToast('Comment posted successfully!');
    form.reset();
}

// ============================================
// View Counter (Recipe Detail)
// ============================================
function incrementViewCount(recipeId) {
    // Send view count to backend
    // fetch(`/api/recipes/${recipeId}/view/`, {
    //     method: 'POST',
    //     headers: {
    //         'X-CSRFToken': getCookie('csrftoken')
    //     }
    // });
    console.log('View counted for recipe:', recipeId);
}

// Call this on recipe detail page load
if (window.location.pathname.includes('recipe-detail')) {
    const recipeId = 1; // Get from page data
    incrementViewCount(recipeId);
}

// ============================================
// Console Welcome Message
// ============================================
console.log('%c🍳 PahiloKhana - Nepali Recipe Platform', 'color: #f97316; font-size: 20px; font-weight: bold;');
console.log('%cWelcome to the best Nepali recipe website!', 'color: #dc2626; font-size: 14px;');