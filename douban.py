# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
import csv
import sys
import importlib
from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import jieba
import re # 正则表达式库
import collections # 词频统计库
import numpy as np # numpy数据处理库
import jieba # 结巴分词
import wordcloud # 词云展示库
from PIL import Image # 图像处理库
import matplotlib.pyplot as plt # 图像展示库
import cv2 as cv
importlib.reload(sys)
headers1={
  'user-agent':'Mozilla/5.0'
}#模拟浏览器进行爬取

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:28.0) Gecko/20100101 Firefox/28.0',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Cookie':'bid="hsM53yRAjQ8"; __utma=30149280.907110929.1386117661.1398322932.1398335444.20; __utmz=30149280.1398167843.17.13.utmcsr=baidu|utmccn=(organic)|utmcmd=organic|utmctr=urllib2%20403; ll="118281"; __utma=223695111.1156190174.1396328833.1398322932.1398335444.11; __utmz=223695111.1396588375.4.4.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmb=30149280.1.10.1398335444; __utmc=30149280; __utmb=223695111.1.10.1398335444; __utmc=223695111',
'Host':'movie.douban.com'
}




def get_prov_year_list(url):
    r=url
    html = requests.get(r,headers=headers)
    html.raise_for_status()
    html.encoding = html.apparent_encoding#内容获取的内容进行转码，以防出现乱码的情况。    
    soup = BeautifulSoup(html.text,'html.parser')
    tmplist = soup.find_all(class_='hd')#获取第一页href相关的位置
    chinese=[]
    yue=[]
    eng=[]
    href=[]
    for i in range(len(tmplist)):
        href.append(tmplist[i].a['href'])
       
        tmp=(tmplist[i].a.find_all('span', recursive=False))
        namelist=[]
        
        for span in tmp:

            j=re.sub('\s', ' ', span.string)
            namelist.append(j)
        try:
            chinese.append(namelist[0])
        except:
            chinese.append('null')
        try:
            eng.append(namelist[1])
        except:
            eng.append('null')
        try:
            yue.append(namelist[2])
        except:
            yue.append('null')
    return href,chinese,yue,eng

# print(href)
# print(chinese)
# print(yue)
# print(eng)
def download(html,name,type_,tdir):
    #通过正则匹配
    for i in range(len(html)):
        try:
            pic = requests.get(html[i], timeout=10)
        except requests.exceptions.ConnectionError:
            print('无法下载')
        #保存图片路径
        dir1 = tdir+'\\'+name+str(i)+'.'+type_
        fp = open(dir1, 'wb')
        fp.write(pic.content)
        fp.close()
def get_prov_year_list1(url,name,tdir):
    r=url
    html = requests.get(r,headers=headers)
    html.encoding = html.apparent_encoding
    html.raise_for_status()
    html.encoding = html.apparent_encoding#内容获取的内容进行转码，以防出现乱码的情况。    
    soup = BeautifulSoup(html.text,'html.parser')
    try:
        tmplist = soup.find_all(class_='all hidden')#获取第一页href相关的位置
        bref=((tmplist[0]).text)
    except:
        tmplist = soup.find_all('span', attrs={'property': 'v:summary'})     
        bref=((tmplist[0]).text)

    tmplist = soup.find_all(class_='avatar')
    html=[]
    for i in range(len(tmplist)):       
        c=tmplist[i].attrs['style']
        html.append(c[22:len(c)-1:])
    download(html,name,'jpg',tdir)
    tmplist = soup.find_all(class_='related-pic-video')
    video=[]
    for i in range(len(tmplist)):  
        c=tmplist[i].attrs['href']
        video.append(c)
    return bref,video
# get_prov_year_list1('https://movie.douban.com/subject/1292052/')
def doit(url):
    href,chinese,yue,eng=(get_prov_year_list(url))
    tar=[]
    for i in range(len(chinese)):
        tmp=[chinese[i],yue[i],eng[i]]
        tar.append(tmp)
    bf=[]
    for i in range(len(href)):
        b=os.getcwd()
        try:
            os.mkdir(b+'\\'+chinese[i])
        except:
            pass
        tdir=b+'\\'+chinese[i]+'\\图片'
        try:
            os.mkdir(tdir)
        except:
            pass
        bef,video=get_prov_year_list1(href[i],chinese[i],tdir)
        
        tar[i].append(bef)
        tar[i].append(video)
        # print(bef,video)
        
        with open(b+'\\'+chinese[i]+'\\'+chinese[i]+'.csv', 'w', newline='',encoding='utf-8') as csvfile:
            writer  = csv.writer(csvfile)
            writer.writerow(tar[i])
        wc1(href[i],tdir)
    # print(chinese,yue,eng)





def wc1(url,tdir):
    r=url
    html = requests.get(r,headers=headers)
    html.encoding = html.apparent_encoding
    html.raise_for_status()
    html.encoding = html.apparent_encoding#内容获取的内容进行转码，以防出现乱码的情况。    
    soup = BeautifulSoup(html.text,'html.parser')
    try:
        tmplist = soup.find_all(class_='mod-hd')#获取第一页href相关的位置
        tmplist = tmplist[0].find_all('span', attrs={'class': 'pl'})    
        for i in range(len(tmplist)):
            tmplist1 = tmplist[i].a['href']
            # print(tmplist1)
            # print("="*1000)
        
    except:
        pass
    r=tmplist1
    short=[]
    for i in range(10):
        html = requests.get(r,headers=headers)
        html.raise_for_status()
        html.encoding = 'utf-8'#内容获取的内容进行转码，以防出现乱码的情况。    
        soup = BeautifulSoup(html.text,'html.parser')
        tmplist = soup.find_all(class_='short')
        for i in range(len(tmplist)):
            s=tmplist[i].text
            short.append(s)
        tmplist = soup.find_all(class_='next')
        # print(tmplist)
        aa=(tmplist[0]['href'])
        head, sep, tail = tmplist1.partition('?')
        html1=head+aa
        # print(html1)
        r=html1
    with open(tdir+'\\短评荟萃.txt', 'w',encoding='utf-8') as f:
        for i in range(len(short)):
            f.write(short[i])
            f.write('\n')
            f.write('\n')
            f.write('\n')
    # print(short)
    long=''
    for i in range(len(short)):
        long+=short[i]
    seg_list_exact = jieba.cut(long, cut_all = False) # 精确模式分词
    object_list = []
    remove_words = [u'的', u'，',u'和', u'是', u'随着', u'对于', u'对',u'等',u'你',u'都',u'。',u' ',u'、',u'中',u'在',u'了',
                 u'就是',u'啊',u'我们',u'看过',u'我',u'看',u'电影',u'很',u'时候',u'这部',u'也'] # 自定义去除词库
   
    for word in seg_list_exact: # 循环读出每个分词
       if word not in remove_words: # 如果不在去除词库中
         object_list.append(word) # 分词追加到列表
 
    word_counts = collections.Counter(object_list) # 对分词做词频统计
    word_counts_top10 = word_counts.most_common(10) # 获取前10最高频的词
    print (word_counts_top10) # 输出检查
 
    mask = np.array(Image.open('RS.jpg')) # 定义词频背景
    wc = wordcloud.WordCloud(
        font_path='C:/Windows/Fonts/simhei.ttf', # 设置字体格式
        mask=mask, # 设置背景图
        max_words=200, # 最多显示词数
        max_font_size=200 )# 字体最大值)
    wc.generate_from_frequencies(word_counts) # 从字典生成词云
    image_colors = wordcloud.ImageColorGenerator(mask) # 从背景图建立颜色方案
    wc.recolor(color_func=image_colors) # 将词云颜色设置为背景图方案
    wc.to_file(tdir+"\\词云图片.jpg")    #保存为图片
url = 'https://movie.douban.com/top250?start=0'
doit(url)
# url1 = 'https://movie.douban.com/top250?start=25'
# url2 = 'https://movie.douban.com/top250?start=50'
# doit(url1)
# doit(url2)  
# url='https://movie.douban.com/subject/1292722/?from=subject-page'
# wc1(url)


























def vis(url,dic):
 req=requests.post(url,dic)
 req.raise_for_status()
 req.encoding = req.apparent_encoding#内容获取的内容进行转码，以防出现乱码的情况。    
 # print(html.text)
 soup = BeautifulSoup(req.text,'html.parser')
 tmplist =str( soup)#获取第一页href相关的位置

 
 tmplist=re.findall( r'(?<=">).*?(?=</td)',tmplist)

 for i in range(len(tmplist)):
    if tmplist[i]=='历年分数线':
        tmplist=tmplist[i+2:len(tmplist)-2:]
        break
 name=tmplist[:8:]
 tmplist=tmplist[8::]

 res=[]
 for i in range(0,len(tmplist),8):
    res.append(tmplist[i:i+8:])
 return name ,res



def getdata(provence_list,year_list):
 dic={}
 result=[]
 for j in year_list:
    for i in provence_list:
        dic={'pro':i,'year':j}
        name,res=vis(url,dic)
        for item in res:
            item.append('燕山大学')
            item.append(j)
            item.append('09118129陈翼张')
        result.append(res)
 result=sum(result,[])
 name=['Province',	'Major',	'Category'	,'最高分'	,'Score','平均分',	'人数'	,'一本线	','College'	,'Year','Contributor']
 test=pd.DataFrame(columns=name,data=result)
 return test
def data_washer(test):   
 name=['最高分'	,'平均分',	'人数'	,'一本线	']
 test=test.drop(name,axis=1)
 name=['College'	, 'Year'	,'Province','Category'	,'Major',	'Score','Contributor']
 test = test.loc[:,name]
 return test
def run_web_crawler():
    provence_list,year_list = get_prov_year_list(url)
    year_list=sum(year_list,[])
    provence_list=sum(provence_list,[])
    #print(provence_list)
    test=data_washer(getdata(provence_list,year_list))
    test.to_csv('./09118129陈翼张-燕山大学.csv',index=False)
# if __name__ == '__main__':
#     run_web_crawler()