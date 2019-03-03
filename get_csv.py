from bs4 import BeautifulSoup
import sys
import io
import os
import urllib.parse as rep
import urllib.request as req
import requests
import pytube
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
import errno
import time
from tqdm import tqdm
import random

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

def get_keyword(keyword):
    base = "https://www.youtube.com/results?search_query="
    quote = rep.quote_plus(keyword)
    return base+quote

def get_page(url):
    driver = webdriver.Chrome('/Users/dai/Desktop/ml_py/dlyt/chromedriver')
    driver.get(url)
    html = driver.page_source
    href = get_link(html)
    driver.close()
    return href


def get_link(source):
    soup = BeautifulSoup(source, 'lxml')
    titles = soup.find_all('h3')
    title = []
    base = "https://www.youtube.com"
    for title in titles:
        if hasattr(title.a, 'href'):
            url = base+title.a['href']
            href.append(url)
    return href

    
    
def make_csv(csv_path, href):
    try:
        if not (os.path.isfile(csv_path)):
            with open(csv_path, mode='w',encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                for row in href:
                    writer.writerow([row])
        else:
            with open(csv_path, mode='r') as file:
                reader = csv.reader(file)
                temp_href = list(reader)
                for row in href:
                    if row in temp_href:
                        href.remove([row])
                tot = temp_href+href
            with open(csv_path, mode='w',encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                for row in tot:
                    writer.writerow([row])
        print("csv file 만들기 완료!")
    except OSError as e:
        if e.errno != errno.EEXIST:
            print('csv file 만들기 실패')
            raise
    return href

#폴더 명 -> 파일 명 -> 파일명 유튜브에 검색 -> 영상 링크 받아서 -> csv file에 쓰기
# /Users/dai/Desktop/sample/get_csv.py

video_dir = '/Volumes/Transcend/data/video/'
csv_dir = '/Volumes/Transcend/data/keyword_csv/'
folders =[]
for f in folders:
    href = []
    dir = video_dir+f
    csv_path = csv_dir + f + '.csv'
    video = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    for v in video:
        # print(v)
        link = get_keyword(v)
        page = get_page(link)
        href.append(page[0])
    make_csv(csv_path, href)
