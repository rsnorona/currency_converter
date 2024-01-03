from selenium import webdriver
import time
from bs4 import BeautifulSoup
import json
import os
import dotenv

dotenv.load_dotenv()


## TESTING
def automated_test(api_url, data):
    chrome_driver_path = os.getenv("CHROME_DRIVER_PATH")
    chrome_options = webdriver.ChromeOptions()
    if os.getenv("OPERATIVE_SYSTEM") == "Windows":
        chrome_options.binary_location = (
            "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        )
    if os.getenv("OPERATIVE_SYSTEM") == "macOS":
        chrome_options.binary_location = (
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        )
    if os.getenv("OPERATIVE_SYSTEM") == "Linux":
        chrome_options.binary_location = "/usr/bin/google-chrome"

    chrome_options.add_argument(f"webdriver.chrome.driver={chrome_driver_path}")
    driver = webdriver.Chrome(options=chrome_options)

    if api_url:
        driver.get(api_url)
        with open("api/test/submitForm.js", "r") as file:
            javascript_code = file.read()
        driver.execute_script(javascript_code, api_url, data)
        time.sleep(2)
        driver.implicitly_wait(5)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        pre_tag = soup.find("pre")
        if pre_tag:
            json_string = pre_tag.text
            parsed_json = json.loads(json_string)
            response = json.dumps(parsed_json, indent=2)
            print(response)
    driver.quit()
