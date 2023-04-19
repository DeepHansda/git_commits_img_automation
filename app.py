from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from dotenv import load_dotenv
import os
from glob import glob
import cloudinary
load_dotenv()
cloudinary.config(
    cloud_name=os.environ['CLOUD_NAME'],
    api_key=os.environ['API_KEY'],
    api_secret=os.environ['API_SECRET'],
)
print(os.environ['CLOUD_NAME'])
service = Service(executable_path="C:\Program Files\WebDriver\bin")
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(
    service=service,
    options=options,
)
driver.set_window_size(1920, 1080)

driver.get("https://github-contributions.vercel.app/")
driver.implicitly_wait(5)
input = driver.find_element(By.ID, "username")
input.send_keys("deepHansda")
button = driver.find_element(By.TAG_NAME, "button")
button.click()

WebDriverWait(driver,
              timeout=5).until(lambda d: d.find_element(By.TAG_NAME, "canvas"))

driver.find_element(By.XPATH, "//input[@value='githubDark']").click()

img = driver.find_element(By.TAG_NAME, "canvas")
pngFile = glob("*.png")
if pngFile:
    os.remove("contributions.png")
isSaved = img.screenshot("contributions.png")
# if isSaved:

# else Exception as e:
#     print(e)

# print()
