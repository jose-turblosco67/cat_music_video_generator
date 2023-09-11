import time
import base64
from io import BytesIO
import re
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests
from PIL import Image

cwd = os.getcwd()
IMAGE_FOLDER = 'images'
os.makedirs(
    name=f'{cwd}/{IMAGE_FOLDER}',
    exist_ok=True
)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(
    service=service
)

SLEEP_TIME = 0.2
LONG_SLEEP = 0.5


def download_google_images(search_query: str, order: int) -> str:
    '''Download google images with this function\n
       Takes -> search_query, order\n
       Returns -> None
    '''
    url = 'https://images.google.com/'

    time.sleep(SLEEP_TIME)

    driver.get(
        url=url
    )

    if driver.find_elements(By.CLASS_NAME, 'sy4vM'):
        cookies = driver.find_element(
            by=By.CLASS_NAME,
            value='sy4vM'
        )
        cookies.click()

    time.sleep(SLEEP_TIME)

    box = driver.find_element(
        by=By.CLASS_NAME,
        value="gLFyf"
    )

    box.send_keys(search_query)
    time.sleep(LONG_SLEEP)
    box.send_keys(Keys.ENTER)
    time.sleep(SLEEP_TIME)

    img_result = driver.find_element(
        by=By.CLASS_NAME,
        value="Q4LuWd"
    )

    time.sleep(SLEEP_TIME)
    try:
        WebDriverWait(
            driver,
            15
        ).until(
            EC.element_to_be_clickable(
                img_result
            )
        )
        img_result.click()
        time.sleep(SLEEP_TIME)

        src = img_result.get_attribute('src')

        if 'https://' in src:
            image_name = search_query.replace('/', ' ')
            image_name = re.sub(pattern=" ", repl="_", string=image_name)
            file_path = f'{IMAGE_FOLDER}/_{image_name}.jpeg'
            try:
                result = requests.get(src, allow_redirects=True, timeout=10)
                open(file_path, 'wb').write(result.content)
                img = Image.open(file_path)
                img = img.convert('RGB')
                img.save(file_path, 'JPEG')
                print('Image saved from https.')
                return file_path
            except:
                print('Bad image.')
                try:
                    os.unlink(file_path)
                except:
                    pass
        else:
            img_data = src.split(',')
            image_name = search_query.replace('/', ' ')
            image_name = re.sub(pattern=" ", repl="_", string=image_name)
            file_path = f'{IMAGE_FOLDER}/{order}_{image_name}.jpeg'
            try:
                img = Image.open(BytesIO(base64.b64decode(img_data[1])))
                img = img.convert('RGB')
                img.save(file_path, 'JPEG')
                print('Image saved from Base64.')
                return file_path
            except:
                print('Bad image.')
        driver.quit()
    except ElementClickInterceptedException as e:
        print(e)
        print('Image is not clickable.')
        driver.quit()
