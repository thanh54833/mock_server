import os
import subprocess

from PIL import Image

# Define the directory containing the PNG images
input_dir = 'images/input'

# Define the directory for the output WebP images
webp_dir = 'images/webp'

# Create the output directory if it doesn't exist
os.makedirs(webp_dir, exist_ok=True)

# Get a list of all image files in the directory
image_files = [f for f in os.listdir(input_dir) if f.endswith(tuple(Image.registered_extensions()))]

# Loop over the list of image files
for image_file in image_files:
    # Construct the WebP filename
    base_name = os.path.splitext(image_file)[0]
    webp_file = base_name + '.webp'

    # Construct the full paths to the image and WebP files
    input_image = os.path.join(input_dir, image_file)
    output_webp = os.path.join(webp_dir, webp_file)

    # Call cwebp to convert the image file to WebP format
    subprocess.run(['cwebp', input_image, '-o', output_webp])

    # Delete the original image file
    os.remove(input_image)
