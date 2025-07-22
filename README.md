# BuyMe - E-commerce Website

A full-featured e-commerce web application built with Django that allows users to browse products, manage their shopping cart, and place orders with cash on delivery payment option.

## Features

### User Management
- Custom user registration and authentication system
- Email-based login (users can login with email instead of username)
- User profile management with first name, last name support
- Secure logout functionality

### Product Management
- Product catalog with categories
- Product search functionality (by name or price)
- Category-based filtering
- Detailed product pages with descriptions and images
- Product image handling with fallback for missing images

### Shopping Cart
- Add/remove items from cart
- Update item quantities
- Persistent cart using cookies for guest users
- Database-backed cart for authenticated users
- Real-time cart total calculations

### Order Management
- Complete checkout process with shipping information
- Cash on Delivery payment method
- Order history for registered users
- Order tracking with transaction IDs
- Shipping address management

### Admin Features
- Django admin integration for all models
- Easy product and category management
- Order and customer management

## Technology Stack

- **Backend**: Django 5.2.3
- **Frontend**: HTML, CSS, Bootstrap 4, JavaScript
- **Database**: MySql
- **Authentication**: Custom Django authentication with email login
- **Image Handling**: Django ImageField

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd eshop-project
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install django pillow
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Project Structure

```
eshop/
├── migrations/          # Database migration files
├── templates/eshop/     # HTML templates
│   ├── main.html       # Base template
│   ├── store.html      # Product listing page
│   ├── cart.html       # Shopping cart page
│   ├── checkout.html   # Checkout page
│   ├── login.html      # Login page
│   ├── register.html   # Registration page
│   ├── order_history.html  # User order history
│   └── product_detail.html # Product detail page
├── models.py           # Database models
├── views.py            # View functions
├── urls.py             # URL routing
├── admin.py            # Admin configuration
├── utils.py            # Utility functions
└── backend.py          # Custom authentication backend
```

## Models

### Customer
- Extends Django's AbstractUser
- Custom fields: name, email (unique)
- Email-based authentication

### Category
- Product categories
- Simple name field

### Product
- Product information (name, price, description)
- Category relationship
- Image handling
- Stock management
- Active/inactive status

### Order
- Customer orders
- Order totals and item counts
- Transaction tracking
- Payment method support

### OrderItem
- Individual items in orders
- Quantity and pricing calculations

### ShippingAddress
- Customer shipping information
- Linked to orders and customers

### OrderHistory
- Order tracking and history

## Key Features Explained

### Cookie-Based Cart for Guests
The application supports shopping carts for both authenticated and guest users. Guest users' cart data is stored in browser cookies and seamlessly transferred when they register or login.

### Email Authentication
Users can login using their email address instead of username, implemented through a custom authentication backend.

### Real-time Cart Updates
The cart updates dynamically using JavaScript without page refreshes, providing a smooth user experience.

### Responsive Design
Bootstrap 4 ensures the application works well on both desktop and mobile devices.

## Usage

### For Customers
1. **Browse Products**: Visit the main store page to see all products
2. **Search & Filter**: Use the search bar or category filters to find products
3. **Add to Cart**: Click "Add to Cart" on any product
4. **View Cart**: Click the cart icon to review items
5. **Checkout**: Proceed to checkout and fill in shipping information
6. **Track Orders**: Registered users can view their order history

### For Administrators
1. **Access Admin Panel**: Go to `/admin/` and login with superuser credentials
2. **Manage Products**: Add, edit, or delete products and categories
3. **View Orders**: Monitor customer orders and their status
4. **Manage Users**: View and manage customer accounts

## Configuration

### Settings Required
Make sure your Django settings include:
- `MEDIA_URL` and `MEDIA_ROOT` for image uploads
- Custom authentication backend in `AUTHENTICATION_BACKENDS`
- Proper static files configuration

### Custom Authentication Backend
The project uses a custom authentication backend (`eshop.backend.EmailBackend`) that allows login with email addresses.

## Development

### Adding New Features
1. **Models**: Add new models in `models.py`
2. **Views**: Create corresponding views in `views.py`
3. **Templates**: Add HTML templates in `templates/eshop/`
4. **URLs**: Update URL patterns in `urls.py`
5. **Admin**: Register new models in `admin.py`

### Database Changes
After modifying models, always run:
```bash
python manage.py makemigrations eshop
python manage.py migrate
```

## Deployment Considerations

For production deployment:
1. Change `DEBUG = False` in settings
2. Set proper `ALLOWED_HOSTS`
3. Use a production database (PostgreSQL recommended)
4. Configure proper static and media file serving
5. Set up HTTPS for secure authentication
6. Configure email backend for notifications

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

---

**Note**: This is a learning/demonstration project. For production use, consider implementing additional security measures, payment gateways, and advanced e-commerce features.
