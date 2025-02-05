import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options

def download():
    # Configure download directory
    file_name = "downloadenv"
    downloads_path = os.path.expanduser("~/Downloads")
    download_dir = os.path.join(downloads_path, file_name)

    # Ensure the download directory exists
    os.makedirs(download_dir, exist_ok=True)

    # Configure Edge Options
    edge_options = Options()
    prefs = {
        "download.default_directory": download_dir,
        "profile.default_content_settings.popups": 0,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
    }
    edge_options.add_experimental_option("prefs", prefs)

    # Set up WebDriver (Edge browser)
    driver = webdriver.Edge(options=edge_options)

    try:
        # Open the webpage
        driver.get("https://drive.google.com/uc?export=download&id=16vHcpsRPKuOv2a9GFXxQU6j4kR02g6EJ")

        # Wait for the download button to appear
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'export=download')]")))
        element.click()

        # Monitor the download folder
        timeout = 300  # Timeout period (seconds)
        start_time = time.time()
        downloaded_file = None

        while time.time() - start_time < timeout:
            files = os.listdir(download_dir)
            for file in files:
                file_path = os.path.join(download_dir, file)
                if file.endswith(".crdownload") or file.endswith(".tmp"):  # Still downloading
                    print(f"File {file} is still downloading...")
                else:
                    # File is fully downloaded
                    downloaded_file = file_path
                    break

            if downloaded_file:
                break
            time.sleep(50)  # Check every 5 seconds

        if downloaded_file:
            print(f"File downloaded successfully: {downloaded_file}")
        else:
            print("File download timed out or failed!")

    except Exception as e:
        print(f"Operation failed: {e}")
    finally:
        driver.quit()  # Ensure the driver is closed

if __name__ == "__main__":
    download()
