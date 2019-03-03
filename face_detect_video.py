import numpy as np
import cv2
import os
import time
import sys
from tqdm import tqdm
import time
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import *

def faceDetect(title):
    font = cv2.FONT_HERSHEY_SIMPLEX

    face_cascade = cv2.CascadeClassifier('/Users/dai/desktop/ml_py/cv/training_data/haarcascade_frontface.xml')
    info = ''

    keyword = '1분 자기소개'
    dir = '/Volumes/Transcend/data/video/'+keyword+'/'

    path = dir + title
    try:
        cap = cv2.VideoCapture(path)

    except:
        print('False)camera loading')
        return

    location = []

    start_time = time.time()

        
    ret, last_frame = cap.read()
    ret, frame = cap.read()

    i = 0
    while True:
        
        last_frame=frame

        ret, frame = cap.read()

        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        cv2.putText(frame, info, (5, 15), font, 0.5, (255, 0, 255), 1)


        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(frame, 'Face', (x-5, y-5), font, 0.5, (255, 255, 0), 2)

            if w*h > 7000 and w*h < 25000:
                diff = cv2.absdiff(last_frame, frame)
                if np.mean(diff)<15:
    
                    ts = cap.get(cv2.CAP_PROP_POS_MSEC)/1000
                    location.append([ts, np.mean(diff)])

        cv2.imshow('frame', frame)
        k = cv2.waitKey(1) & 0xFF

        if k == ord('e'):
            break
        # if k == ord('k'):
        #     continue



    clip = []
    tmp = []
    for i in range(len(location)-1):
        if location[i+1][0]-location[i][0]<=1:
            tmp.append(location[i][0])
        else:
            if len(tmp)!=0 :
                tmp.append(location[i][0])
                clip.append(tmp)
            tmp=[]


    if len(location)>=2 and location[len(location)-1][0]-location[len(location)-2][0] <= 0.8:
        tmp.append(location[len(location)-1][0])
        clip.append(tmp) 

    for c in clip:
        if (c[len(c)-1]-c[0] >= 15):
            output = '/Volumes/Transcend/data/clip/'+str(i)+title                
            i+=1
            ffmpeg_extract_subclip(path, c[0], c[len(c)-1], targetname=output)


    cap.release()
    cv2.destroyAllWindows()

def main():
    keyword = '1분 자기소개'
    dir = '/Volumes/Transcend/data/video/'+keyword+'/'
    video = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]


    for i in video:
        if '._' in i:
            i = i.replace('._','')
        faceDetect(i)



main()