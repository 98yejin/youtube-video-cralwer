import os
from itertools import groupby
from collections import namedtuple
import re
from datetime import datetime
import csv
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

def delete_hex(strlist):
    comp = re.compile('#?([A-F0-9]{6}|[A-F0-9]{3})')
    temp = []
    for sentence in strlist:
        if comp.search(sentence) != None:
            res = comp.search(sentence).group(0)
            while res in sentence:
                try:
                    if res in sentence:
                        sentence = sentence.replace(res, '')
                    if '<font color="">' in sentence:
                        sentence = sentence.replace('<font color="">', '')
                    if '</font>' in sentence:
                        sentence = sentence.replace('</font>', '')
                    res = comp.search(sentence).group(0)
                except:
                    temp.append(sentence)
                    break
        else:
            temp.append(sentence)
    return temp


def get_bucket(file):
    title = file.replace('.srt','')
    with open(file, 'r') as title:
        title = [list(g) for b,g in groupby(title, lambda x: bool(x.strip())) if b]
    Parse = namedtuple('Parse', 'index start end duration content')
    bucket = []
    i=0
    for sub in title:
        if len(sub) >= 3: 
            s = str(i)
            sub = [x.strip() for x in sub]
            temp = delete_hex(sub)
            number, start_end, *content = temp
            number = s
            start, end = start_end.split(' --> ')
            if ',' in start:
                start = start.replace(',','')
            if ',' in end:
                end = end.replace(',', '')
            tmp = datetime.strptime(end, '%H:%M:%S') - datetime.strptime(start, '%H:%M:%S')
            duration = tmp.seconds
            bucket.append(Parse(number, start ,end, duration, content))
            i+=1
    return bucket

def get_time(res):
    sec_srt = []
    for i, t in enumerate(res):
        tmp = res[i].start
        sec = sum(x * int(t) for x, t in zip([3600, 60, 1], tmp.split(":"))) 
        sec_srt.append(float(sec))
    return sec_srt

def get_csv(path):
    start = []
    area = []
    with open(path, mode='r') as file:
        reader = csv.reader(file)
        csv_list = list(reader)
    for i in range(len(csv_list)):
        start.append(float(csv_list[i][0]))
        area.append(float(csv_list[i][2]))
    return start

def closet_value(myList, myValue):
    return min(myList, key=lambda x:abs(x-myValue))

def cut_clip(csvl, srtl):
    clip = []
    tmp = []
    res = []
    tmp2 = []
    cut = []
    for i in range(len(csvl)-1):
        if csvl[i+1] - csvl[i] < 0.7:
            tmp.append(csvl[i])
        else:
            if len(tmp)!=0:
                tmp.append(csvl[i])
                clip.append(tmp)
            tmp=[]
    for i in range(len(clip)):
        last = len(clip[i])-1
        duration = clip[i][last]-clip[i][0]
        if duration>15:
            res.append(clip[i])
    for i, r in enumerate(res):
        for s in srtl:
            if len(tmp2)==0 and s > r[0]:
                tmp2.append(closet_value(r, s))
            if len(tmp2)==1 and s < r[len(r)-1]:
                tmp2.append(closet_value(r, s+15)) #ì‹œìž‘ì§€ì ì—ì„œ 15ì´ˆë¥¼ ë”í•œê²ƒê³¼ ê°€ìž¥ ê°€ê¹Œìš´ start point
        cut.append(tmp2)
        tmp2=[]
    return cut

        
def make_clip(title, cut):
    path = '/Users/dai/desktop/sample/video/'+title
    for i, c in enumerate(cut):
        output = '/Users/dai/desktop/sample/video/clip/'+str(i)+title
        ffmpeg_extract_subclip(path, c[0], c[len(c)-1], targetname=output)



def main():
    path = '/Users/dai/desktop/sample/video/'
    file = path+'sample.srt'
    res = get_bucket(file)
    start_point = get_time(res)    
    start = get_csv(path+'sample.csv')
    cut=cut_clip(start, start_point)
    title = 'sample.mp4'
    make_clip(title, cut)
    # print(cut)



main()
