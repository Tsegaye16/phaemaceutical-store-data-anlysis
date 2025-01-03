import zipfile
import os

def unzip_file(zip_path, extract_to):
    """
    Unzips a .zip file to the specified directory.
    
    Parameters:
    - zip_path: Path to the .zip file.
    - extract_to: Directory where the contents will be extracted.
    """
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
            print(f"Successfully extracted to {extract_to}")
    except zipfile.BadZipFile:
        print("The file is not a valid ZIP archive.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
zip_file_path = "data/rossmann-store-sales.zip"  # Replace with the path to your .zip file
output_directory = "data/"    # Replace with the desired extraction directory

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

unzip_file(zip_file_path, output_directory)
