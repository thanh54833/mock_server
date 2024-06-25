from io import BytesIO

import requests
from PIL import Image

# The original image URL
url = "https://storage.cloud.google.com/ccdataset/sua-nan-a2-infinipro-800g-so-3-2-6-tuoi.png?authuser=2"

# Get the image data
response = requests.get(url)
img = Image.open(BytesIO(response.content))

# Resize the image
img.thumbnail((200, 200))

# Save the image in webp format
img.save("output_image.webp", "WEBP")
