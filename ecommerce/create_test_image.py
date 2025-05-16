"""
Create a test image for product testing
"""
import os
from PIL import Image

# Ensure the directory exists
media_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'product_images')
os.makedirs(media_dir, exist_ok=True)

# Create a simple red square image
img_path = os.path.join(media_dir, 'test_image.jpg')
img = Image.new('RGB', (100, 100), color = 'red')
img.save(img_path)

print(f"Test image created at: {img_path}")
