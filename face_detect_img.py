from os import listdir
from os.path import isfile, join
import subprocess
import os
from tqdm import tqdm
import errno
from moviepy.video.io.VideoFileClip import VideoFileClip
import shutil
import numpy as np
import cv2
import csv
import re


def extract_img(title, video_path, img_dir):
    subprocess.call(['ffmpeg', '-i', '%s' %(video_path), '-r', '10', '-s', '640x360', '%s/%s.png' %(img_dir, title+'%06d')])
    

def face_detection(dir, i ,img):
    face_cascade = cv2.CascadeClassifier('/Users/dai/desktop/ml_py/cv/training_data/haarcascade_frontface.xml') #driver 위치
    image = cv2.imread(img)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    area = 0
    i = i.replace('.png','')
    f = re.findall('\d+', i)
    frame = f[len(f)-1]
    for (x, y, w, h) in faces:
        area = 0
        if faces.shape[0] == 1:            
            if w*h > 7000 and w*h < 30000:
                area = w*h
    return (frame, area)


def make_csv(v, video_path):
    dir = '/Users/dai/desktop/sample/video'
    img_dir = dir+'/temp'
    try:
        if not (os.path.isdir(img_dir)):
            os.makedirs(os.path.join(img_dir))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print('폴더 만들기 실패')
            raise
    title = v.replace('.mp4', '')    
    extract_img(title, video_path, img_dir)
    imgs = [f for f in listdir(img_dir) if isfile(join(img_dir, f))]
    s_imgs = sorted(imgs)
    with open(dir+'/'+title+'.csv', mode='w',encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        # writer.writerow(['time(sec)','frame', 'area'])
        for i in tqdm(s_imgs):
            img = img_dir + '/' + i
            res = face_detection(dir, i , img)
            try:
                if res[1] != 0:
                    ret = writer.writerow([int(res[0])*0.1,res[0], res[1]])
            except:
                print('csv file 작성 실패')
                raise
    shutil.rmtree(img_dir, ignore_errors=True)    


if __name__ == '__main__':
    keyword = '1분 자기소개' #폴더명
    dir = '/Volumes/Transcend/data/video/'+keyword+'/'
    video = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    # video = ['금호아시아나 그룹 면접 완전분석(아시아나 항공 일반직면접)_공채를 잡아라 46회.mp4']

    for v in video:
        if '._' in v:
            v = v.replace('._', '')
        video_path = dir+v
        make_csv(v, video_path)

