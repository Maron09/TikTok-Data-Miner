from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchAttributeException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import time
import requests
import re
import xlsxwriter as xs
import pandas as pd

# initialize webdriver
chrome_options = Options()
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.headless = False
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
prefs= {"prfile.managed_default_content_settings.images" : 2}
chrome_options.add_experimental_option("prefs", prefs)
ua = UserAgent(use_external_data=False)
UserAgent = ua.random
chrome_options.add_argument(f"user-agent={UserAgent}")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

driver.get("https://www.tiktok.com/@Username")
# scroll to the end of the page
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height


soup = bs(driver.page_source, 'html.parser')
videos = soup.find_all('div', {'class': 'tiktok-yz6ijl-DivWrapper'})
time.sleep(3)
print(len(videos))
data=[]
for video in videos:
    url = video.a['href']
    views = video.find('strong', {'data-e2e':'video-views'}).text
    description = video.find('img', {'class':'tiktok-1itcwxg-ImgPoster e1yey0rl1'})['alt']
    tags = re.findall('#\w*', description)

    driver.get(url)
    soap = bs(driver.page_source, 'html.parser')
    time.sleep(3)
    try:
        likes = soap.find('strong', {'data-e2e':'like-count'}).text
        comments = soap.find('strong', {'data-e2e':'comment-count'}).text
        shares = soap.find('strong', {'data-e2e': 'share-count'}).text
        music_nc = soap.find('h4', {'data-e2e':'browse-music'}).find('a')['href']
        music = f"https://tiktok.com{music_nc}"
        date = soap.find('span', {'class':'tiktok-sfaea2-SpanOtherInfos e17fzhrb2'}).find_all('span')[-1].text

    except Exception:
        pass

    

    print(likes)
    print(comments)
    print(shares)
    print(f"https://tiktok.com{music}")
    print(url)
    
    
    # data.append(date)
    data.append([likes, comments, shares, music])
    data.append([url])

workbook = xs.Workbook('tiktok_data.xlsx')
worksheet = workbook.add_worksheet()
for row_num, row_data in enumerate(data):
    for col_num, col_data in enumerate(row_data):
        worksheet.write(row_num, col_num, col_data)
workbook.close()

# close webdriver
