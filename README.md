# E-Commerce Web Application

A Django-based e-commerce web application that sells food products using open data from the Open Food Facts database.

## Features

- **Product Catalog**: Browse and search through thousands of food products
- **Shopping Cart**: Add products to your cart and manage quantities
- **User Authentication**: Register, login, and manage your profile
- **Order Management**: Place orders and view order history
- **Product Reviews and Ratings**: Leave reviews and ratings for products
- **Rating Statistics**: View detailed breakdown of product ratings with distribution charts
- **Recently Viewed Products**: Track and display products you've recently viewed
- **Product Comparison**: Compare multiple products side by side
- **Discount Coupons**: Apply coupon codes during checkout for discounts
- **Admin Dashboard**: Manage products, orders, and users with different access levels
- **Responsive Design**: Works on desktop and mobile devices

## Technology Stack

- **Backend**: Python 3.11, Django 4.2
- **Database**: SQLite (development), PostgreSQL (production)
- **Static File Serving**: WhiteNoise
- **Deployment**: Heroku
- **Database**: SQLite (development), PostgreSQL (production)
- **Frontend**: HTML, CSS, Bootstrap 5
- **Deployment**: Heroku

## Installation

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Git

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ecommerce.git
   cd ecommerce
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env file with your settings
   ```

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Import products from Open Food Facts:
   ```bash
   python manage.py import_products --limit 2000
   ```

8. Run the development server:
   ```bash
   python manage.py runserver
   ```

9. Access the application at http://127.0.0.1:8000/

## Project Structure

```bash
ecommerce/
├── ecommerce/              # Main project directory
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py         # Project settings
│   ├── urls.py             # Main URL configuration
│   └── wsgi.py
├── store/                  # Store app
│   ├── management/         # Custom management commands
│   │   └── commands/
│   │       └── import_products.py  # Command to import products
│   ├── migrations/         # Database migrations
│   ├── templates/          # HTML templates
│   ├── __init__.py
│   ├── admin.py            # Admin configuration
│   ├── apps.py
│   ├── context_processors.py  # Context processors
│   ├── forms.py            # Forms
│   ├── models.py           # Database models
│   ├── tests.py            # Tests
│   ├── urls.py             # URL patterns
│   └── views.py            # Views
├── users/                  # Users app
│   ├── migrations/
│   ├── templates/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── signals.py
│   ├── tests.py
│   └── views.py
├── static/                 # Static files
├── media/                  # User-uploaded files
├── templates/              # Project-wide templates
├── .env.example            # Environment variables template
├── .gitignore
├── manage.py               # Django management script
├── Procfile                # Heroku deployment configuration
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies
└── runtime.txt             # Python runtime for Heroku
```

## Database Design

The application uses several interconnected models:

1. **Category**: Organizes products into categories
2. **Product**: Stores product information, linked to Category
3. **Cart**: Represents a user's shopping cart
4. **CartItem**: Items in a cart, linked to Cart and Product
5. **Order**: Stores order information, linked to User
6. **OrderItem**: Items in an order, linked to Order and Product
7. **Profile**: Extends the User model with additional information
8. **Review**: Stores product reviews and ratings, linked to Product and User
9. **Wishlist**: Represents a user's wishlist of products
10. **WishlistItem**: Items in a wishlist, linked to Wishlist and Product
11. **RecentlyViewedProduct**: Tracks products a user has recently viewed, linked to User and Product
12. **Coupon**: Stores discount coupon information including code, validity period, and discount amount
13. **CouponUse**: Tracks coupon usage by users, linked to Coupon, User, and Order
14. **ComparisonList**: Represents a user's product comparison list
15. **ComparisonItem**: Items in a comparison list, linked to ComparisonList and Product

## User Roles

The application supports three user roles:

1. **Guest**: Can browse products and add them to cart
2. **Customer**: Can place orders and view order history
3. **Admin**: Can manage products, orders, and users

## Deployment

### GitHub Deployment

For instructions on how to deploy this project to GitHub, please see the [GitHub Deployment Guide](GITHUB_DEPLOYMENT.md).

### Heroku Deployment

The application is configured for deployment on Heroku. You can deploy it in two ways:

#### Manual Deployment

1. Create a Heroku account and install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)

2. Login to your Heroku account:
   ```bash
   heroku login
   ```

3. Create a new Heroku app:
   ```bash
   heroku create your-app-name
   ```

4. Configure environment variables:
   ```bash
   heroku config:set SECRET_KEY=your_secret_key
   heroku config:set DEBUG=False
   heroku config:set DJANGO_SETTINGS_MODULE=ecommerce.settings
   heroku config:set HEROKU_APP_NAME=your-app-name
   ```

5. Add PostgreSQL addon:
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

6. Deploy the application:
   ```bash
   git push heroku main
   ```

7. Run migrations and collect static files:
   ```bash
   heroku run 'cd ecommerce && python manage.py migrate'
   heroku run 'cd ecommerce && python manage.py collectstatic --noinput'
   ```

8. Create a superuser:
   ```bash
   heroku run 'cd ecommerce && python manage.py createsuperuser'
   ```

#### Automated Deployment

For an easier deployment, use the included script:

```bash
python setup_heroku.py
```

This script will guide you through the process of creating a Heroku app, configuring it, and deploying your application.

#### GitHub Actions Deployment

The project includes a GitHub Actions workflow that automatically deploys to Heroku when you push to the main branch. To set it up:

1. Add the following secrets to your GitHub repository:
   - `HEROKU_API_KEY`: Your Heroku API key
   - `HEROKU_APP_NAME`: Your Heroku app name
   - `HEROKU_EMAIL`: Your Heroku email
   - `SECRET_KEY`: A secret key for Django

2. Push to the main branch, and GitHub Actions will deploy your application.

8. Import products:
   ```bash
   heroku run python manage.py import_products --limit 2000
   ```

## Testing

The application includes comprehensive tests for models, views, and forms. Run the tests with:

```bash
python manage.py test
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Open Food Facts](https://world.openfoodfacts.org/) for providing the open data used in this project
- [Django](https://www.djangoproject.com/) for the web framework
- [Bootstrap](https://getbootstrap.com/) for the frontend framework
