import pandas as pd
import os
import re
import requests

# Load the Excel file
file_path = 'inlinks.xlsx'
df = pd.read_excel(file_path)

# Specify the download directory
download_directory = 'super-new-images'

# Ensure the download directory exists
if not os.path.exists(download_directory):
    os.makedirs(download_directory)

# Function to download image
def download_image(url, file_name):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        file_path = os.path.join(download_directory, file_name)
        with open(file_path, 'wb') as file:
            for chunk in response:
                file.write(chunk)
    else:
        print(f"Failed to download {url}")

# Function to clean URLs
def clean_url(url):
    return url.strip()

# Extract and process the image URLs
image_base_url = "https://rethinkyouroffice.co.uk"
processed_images = []
original_slugs = []

for idx, row in df.iterrows():
    image_paths = row['Images'].split(',')
    processed_paths = []
    slugs = []
    for image_path in image_paths:
        image_path = clean_url(image_path)
        if image_path.endswith('.jpg'):
            file_name = image_path.split('/')[-1]
        else:
            # Apply the renaming logic
            match = re.search(r'sImageUUID=(.*?)&w=', image_path)
            if match:
                uuid = match.group(1)
                file_name = f"{uuid}.jpg"
            else:
                file_name = image_path.split('/')[-1] + ".jpg"  # Fallback in case of unexpected format

        # Download the image
        full_url = f"{image_base_url}{image_path}"
        download_image(full_url, file_name)
        
        # Keep track of processed paths and original slugs
        processed_paths.append(file_name)
        slug = image_path.split('/')[-1]
        slug = re.sub(r'(_dspImageWrapper\.cfm\?sImageUUID=|&w=\d+)', '', slug)
        slugs.append(slug)
    
    processed_images.append(','.join(processed_paths))
    original_slugs.append(','.join(slugs))

# Add the new columns to the dataframe
df['Processed_Images'] = processed_images
df['Original_Slugs'] = original_slugs

# Save the updated dataframe to a new Excel file
output_file_path = 'processed_inlinks.xlsx'
df.to_excel(output_file_path, index=False)
