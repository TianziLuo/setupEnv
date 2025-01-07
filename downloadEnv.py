import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from downloadRources import downloadList

# 配置下载目录
download_dir = os.path.join(os.getcwd(), "downloads")
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# 配置 Edge Options
edge_options = Options()
prefs = {
    "download.default_directory": download_dir,
    "profile.default_content_settings.popups": 0,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True,
}
edge_options.add_experimental_option("prefs", prefs)

# 设置 WebDriver（Edge 浏览器）
driver = webdriver.Edge(options=edge_options)

try:
    attempts = 0
    max_attempts = 5

    while attempts < max_attempts:
        try:
            # 打开网页
            driver.get("https://drive.usercontent.google.com/download?id=1UjVxHYH6ZXnFRYP6TQ3uqmvDpAhL48mw&export=download&authuser=0")
            break  # 如果成功打开网页，退出循环
        except Exception as e:
            print(f"尝试第 {attempts + 1} 次打开网页失败: {e}")
            attempts += 1
            if attempts >= max_attempts:
                print("已达到最大重试次数，操作终止。")
                raise

    # 等待并点击下载按钮
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.ID, "uc-download-link")))
    element.click()
    print("点击下载按钮，等待文件下载...")

    # 检测下载目录
    timeout = 30
    start_time = time.time()
    downloaded = False

    while time.time() - start_time < timeout:
        files = os.listdir(download_dir)
        if files:
            for file in files:
                if file.endswith(".tmp"):
                    print(f"文件 {file} 正在下载中...")
                    time.sleep(20)
                else:
                    downloaded_file = os.path.join(download_dir, file)
                    downloaded = True
                    break
        if downloaded:
            break

    if downloaded:
        print(f"文件下载成功: {downloaded_file}")
    else:
        print("文件下载超时或失败！")

except Exception as e:
    print(f"操作失败: {e}")
