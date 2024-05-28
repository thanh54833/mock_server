import os
import json
import requests

# Define the directory for the input images
input_dir = 'images/input'

# Create the input directory if it doesn't exist
os.makedirs(input_dir, exist_ok=True)

# Open the JSON file
with open('mockoon/concung.json', 'r') as f:
    data = json.load(f)

# Iterate over the JSON data to find the image URLs
for item in data['routes']:
    for response in item['responses']:
        # Check if the 'body' key exists and is a string
        if 'body' in response and isinstance(response['body'], str):
            try:
                # Try to parse the 'body' string as JSON
                body = json.loads(response['body'])
                # Check if the 'mobile_image' key exists in the 'body' dictionary

                for value in body.values():
                    # Check if the value is a string and looks like a URL

                    if isinstance(value, str) and (value.startswith('http://') or value.startswith('https://')):
                        image_url = value
                        print(image_url)
                        # Send a GET request to the image URL
                        response = requests.get(image_url)
                        # Check if the request was successful
                        if response.status_code == 200:
                            # Extract the image filename from the URL
                            filename = os.path.basename(image_url)
                            # Open a new file in binary write mode
                            with open(os.path.join(input_dir, filename), 'wb') as img_file:
                                # Write the content of the response to the file
                                img_file.write(response.content)

            except json.JSONDecodeError:
                # The 'body' string is not valid JSON, skip it
                pass