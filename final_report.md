# E-Commerce Web Application - Final Report

## Project Overview

This project is a Django-based e-commerce web application that sells food products using open data from the Open Food Facts database. The application allows users to browse products, add them to a cart, place orders, and manage their account. It also provides an admin interface for managing products, orders, and users.

## Design

### Architecture

The application follows the Model-View-Template (MVT) architecture of Django:

- **Models**: Define the database structure with tables for products, categories, orders, and users
- **Views**: Handle HTTP requests and business logic
- **Templates**: Render HTML for the user interface

### Database Design

The database consists of several interconnected tables:

1. **Category**: Organizes products into categories
2. **Product**: Stores product information, linked to Category
3. **Cart & CartItem**: Manage the shopping cart functionality
4. **Order & OrderItem**: Handle order processing
5. **User & Profile**: Manage user authentication and profiles
6. **Review**: Stores product reviews and ratings, linked to Product and User
7. **Wishlist & WishlistItem**: Manage the wishlist functionality, linked to User and Product

This design satisfies the requirement for at least two linked tables, with multiple relationships between entities.

### User Interface

The UI is designed to be responsive and user-friendly, with:

- A clean, modern layout using Bootstrap 5
- Intuitive navigation with a persistent header and footer
- Product cards with images, descriptions, and prices
- A search bar and filtering options
- A shopping cart with quantity adjustments
- A wishlist for saving products of interest
- Checkout forms with validation

## Development

### Technology Stack

- **Backend**: Python 3.11, Django 4.2
- **Database**: SQLite (development), PostgreSQL (production)
- **Frontend**: HTML, CSS, Bootstrap 5
- **Deployment**: Heroku

### Key Features Implemented

1. **Product Catalog**: Browse and search through thousands of food products
2. **Shopping Cart**: Add products to your cart and manage quantities
3. **User Authentication**: Register, login, and manage your profile
4. **Order Management**: Place orders and view order history
5. **Product Reviews and Ratings**: Leave reviews and ratings for products
6. **Wishlist**: Save products for later viewing or purchasing
7. **Admin Dashboard**: Manage products, orders, and users with different access levels
8. **Search Functionality**: Search products by name, description, or category
9. **Error Handling**: Comprehensive error handling throughout the application

### Open Data Integration

The application uses the Open Food Facts API to import product data. A custom management command (`import_products.py`) fetches and processes this data, creating Product objects in the database. This satisfies the requirement to use open data records of 2000-7000 items.

### Product Reviews and Ratings

The Product Reviews and Ratings feature allows users to:

1. **Submit Reviews**: Authenticated users can submit reviews with a rating (1-5 stars), title, and detailed comment
2. **View Reviews**: All users can view reviews on product detail pages, including average ratings and total review count
3. **Edit Reviews**: Users can edit their own reviews
4. **One Review Per User**: The system ensures each user can only submit one review per product

Implementation details:

- **Model**: A Review model with fields for product, user, rating, title, comment, and timestamps
- **Form**: A ReviewForm for submitting and editing reviews
- **Views**: Updated ProductDetailView to include reviews and a new add_review view for submitting/editing reviews
- **Templates**: Enhanced product_detail.html to display reviews and the review form
- **JavaScript**: Added for toggling the edit review form

This feature enhances the user experience by providing social proof and helping customers make informed purchasing decisions.

### Wishlist Functionality

The Wishlist feature allows users to save products they're interested in for later viewing or purchasing:

1. **Save Products**: Users can add products to their wishlist from product detail pages
2. **View Wishlist**: Users can view all items in their wishlist on a dedicated page
3. **Add to Cart**: Users can add individual items or all items from their wishlist to their cart
4. **Remove Items**: Users can remove items from their wishlist
5. **Wishlist Count**: The number of items in the wishlist is displayed in the navigation bar

Implementation details:

- **Models**: 
  - Wishlist model with a one-to-one relationship to User
  - WishlistItem model linking products to wishlists with a unique constraint
- **Views**: 
  - wishlist_detail for displaying the wishlist
  - wishlist_add for adding products to the wishlist
  - wishlist_remove for removing products from the wishlist
  - Enhanced cart_add to handle adding all wishlist items to cart
- **Templates**: 
  - New wishlist_detail.html template
  - Updated base.html to include wishlist link and count
  - Updated product_detail.html to include "Add to Wishlist" button
- **Context Processor**: Added wishlist_processor to make wishlist count available in all templates

This feature enhances the user experience by allowing customers to save products for later consideration, creating a more engaging shopping experience and potentially increasing conversion rates.

## Implementation

### User Roles and Access Levels

The application implements three user roles:

1. **Guest**: Can browse products and add them to cart
2. **Customer**: Can place orders and view order history
3. **Admin**: Can manage products, orders, and users

This satisfies the requirement for different levels of access to the app.

### Testing

Comprehensive tests were written for:

- Models: Ensure data integrity and method functionality
- Views: Test HTTP responses and context data
- Forms: Validate form submission and processing
- Access Control: Verify that users can only access appropriate resources

### Error Handling

Error handling is implemented throughout the application:

- Form validation with user-friendly error messages
- Exception handling in views with appropriate error responses
- Logging of errors for debugging
- Custom error pages for 404, 500, etc.

## Deployment

The application is configured for deployment on Heroku:

1. **Procfile**: Specifies the command to run the application
2. **runtime.txt**: Specifies the Python version
3. **requirements.txt**: Lists all dependencies
4. **.env.example**: Provides a template for environment variables
5. **Database Configuration**: Uses dj-database-url to configure the database from the DATABASE_URL environment variable
6. **Static Files**: Uses whitenoise to serve static files in production

## Conclusion

This project successfully implements all the required features of a database-driven Django e-commerce application. It uses open data, provides different access levels, includes error handling and search functionality, and is configured for cloud deployment. The codebase is well-structured and includes comprehensive tests.

The application demonstrates the power and flexibility of Django for building complex web applications, and showcases best practices in web development, including security, performance, and user experience.
