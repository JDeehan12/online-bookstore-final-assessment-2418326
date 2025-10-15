"""
Student 2418326
app.py
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from models import Book, Cart, User, Order, PaymentGateway, EmailService
import uuid
import os
import re

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')  # Required for session management

# Global storage for users and orders (in production, use a database)
users = {}  # email -> User object
orders = {}  # order_id -> Order object

# Create demo user for testing
demo_user = User("demo@bookstore.com", "demo123", "Demo User", "123 Demo Street, Demo City, DC 12345")
users["demo@bookstore.com"] = demo_user

# Create a cart instance to manage the cart
cart = Cart()

# Create a global books list to avoid duplication
BOOKS = [
    Book("The Great Gatsby", "Fiction", 10.99, "/images/books/the_great_gatsby.jpg"),
    Book("1984", "Dystopia", 8.99, "/images/books/1984.jpg"),
    Book("I Ching", "Traditional", 18.99, "/images/books/I-Ching.jpg"),
    Book("Moby Dick", "Adventure", 12.49, "/images/books/moby_dick.jpg")
]

def get_book_by_title(title):
    """Helper function to find a book by title"""
    return next((book for book in BOOKS if book.title == title), None)

def is_valid_email(email):
    """Validate email format using regex"""
    if not email:
        return False
    
    # More strict pattern requiring valid TLD
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def sanitise_text_input(text, max_length=500):
    """Sanitise text input by removing control characters and limiting length"""
    if not text:
        return text
    
    # Strip whitespace
    text = text.strip()
    
    # Remove control characters (except newlines/tabs for addresses)
    text = ''.join(char for char in text if char.isprintable() or char in '\n\t')
    
    # Limit length
    if len(text) > max_length:
        text = text[:max_length]
    
    return text

def get_current_user():
    """Helper function to get current logged-in user"""
    if 'user_email' in session:
        return users.get(session['user_email'])
    return None

def login_required(f):
    """Decorator to require login for certain routes"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    current_user = get_current_user()
    return render_template('index.html', books=BOOKS, cart=cart, current_user=current_user)


@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    book_title = request.form.get('title')
    quantity_str = request.form.get('quantity', '1')
    
    # Validate quantity input
    try:
        quantity = int(quantity_str)
        if quantity <= 0:
            flash('Quantity must be a positive number', 'error')
            return redirect(url_for('index'))
    except ValueError:
        flash('Invalid quantity. Please enter a valid number', 'error')
        return redirect(url_for('index'))
    
    book = get_book_by_title(book_title)
        
    if book:
        cart.add_book(book, quantity)
        flash(f'Added {quantity} "{book.title}" to cart!', 'success')
    else:
        flash('Book not found!', 'error')

    return redirect(url_for('index'))


@app.route('/remove-from-cart', methods=['POST'])
def remove_from_cart():
    book_title = request.form.get('title')
    cart.remove_book(book_title)
    flash(f'Removed "{book_title}" from cart!', 'success')
    return redirect(url_for('view_cart'))


@app.route('/update-cart', methods=['POST'])
def update_cart():
    """
    Update the quantity of a book in the cart.
    This function handles HTTP POST requests to update the quantity of a book in the user's cart.
    If the quantity is set to 0 or less, the book is effectively removed from the cart.
    Args:
        None (uses form data from the request)
    Returns:
        Response: Redirects to the view_cart page after updating the cart.
    Form Parameters:
        title (str): The title of the book to update.
        quantity (int): The new quantity of the book. Defaults to 1.
    Flash Messages:
        - Confirmation of removal if quantity <= 0
        - Confirmation of update otherwise
    """
    book_title = request.form.get('title')
    quantity_str = request.form.get('quantity', '1')
    
    # Validate quantity input
    try:
        quantity = int(quantity_str)
    except ValueError:
        flash('Invalid quantity. Please enter a valid number', 'error')
        return redirect(url_for('view_cart'))
    
    cart.update_quantity(book_title, quantity)
    
    if quantity <= 0:
        flash(f'Removed "{book_title}" from cart!', 'success')
    else:
        flash(f'Updated "{book_title}" quantity to {quantity}!', 'success')
    
    return redirect(url_for('view_cart'))


@app.route('/cart')
def view_cart():
    current_user = get_current_user()
    return render_template('cart.html', cart=cart, current_user=current_user)


@app.route('/clear-cart', methods=['POST'])
def clear_cart():
    cart.clear()
    flash('Cart cleared!', 'success')
    return redirect(url_for('view_cart'))


@app.route('/checkout')
def checkout():
    if cart.is_empty():
        flash('Your cart is empty!', 'error')
        return redirect(url_for('index'))
    
    current_user = get_current_user()
    total_price = cart.get_total_price()
    
    # Get preserved form data and discount from session
    form_data = session.get('form_data', {})
    discount_info = session.get('discount_info', None)
    
    # Clear form_data if coming from navigation (not from validation redirect)
    # Check if there are any flash messages - if not, this is a fresh visit
    messages = session.get('_flashes', [])
    if not messages:
        # Fresh visit - clear old form data but preserve discount
        session.pop('form_data', None)
        form_data = {}
    
    return render_template('checkout.html', 
                         cart=cart, 
                         total_price=total_price,
                         discount_info=discount_info,
                         current_user=current_user,
                         form_data=form_data)


@app.route('/process-checkout', methods=['POST'])
def process_checkout():
    """Process the checkout form with shipping and payment information"""
    if cart.is_empty():
        flash('Your cart is empty!', 'error')
        return redirect(url_for('index'))
    
    # Get form data
    shipping_info = {
        'name': sanitise_text_input(request.form.get('name')),
        'email': request.form.get('email'),
        'address': sanitise_text_input(request.form.get('address'), max_length=1000),
        'city': sanitise_text_input(request.form.get('city')),
        'zip_code': sanitise_text_input(request.form.get('zip_code'), max_length=20)
    }
    
    payment_info = {
        'payment_method': request.form.get('payment_method'),
        'card_number': request.form.get('card_number'),
        'expiry_date': request.form.get('expiry_date'),
        'cvv': request.form.get('cvv')
    }
    
    discount_code = request.form.get('discount_code', '').strip()

    # STEP 1: Check if this is ONLY a discount application (no payment info filled)
    # If user hasn't filled payment fields, they're just applying discount
    payment_fields_filled = payment_info.get('card_number') or payment_info.get('paypal_email')
    
    # If discount code provided AND no payment info, just apply discount and redirect
    if discount_code and not payment_fields_filled:
        # User is just applying discount without completing other fields
        total_amount = cart.get_total_price()
        discount_applied = 0
        discount_percentage = 0
        
        if discount_code.upper() == 'SAVE10':
            discount_percentage = 10
            discount_applied = total_amount * 0.10
        elif discount_code.upper() == 'WELCOME20':
            discount_percentage = 20
            discount_applied = total_amount * 0.20
        else:
            # Invalid discount code
            flash('Invalid discount code', 'error')
            session['form_data'] = {
                'name': shipping_info.get('name', ''),
                'email': shipping_info.get('email', ''),
                'address': shipping_info.get('address', ''),
                'city': shipping_info.get('city', ''),
                'zip_code': shipping_info.get('zip_code', '')
            }
            session.pop('discount_info', None)
            return redirect(url_for('checkout'))
        
        # Valid discount - store and redirect back to checkout
        session['discount_info'] = {
            'code': discount_code.upper(),
            'percentage': discount_percentage,
            'amount': discount_applied,
            'discounted_total': total_amount - discount_applied
        }
        session['form_data'] = {
            'name': shipping_info.get('name', ''),
            'email': shipping_info.get('email', ''),
            'address': shipping_info.get('address', ''),
            'city': shipping_info.get('city', ''),
            'zip_code': shipping_info.get('zip_code', '')
        }
        flash(f'Discount code "{discount_code.upper()}" applied! You saved ${discount_applied:.2f}', 'success')
        return redirect(url_for('checkout'))
    
    # STEP 2: Calculate total with discount (if provided with full form OR previously applied)
    total_amount = cart.get_total_price()
    discount_applied = 0
    discount_percentage = 0

    # Check if all required shipping fields are filled
    required_fields = ['name', 'email', 'address', 'city', 'zip_code']
    missing_fields = [field for field in required_fields if not shipping_info.get(field)]

    if discount_code and not missing_fields:
        # User is completing checkout with discount code
        if discount_code.upper() == 'SAVE10':
            discount_percentage = 10
            discount_applied = total_amount * 0.10
            total_amount -= discount_applied
        elif discount_code.upper() == 'WELCOME20':
            discount_percentage = 20
            discount_applied = total_amount * 0.20
            total_amount -= discount_applied
        else:
            # Invalid discount code during full checkout
            flash('Invalid discount code', 'error')
            session['form_data'] = {
                'name': shipping_info.get('name', ''),
                'email': shipping_info.get('email', ''),
                'address': shipping_info.get('address', ''),
                'city': shipping_info.get('city', ''),
                'zip_code': shipping_info.get('zip_code', '')
            }
            session.pop('discount_info', None)
            return redirect(url_for('checkout'))
        
        # Store valid discount
        session['discount_info'] = {
            'code': discount_code.upper(),
            'percentage': discount_percentage,
            'amount': discount_applied,
            'discounted_total': total_amount
        }
    elif 'discount_info' in session:
        # Use previously applied discount
        discount_info = session['discount_info']
        discount_applied = discount_info['amount']
        total_amount = discount_info['discounted_total']
    
    # STEP 3: Validate shipping information
    required_fields = ['name', 'email', 'address', 'city', 'zip_code']
    missing_fields = [field.replace("_", " ") for field in required_fields if not shipping_info.get(field)]
    if missing_fields:
        flash(f'Please fill in: {", ".join(missing_fields)}', 'error')
        session['form_data'] = {
            'name': shipping_info.get('name', ''),
            'email': shipping_info.get('email', ''),
            'address': shipping_info.get('address', ''),
            'city': shipping_info.get('city', ''),
            'zip_code': shipping_info.get('zip_code', '')
        }
        return redirect(url_for('checkout'))
    
    # Validate email format
    if not is_valid_email(shipping_info.get('email', '')):
        flash('Please enter a valid email address', 'error')
        session['form_data'] = {
            'name': shipping_info.get('name', ''),
            'email': shipping_info.get('email', ''),
            'address': shipping_info.get('address', ''),
            'city': shipping_info.get('city', ''),
            'zip_code': shipping_info.get('zip_code', '')
        }
        return redirect(url_for('checkout'))
    
    # Validate name length (minimum 2 characters)
    if len(shipping_info.get('name', '')) < 2:
        flash('Please enter a valid name (at least 2 characters)', 'error')
        session['form_data'] = {
            'name': shipping_info.get('name', ''),
            'email': shipping_info.get('email', ''),
            'address': shipping_info.get('address', ''),
            'city': shipping_info.get('city', ''),
            'zip_code': shipping_info.get('zip_code', '')
        }
        return redirect(url_for('checkout'))
    
    # Validate city length (minimum 2 characters)
    if len(shipping_info.get('city', '')) < 2:
        flash('Please enter a valid city name (at least 2 characters)', 'error')
        session['form_data'] = {
            'name': shipping_info.get('name', ''),
            'email': shipping_info.get('email', ''),
            'address': shipping_info.get('address', ''),
            'city': shipping_info.get('city', ''),
            'zip_code': shipping_info.get('zip_code', '')
        }
        return redirect(url_for('checkout'))
    
    # Validate address length (minimum 5 characters for street address)
    if len(shipping_info.get('address', '')) < 5:
        flash('Please enter a complete street address (at least 5 characters)', 'error')
        session['form_data'] = {
            'name': shipping_info.get('name', ''),
            'email': shipping_info.get('email', ''),
            'address': shipping_info.get('address', ''),
            'city': shipping_info.get('city', ''),
            'zip_code': shipping_info.get('zip_code', '')
        }
        return redirect(url_for('checkout'))
    
    # Validate zip code length (keep flexible for international - just minimum 3 characters)
    if len(shipping_info.get('zip_code', '')) < 3:
        flash('Please enter a valid postal/zip code (at least 3 characters)', 'error')
        session['form_data'] = {
            'name': shipping_info.get('name', ''),
            'email': shipping_info.get('email', ''),
            'address': shipping_info.get('address', ''),
            'city': shipping_info.get('city', ''),
            'zip_code': shipping_info.get('zip_code', '')
        }
        return redirect(url_for('checkout'))
    
    # STEP 4: Validate payment information
    if payment_info['payment_method'] == 'credit_card':
        if not payment_info.get('card_number') or not payment_info.get('expiry_date') or not payment_info.get('cvv'):
            flash('Please fill in all credit card details', 'error')
            session['form_data'] = {
                'name': shipping_info.get('name', ''),
                'email': shipping_info.get('email', ''),
                'address': shipping_info.get('address', ''),
                'city': shipping_info.get('city', ''),
                'zip_code': shipping_info.get('zip_code', '')
            }
            return redirect(url_for('checkout'))
    
    # Process payment through mock gateway
    payment_result = PaymentGateway.process_payment(payment_info)
    
    if not payment_result['success']:
        flash(payment_result['message'], 'error')
        session['form_data'] = {
            'name': shipping_info.get('name', ''),
            'email': shipping_info.get('email', ''),
            'address': shipping_info.get('address', ''),
            'city': shipping_info.get('city', ''),
            'zip_code': shipping_info.get('zip_code', '')
        }
        return redirect(url_for('checkout'))
    
    # Create order
    order_id = str(uuid.uuid4())[:8].upper()
    order = Order(
        order_id=order_id,
        user_email=shipping_info['email'],
        items=cart.get_items(),
        shipping_info=shipping_info,
        payment_info={
            'method': payment_info['payment_method'],
            'transaction_id': payment_result['transaction_id']
        },
        total_amount=total_amount
    )
    
    # Store order
    orders[order_id] = order
    
    # Add order to user if logged in
    current_user = get_current_user()
    if current_user:
        current_user.add_order(order)
    
    # Send confirmation email (mock)
    EmailService.send_order_confirmation(shipping_info['email'], order)
    
    # Clear cart and session data
    cart.clear()
    session.pop('form_data', None)
    session.pop('discount_info', None)
    
    # Store order in session for confirmation page
    session['last_order_id'] = order_id
    
    flash('Payment successful! Your order has been confirmed.', 'success')
    return redirect(url_for('order_confirmation', order_id=order_id))


@app.route('/order-confirmation/<order_id>')
def order_confirmation(order_id):
    """Display order confirmation page"""
    order = orders.get(order_id)
    if not order:
        flash('Order not found', 'error')
        return redirect(url_for('index'))
    
    current_user = get_current_user()
    return render_template('order_confirmation.html', order=order, current_user=current_user)


# User Account Management Routes

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        email = request.form.get('email').lower().strip() if request.form.get('email') else ''
        password = request.form.get('password')
        name = sanitise_text_input(request.form.get('name'))
        address = sanitise_text_input(request.form.get('address', ''), max_length=1000)
        
        # Validate required fields
        if not email or not password or not name:
            flash('Please fill in all required fields', 'error')
            return render_template('register.html')
        
        if not is_valid_email(email):
            flash('Please enter a valid email address', 'error')
            return render_template('register.html')
        
        if email in users:
            flash('An account with this email already exists', 'error')
            return render_template('register.html')
        
        # Create new user
        user = User(email, password, name, address)
        users[email] = user
        
        # Log in the user
        session['user_email'] = email
        flash('Account created successfully! You are now logged in.', 'success')
        return redirect(url_for('index'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        email = request.form.get('email').lower().strip() if request.form.get('email') else ''
        password = request.form.get('password')
        
        user = users.get(email)
        if user and user.verify_password(password):
            session['user_email'] = email
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """User logout"""
    session.pop('user_email', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))


@app.route('/account')
@login_required
def account():
    """User account page"""
    current_user = get_current_user()
    return render_template('account.html', current_user=current_user)


@app.route('/update-profile', methods=['POST'])
@login_required
def update_profile():
    """Update user profile"""
    current_user = get_current_user()
    
    current_user.name = sanitise_text_input(request.form.get('name', current_user.name))
    current_user.address = sanitise_text_input(request.form.get('address', current_user.address), max_length=1000)
    
    new_password = request.form.get('new_password')
    if new_password:
        current_user.password = current_user._hash_password(new_password)
        flash('Password updated successfully!', 'success')
    else:
        flash('Profile updated successfully!', 'success')
    
    return redirect(url_for('account'))


if __name__ == '__main__':
    app.run(debug=False)