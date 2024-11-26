from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
from glob import glob
import cloudinary
from cloudinary import uploader
import json
import platform


load_dotenv()
git_user_name = os.environ["GIT_USER"]
cloudinary.config(
    cloud_name=os.environ["CLOUD_NAME"],
    api_key=os.environ["API_KEY"],
    api_secret=os.environ["API_SECRET"],
)
print(git_user_name)
if os.name == "nt":  # Windows
    geckodriver_path = "C:\\WebDriver\\geckodriver.exe"
elif os.name == "posix":  # Linux/Mac
    geckodriver_path = "/usr/local/bin/geckodriver"
else:
    raise Exception("Unsupported operating system")

service = Service(executable_path=geckodriver_path)
options = webdriver.FirefoxOptions()
options.add_argument("--width=1920")
options.add_argument("--height=1080")


# Initialize WebDriver
driver = webdriver.Firefox(service=service, options=options)

imgName = "contributions"
folder = "portfolio_images/git"

try:
    driver.get("https://github-contributions.vercel.app/")
    WebDriverWait(driver, timeout=10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )

    input_element = driver.find_element(By.ID, "username")
    input_element.send_keys(git_user_name)
    button = driver.find_element(By.TAG_NAME, "button")
    button.click()

    WebDriverWait(driver, timeout=10).until(
        EC.presence_of_element_located((By.TAG_NAME, "canvas"))
    )

    driver.find_element(By.XPATH, "//input[@value='githubDark']").click()

    img = driver.find_element(By.TAG_NAME, "canvas")
    # Clear existing screenshots
    for file in glob("*.png"):
        os.remove(file)

    if img.screenshot(imgName + ".png"):
        try:
            # Check and delete existing Cloudinary image
            response = uploader.destroy(public_id=f"{imgName}_deep")
            deletion_result = json.loads(json.dumps(response))
            print(deletion_result)

            if deletion_result.get("result") in ["ok", "not found"]:
                # Upload new screenshot
                uploaded = uploader.upload(
                    imgName + ".png",
                    public_id=f"{imgName}_deep",
                )
                print(uploaded)
        except Exception as e:
            print(f"Cloudinary Error: {e}")
    else:
        print("Screenshot failed.")
except Exception as e:
    print(f"Error: {e}")
# finally:
#     driver.quit()
