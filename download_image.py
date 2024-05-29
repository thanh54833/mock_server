import io
import json
import os
import subprocess
from urllib.parse import urlparse

import requests
from PIL import Image


def find_image_urls(data):
    image_urls = []
    for route in data['routes']:
        for response in route['responses']:
            try:
                body = json.loads(response['body'])
                if 'data' in body and isinstance(body['data'], (list, dict)):
                    data_ = body['data']
                    if isinstance(data_, dict):
                        for key, value in data_.items():
                            if isinstance(value, str) and ('.jpg' in value or '.png' in value or '.gif' in value):
                                image_urls.append(value)
                    else:
                        for item in data_:
                            for key, value in item.items():
                                if isinstance(value, str) and ('.jpg' in value or '.png' in value or '.gif' in value):
                                    image_urls.append(value)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from response body: {e}")
    return image_urls


with open('mockoon/concung.json', 'r') as f:
    data = json.load(f)

image_urls = find_image_urls(data)
filter_urls = [url for url in image_urls if ('packages/assets' not in url) and ('<img src=' not in url)]

# Define the directory for the output AVIF images
avif_dir = 'images/avif/'

# Create the output directory if it doesn't exist
os.makedirs(avif_dir, exist_ok=True)


def convert_to_avif(url, avif_dir):
    # Define the directory for the temporary PNG file
    temp_dir = 'images/input'
    os.makedirs(temp_dir, exist_ok=True)

    headers = {
        'Cookie': 'Srv=cc205|ZlYHP|ZlYFd',
        'cc_mock_server': 'GET',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    }

    # Download the image into a PIL.Image object
    response = requests.get(url, headers=headers)
    try:
        image = Image.open(io.BytesIO(response.content))

        # Extract the base name from the URL
        base_name = os.path.splitext(os.path.basename(urlparse(url).path))[0]

        # Save the image as a temporary PNG file
        temp_png = os.path.join(temp_dir, f'{base_name}.png')
        image.save(temp_png)

        # Construct the AVIF filename
        avif_path = os.path.join(avif_dir, f'{base_name}.avif')

        # Convert the temporary PNG file to AVIF format
        subprocess.run(['avifenc', temp_png, avif_path])

        # Delete the temporary PNG file
        os.remove(temp_png)
    except Exception as e:
        print("----------")
        print(f"url -> {url}")
        print(f"Error downloading image: {e}")
        print("----------")


print(f"Total images before convert : {len(filter_urls)}")
for url in filter_urls:
    convert_to_avif(url, avif_dir)

# Define the directory
avif_dir = 'images/avif/'

# List the files in the directory
files = os.listdir(avif_dir)

# Print the total number of files
print(f"Total files in {avif_dir}: {len(files)}")
