import io
import json
import os
import subprocess
from urllib.parse import urlparse

import requests
from PIL import Image

# Define the directory for the output AVIF images
avif_dir = 'images/avif/'
list_url_convert_error = []


def replace_value(data, old_value, new_value):
    if isinstance(data, dict):
        return {k: replace_value(v, old_value, new_value) for k, v in data.items()}
    elif isinstance(data, list):
        return [replace_value(i, old_value, new_value) for i in data]
    elif isinstance(data, str):
        return data.replace(old_value, new_value)
    else:
        return data


def convert_to_avif(url, avif_dir):
    try:
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
        return f'http://10.10.11.159:8002/images/{base_name}.avif'
    except Exception as e:
        list_url_convert_error.append(url)
        print("----------")
        print(f"url -> {url}")
        print(f"Error downloading image: {e}")
        print("----------")
    return ""


def find_image_urls(data_source):
    image_urls = []

    data_image_change_avif = data_source
    for route in data_source['routes']:
        for response in route['responses']:
            try:
                body = json.loads(response['body'])
                if 'data' in body and isinstance(body['data'], (list, dict)):
                    data_ = body['data']
                    if isinstance(data_, dict):
                        for key, value in data_.items():
                            if isinstance(value, str) and ('.jpg' in value or '.png' in value or '.gif' in value):
                                if ('packages/assets' not in value) and ('<img src=' not in value):
                                    image_urls.append(value)
                                    url_local = convert_to_avif(value, avif_dir)

                                    if url_local:
                                        data_[key] = url_local
                                        data_image_change_avif = replace_value(data_image_change_avif, value, url_local)
                                        # print(data_new)
                                        # print(data_[key])
                    else:
                        for i in range(len(data_)):
                            for key, value in data_[i].items():
                                if isinstance(value, str) and ('.jpg' in value or '.png' in value or '.gif' in value):
                                    if ('packages/assets' not in value) and ('<img src=' not in value):
                                        image_urls.append(value)
                                        url_local = convert_to_avif(value, avif_dir)
                                        print(value)
                                        if url_local:
                                            data_[i][key] = url_local
                                            data_image_change_avif = replace_value(data_image_change_avif, value, url_local)
                                            # print(data_new)
                                            # print(data_[i][key])

            except json.JSONDecodeError as e:
                list_url_convert_error.append("Error decoding JSON from response body:")
                print(f"Error decoding JSON from response body: {e}")

    return data_image_change_avif, image_urls


with open('mockoon/concung.json', 'r') as f:
    data = json.load(f)

data, image_urls = find_image_urls(data)

with open('mockoon/concung_convert_avif.json', 'w') as f:
    json.dump(data, f, indent=4)

# Create the output directory if it doesn't exist
os.makedirs(avif_dir, exist_ok=True)

print(f"Total images before convert : {len(image_urls)}")
print(f"Total images convert error : {len(list_url_convert_error)}")
# List the files in the directory
files = os.listdir(avif_dir)
# Print the total number of files
print(f"Total files in {avif_dir}: {len(files)}")
