import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options

def download():
    isdownload = False
    # Configure download directory
    download_dir = os.path.join(os.getcwd(), "downloads")
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # Configure Edge Options
    edge_options = Options()
    prefs = {
        "download.default_directory": download_dir,  # Set the default download directory
        "profile.default_content_settings.popups": 0,  # Disable popups
        "download.prompt_for_download": False,  # Disable the download prompt
        "download.directory_upgrade": True,  # Enable directory upgrades
        "safebrowsing.enabled": True,  # Enable safe browsing
    }
    edge_options.add_experimental_option("prefs", prefs)

    # Set up WebDriver (Edge browser)
    driver = webdriver.Edge(options=edge_options)

    try:
        # Open the webpage
        driver.get("https://drive.usercontent.google.com/download?id=16vHcpsRPKuOv2a9GFXxQU6j4kR02g6EJ&export=download&authuser=0")

        # Wait for and click the download button
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.element_to_be_clickable((By.ID, "uc-download-link")))
        element.click()
        print("Clicked the download button, waiting for file download...")

        # Check the download directory
        timeout = 30  # Timeout period (seconds)
        start_time = time.time()
        downloaded = False

        # Loop to check if the download has completed
        while time.time() - start_time < timeout:
            files = os.listdir(download_dir)
            if files:
                for file in files:
                    if file.endswith(".tmp"):  # Check if the file is still downloading
                        print(f"File {file} is downloading...")
                        time.sleep(200)
                    else:
                        # If the file is fully downloaded, break the loop
                        downloaded_file = os.path.join(download_dir, file)
                        downloaded = True
                        break
            if downloaded:
                break

        if downloaded:
            isdownload = True
            print(f"File downloaded successfully: {downloaded_file}")
            return isdownload
        else:
            print("File download timed out or failed!")

    except Exception as e:
        print(f"Operation failed: {e}")

if __name__ == "__main__":
    download()