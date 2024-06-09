from datetime import datetime
import pandas as pd
import pprint
import requests
import os


# Function to download image from URL
def download_image(url, folder_path):
  try:
    # Send a GET request to the URL
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Raise an exception for bad requests

    # Extract the filename from the URL
    filename = os.path.join(folder_path, os.path.basename(url))

    # Save the image to the local file
    with open(filename, 'wb') as file:
      for chunk in response.iter_content(chunk_size=8192):
        file.write(chunk)

    print(f"Image downloaded and saved: {filename}")
  except Exception as e:
    print(f"Failed to download image from {url}: {e}")

from_header = [
  "Name",
  "Images",
]

def split_urls(input_string):
  # Split the input string by comma and remove spaces
  urls = [url.strip() for url in input_string.split(',')]
  return urls

def main():
  # Read the CSV file with the first line as header
  df = pd.read_csv('./products/products-export.csv', header=0)
  
  for index, row in df.iterrows():
    folder_name = row["Name"]
    images = split_urls(row["Images"])
    folder_path = f"images/{folder_name}"
    os.makedirs(folder_path, exist_ok=True)
    
    for image in images:
      download_image(image, folder_path)

if __name__ == "__main__":
  main()