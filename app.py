from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from dotenv import load_dotenv
import os
from glob import glob
import cloudinary
from cloudinary import uploader
import json


load_dotenv()
cloudinary.config(
    cloud_name=os.environ['CLOUD_NAME'],
    api_key=os.environ['API_KEY'],
    api_secret=os.environ['API_SECRET']
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

imgName = "contributions"
folder ='portfolio_images/git/'


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
pngFiles = glob("*.png")
for file in pngFiles:
    if file:
        os.remove(file)
isSaved = img.screenshot(imgName+'.png')
if isSaved:
    try:
        response = uploader.destroy(public_id=folder+imgName)
        isDeleted = str(response).strip("'<>() ").replace('\'', '\"')
        # print(json.loads(isDeleted)["result"])
        if json.loads(isDeleted)['result']=='ok' or json.loads(isDeleted)['result']=='not found':
            uploaded = uploader.upload(imgName,public_id=folder+imgName,folder=folder)
            print(uploaded)
    except Exception as e:
        print(e)
else:
    print("something went wrong.")

# print()
