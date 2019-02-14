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

#키워드 넣고 나중에 계속 반복해서 돌릴려면 키워드 받는 함수 만들어서
#나중에 필요한 키워드 다 때려넣은 리스트 반복문 돌리는게 좋을거같당

def get_keyword(keyword):
    base = "https://www.youtube.com/results?search_query=%"
    quote = rep.quote_plus(keyword)
    hd = "&sp=EgIgAQ%253D%253D"
    return base+quote+hd

#link download
# href 만듬 받아온 url(html)필요

def get_link(source):
    soup = BeautifulSoup(source, 'lxml')
    titles = soup.find_all('h3')
    href = []
    title = []
    base = "https://www.youtube.com"
    for title in titles:
        if hasattr(title.a, 'href'):
            href.append(base+title.a['href'])
    return href

def auto_scroll(url):
    driver = webdriver.Chrome('/Users/dai/Desktop/ml_py/dlyt/chromedriver')
    driver.get(url)
    time.sleep(1)
    sleep_time = 0.5
    while True:
        last_height = driver.execute_script("return document.documentElement.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(sleep_time)
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(sleep_time)
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        time.sleep(sleep_time)
        if new_height == last_height:
            break
        else:
            last_height = new_height
            continue
    print("complete scroll down!")
    html = driver.page_source
    href = get_link(html)
    driver.close()
    return href

def make_csv(csv_path, href):
    # temp_href = []
    try:
        if not (os.path.isfile(csv_path)):
            #if there is not csv file
            with open(csv_path, mode='w',encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                for row in href:
                    writer.writerow([row])
        # else:
        #     #if there is csv file
        #     with open(csv_path, mode='r') as file:
        #         reader = csv.reader(file)
        #         temp_href = list(reader)
        #         for row in href:
        #             # if row not in temp_href:
        #             if row in temp_href:
        #                 href.remove([row])
        #     with open(csv_path, mode='w',encoding='utf-8', newline='') as file:
        #         writer = csv.writer(file)
        #         for row in href:
        #             writer.writerow([row])
        print("csv file 만들기 완료!")
    except OSError as e:
        if e.errno != errno.EEXIST:
            print('csv file 만들기 실패')
            raise
    return href

def download_video(keyword, href):
    down_dir = "/Volumes/Transcend/data/video/"+keyword+"/"
    try:
        if not (os.path.isdir(down_dir)):
            os.makedirs(os.path.join(down_dir))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print('폴더 만들기 실패')
            raise
    caption_dir = '/Volumes/Transcend/data/captions/'+keyword+'/'
    try:
        if not (os.path.isdir(caption_dir)):
            os.makedirs(os.path.join(caption_dir))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print('폴더 만들기 실패')
            raise
    # print("동영상 다운로드 시작")
    for i in tqdm(href):
        try:
            yt = pytube.YouTube(i)
        except:
            continue
        caption = yt.captions.get_by_language_code('ko')
        title = yt.title

        #현재 상태태탵ㅌ
        current_caption = [f for f in os.listdir(caption_dir) if os.path.isfile(os.path.join(caption_dir, f))]

        if not caption:
            continue
        else:
            if caption_dir+title+'.srt' in current_caption:
                continue
            else:
                if '/' in title:
                    title = title.replace('/', '')
                subtitle = caption.generate_srt_captions()
                with open(caption_dir+title+'.srt', 'w', encoding='utf-8', newline='') as f:
                    f.write(subtitle)
        #현재 상태

        current_video = [f for f in os.listdir(down_dir) if os.path.isfile(os.path.join(down_dir, f))]

        for e in yt.streams.filter(progressive=True, file_extension='mp4').all():
            try:
                e.download(output_path = down_dir, skip_existing=True)
            except:
                continue

        time.sleep(random.randint(1,3))




def main():
    keywords = ['1분 자기소개','1분 자기소개 예시', '화장법', '메이크업', '큐앤에이 답변', '스피치']
    keywordtest = ['인터뷰','자기소개']
    #이미한거 : '아나운서 발성'
    # for keyword in keywords:
    for keyword in keywordtest:
        csv_path = '/Volumes/Transcend/data/keyword_csv/'+keyword+'.csv'
        print('#####'+keyword+'다운로드 시작'+'#####')
        url = get_keyword(keyword)
        if not (os.path.isfile(csv_path)):
            href = auto_scroll(url)
        else:
            href = []
            with open(csv_path, mode='r') as file:
                reader = csv.reader(file)
                tmp = list(reader)
            for i in tmp:
                href.append(''.join(i))
            # print(href)
        download_list = make_csv(csv_path, href)
        
        download_video(keyword, download_list)
        print('#####'+keyword+'다운로드 끝'+'#####')


if __name__ == '__main__':
    main()
    print('video/srt')
    