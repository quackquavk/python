import os
from PIL import Image
import pytesseract

# Path to the folder containing the images
folder_path = "/Users/mac/Desktop/python/whatsapp"

# Output file to save the extracted text
output_file = "/Users/mac/Desktop/python/questions.txt"

# Ensure the path is correct for your system
if not os.path.exists(folder_path):
    print("Folder not found!")
    exit()

# Create or clear the output file
with open(output_file, "w") as f:
    f.write("")  # Clear the file contents if it exists

# Iterate through all files in the folder
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    
    # Check if the file is an image (extensions can vary)
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif')):
        try:
            # Open the image
            img = Image.open(file_path)

            # Extract text
            text = pytesseract.image_to_string(img)

            # Append the extracted text to the output file
            with open(output_file, "a") as f:
                f.write(f"Text from {filename}:\n{text}\n{'-' * 80}\n")
            
            print(f"Extracted text from {filename} and saved to {output_file}")

        except Exception as e:
            print(f"Could not process {filename}: {e}")
