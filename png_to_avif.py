import os
import subprocess

# Define the directory containing the PNG images
png_dir = 'images/png'

# Define the directory for the output AVIF images
avif_dir = 'images/avif'

# Create the output directory if it doesn't exist
os.makedirs(avif_dir, exist_ok=True)

# Get a list of all PNG files in the directory
png_files = [f for f in os.listdir(png_dir) if f.endswith('.png')]

# Loop over the list of PNG files
for png_file in png_files:
    # Construct the AVIF filename
    base_name = os.path.splitext(png_file)[0]
    avif_file = base_name + '.avif'

    # Construct the full paths to the PNG and AVIF files
    input_png = os.path.join(png_dir, png_file)
    output_avif = os.path.join(avif_dir, avif_file)

    # Call avifenc to convert the PNG file to AVIF format
    subprocess.run(['avifenc', input_png, output_avif])

    # Delete the PNG file
    os.remove(input_png)
