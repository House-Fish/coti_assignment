from flask import Flask, render_template, request, redirect, url_for, flash, session
from jinja2 import Environment
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.jinja_env.globals.update(min=min)

# Initialize LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Configure logging
if not os.path.exists('logs'):
    os.mkdir('logs')

file_handler = RotatingFileHandler('logs/ecommerce.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('E-commerce startup')

# In-memory storage
class User(UserMixin):
    def __init__(self, id, username, email, password_hash):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Sample users
users = {
    1: User(1, 'hi', 'john@example.com', 
            generate_password_hash('hi')),
    2: User(2, 'jane_smith', 'jane@example.com', 
            generate_password_hash('password456'))
}

username_to_id = {user.username: user_id for user_id, user in users.items()}

# Sample products
products = [
    {
        'id': 1,
        'name': 'Laptop',
        'description': 'High-performance laptop with 16GB RAM and 512GB SSD',
        'price': 999.99,
        'stock': 10,
        'image_url': '/static/images/laptop.jpg'
    },
    {
        'id': 2,
        'name': 'Smartphone',
        'description': 'Latest smartphone with 5G capability and amazing camera',
        'price': 699.99,
        'stock': 15,
        'image_url': '/static/images/smartphone.jpg'
    },
    {
        'id': 3,
        'name': 'Headphones',
        'description': 'Noise-cancelling wireless headphones',
        'price': 199.99,
        'stock': 20,
        'image_url': '/static/images/headphones.jpg'
    }
]

# In-memory orders storage
orders = {}
order_counter = 1

# Valid cards for payment
VALID_CARDS = [
    {
        'number': '4111111111111111',
        'expiry': '12/25',
        'cvv': '123'
    },
    {
        'number': '5555555555554444',
        'expiry': '12/25',
        'cvv': '456'
    },
    {
        'number': '378282246310005',
        'expiry': '12/25',
        'cvv': '789'
    }
]

@login_manager.user_loader
def load_user(user_id):
    return users.get(int(user_id))

@app.route('/')
def index():
    app.logger.info('Homepage accessed')
    return render_template('index.html', products=products)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_id = username_to_id.get(username)
        
        if user_id:
            user = users[user_id]
            if user.check_password(password):
                login_user(user)
                app.logger.info(f'User {username} logged in successfully')
                return redirect(url_for('index'))
        
        app.logger.warning(f'Failed login attempt for username: {username}')
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if username in username_to_id:
            flash('Username already exists')
            return redirect(url_for('register'))
        
        user_id = max(users.keys()) + 1
        users[user_id] = User(
            id=user_id,
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        username_to_id[username] = user_id
        
        app.logger.info(f'New user registered: {username}')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        app.logger.info(f'Product viewed: {product["name"]}')
        return render_template('product_detail.html', product=product)
    return redirect(url_for('index'))

@app.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    if 'cart' not in session:
        session['cart'] = {}
    
    cart_items = []
    total = 0
    
    for product_id, quantity in session['cart'].items():
        product = next((p for p in products if p['id'] == int(product_id)), None)
        if product:
            item_total = product['price'] * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': item_total
            })
            total += item_total
    
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = {}
    
    quantity = int(request.form.get('quantity', 1))
    product = next((p for p in products if p['id'] == product_id), None)
    
    if product and product['stock'] >= quantity:
        if str(product_id) in session['cart']:
            session['cart'][str(product_id)] += quantity
        else:
            session['cart'][str(product_id)] = quantity
        
        session.modified = True
        app.logger.info(f'Product {product_id} added to cart by user {current_user.username}')
        flash('Product added to cart')
    else:
        flash('Product not available in requested quantity')
    
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    if 'cart' not in session or not session['cart']:
        return redirect(url_for('cart'))
    
    cart_items = []
    total = 0
    
    for product_id, quantity in session['cart'].items():
        product = next((p for p in products if p['id'] == int(product_id)), None)
        if product and product['stock'] >= quantity:
            item_total = product['price'] * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': item_total
            })
            total += item_total
        else:
            flash(f'Sorry, product is out of stock')
            return redirect(url_for('cart'))
    
    if request.method == 'POST':
        global order_counter
        order_id = order_counter
        order_counter += 1
        
        orders[order_id] = {
            'id': order_id,
            'user_id': current_user.id,
            'items': cart_items,
            'total_amount': total,
            'status': 'pending',
            'date_ordered': datetime.now()
        }
        
        # Update product stock
        for item in cart_items:
            product = next((p for p in products if p['id'] == item['product']['id']), None)
            if product:
                product['stock'] -= item['quantity']
        
        return render_template('payment.html', order_id=order_id, total=total)
    
    return render_template('checkout.html', cart_items=cart_items, total=total)

@app.route('/process_payment', methods=['POST'])
@login_required
def process_payment():
    order_id = int(request.form.get('order_id'))
    total = float(request.form.get('total'))
    card_number = request.form.get('card_number')
    card_expiry = request.form.get('card_expiry')
    card_cvv = request.form.get('card_cvv')
    
    is_valid = any(
        card['number'] == card_number and 
        card['expiry'] == card_expiry and 
        card['cvv'] == card_cvv 
        for card in VALID_CARDS
    )
    
    if is_valid and order_id in orders:
        orders[order_id]['status'] = 'completed'
        app.logger.info(f'Payment successful for order {order_id}')
        
        # Clear cart
        session.pop('cart', None)
        
        flash('Payment successful! Thank you for your order.')
        return redirect(url_for('orders_page'))
    else:
        app.logger.warning(f'Invalid card details provided for order {order_id}')
        flash('Invalid card details. Please try again.')
        return render_template('payment.html', order_id=order_id, total=total)
        # return redirect(url_for('checkout', order_id=order_id))

@app.route('/orders')
@login_required
def orders_page():  
    user_orders = [
        order for order in orders.values()
        if order['user_id'] == current_user.id
    ]
    return render_template('orders.html', user_orders=user_orders)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    app.logger.info(f'User logged out')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)