import os
import gdown

def download():
    download_dir = os.path.join(os.getcwd(), "downloads")
    os.makedirs(download_dir, exist_ok=True)

    file_url = "https://drive.google.com/uc?id=16vHcpsRPKuOv2a9GFXxQU6j4kR02g6EJ"
    output_path = os.path.join(download_dir, "downloaded_file.zip")  # Ensure correct extension
    
    try:
        gdown.download(file_url, output_path, fuzzy=True)  # Remove 'quiet' and use 'fuzzy=True'
        if os.path.exists(output_path):
            print(f"File downloaded successfully: {output_path}")
            return True
    except Exception as e:
        print(f"Download failed: {e}")

    return False

if __name__ == "__main__":
    download()
