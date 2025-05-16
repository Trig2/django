"""
Simple test script for verifying product image functionality.
Run with: python manage.py shell < test_product_image.py
"""

import os
import json
from django.core.files.images import ImageFile
from store.models import Product, ProductImage, ProductHistory, Category
from django.contrib.auth.models import User
from django.conf import settings

# Check if PIL is installed
try:
    from PIL import Image
    print("PIL is installed correctly.")
except ImportError:
    print("WARNING: PIL/Pillow is not installed. Image resizing won't work.")

# Create a test category
try:
    category = Category.objects.get(name='Test Category')
except Category.DoesNotExist:
    category = Category.objects.create(name='Test Category', description='Test category description')
    print(f"Created test category: {category}")

# Create or get a test product
try:
    product = Product.objects.get(name='Test Product')
    print(f"Found existing test product: {product}")
except Product.DoesNotExist:
    product = Product.objects.create(
        name='Test Product',
        description='Test product description',
        price=99.99,
        category=category,
        stock=10,
        available=True
    )
    print(f"Created test product: {product}")

# Try to add an image to the product
test_image_path = os.path.join(settings.MEDIA_ROOT, 'product_images', 'test_image.jpg')
if os.path.exists(test_image_path):
    print(f"Using existing test image: {test_image_path}")
    with open(test_image_path, 'rb') as img:
        product.image.save('test_image.jpg', ImageFile(img), save=True)
    print(f"Updated product with image: {product.image.url if product.image else 'No image'}")
else:
    print(f"Test image not found at path: {test_image_path}")
    print("Please create a test image in the media/product_images directory")

# Test creating product history
try:
    # Debug product image field
    print(f"Product image type: {type(product.image)}")
    print(f"Product image name: {product.image.name if product.image else None}")
    
    # Try manual serialization
    print("Testing manual JSON serialization...")
    manual_data = {
        'name': product.name,
        'description': product.description,
        'price': str(product.price),
        'image_path': product.image.name if product.image else None,
    }
    
    # Try to JSON serialize manually
    print("Converting to JSON string...")
    json_str = json.dumps(manual_data)
    print(f"Manual JSON serialization successful: {json_str[:50]}...")
    
    # Now try the create_from_product method
    print("Now testing ProductHistory.create_from_product()...")
    history = ProductHistory.create_from_product(product)
    print(f"Created history record: {history}")
    print(f"History data sample: {json.dumps(history.product_data)[:50]}...")
except Exception as e:
    print(f"Error creating history: {e}")
    import traceback
    traceback.print_exc()

print("Test completed.")
