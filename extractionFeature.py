import numpy as np
import pandas as pd
import csv
import re
import jieba
import jieba.analyse
import jieba.posseg

dataPath = "CarDic_merge.xlsx"

car_data=pd.read_excel(dataPath)
group = car_data["汽车集团"].values
company = car_data["汽车公司"].values

car = car_data["汽车"].values
cars = []
for i in range(len(car)):
    cars+=str(car[i]).split(";")

cars=list(set(cars))

# 正则取时间
def getTimeIndex(text):
    # 日期格式统一化 2019/12/25 ---> 2019-12-25
    # text = text.replace("年", "-").replace("月", "-").replace("日", " ").replace("/", "-").strip()
    list = [0]*len(text)
    # print (list)
    regex_list = [
        # 2019-12-25 22:46:21
        "(\d{4}-\d{1,2}-\d{1,2}\d{1,2}:\d{1,2}:\d{1,2})",
        # "2019-12-25 22:46"
        "(\d{4}-\d{1,2}-\d{1,2}\d{1,2}:\d{1,2})",
        # "2019-12-25"
        "(\d{4}-\d{1,2}-\d{1,2})",
        # "2019-12"
        "(\d{4}-\d{1,2})",
        # "12-25"
        "(\d{1,2}-\d{1,2})",
        # "2019年12月25日"
        "(\d{4}年\d{1,2}月\d{1,2}日)",
        # "2019年12月"
        "(\d{4}年\d{1,2}月)",
        # "2019年"
        "(\d{4}年)",
        # "12月"
        "(\d{1,2}月)",
        # "12月25日"
        "(\d{1,2}月\d{1,2}日)",
    ]
    for regex in regex_list:
        find_list = re.search(regex, text)
        # print (find_list)
        if find_list:
            index=find_list.span()
            for i in range(index[0],index[1]):
                list[i]=1
    # print (list)
    return list


Loc_data_reader = open('loc.txt',encoding = 'utf-8-sig')
Loc_data=Loc_data_reader.readlines()
for i in range(len(Loc_data)):
    Loc_data[i]=Loc_data[i][:-1]

# print (Loc_data)

def getLocIndex(text):
    list = [0] * len(text)

    # print (Loc_data)
    for i in Loc_data:
        t=re.search(i, text)
        if t:
            index = t.span()
            for j in range(index[0], index[1]):
                list[j] = 1
    return list

tech_data_reader = open('technology.txt',encoding = 'utf-8-sig')
tech_data=tech_data_reader.readlines()

for i in range(len(tech_data)):
    tech_data[i]=tech_data[i][:-1]

def getTechIndex(text):
    list = [0] * len(text)
    # print (Loc_data)
    for i in tech_data:
        t = re.search(i, text)
        if t:
            index = t.span()
            for j in range(index[0], index[1]):
                list[j] = 1
    return list

def getCarIndex(text):
    list = [0] * len(text)
    # print (Loc_data)
    for i in cars:
        # print(i)
        t = re.search(i, text)
        if t:
            index = t.span()
            for j in range(index[0], index[1]):
                list[j] = 1
    return list

def getLetterIndex(text):
    list=[0]*len(text)
    for i in range(len(text)):
        if (text[i] >= u'\u0041' and text[i] <= u'\u005a') or (text[i] >= u'\u0061' and text[i] <= u'\u007a'):
            # print (text[i],end="")
            list[i]=1
    return list
        # if(i >= u'\u0041' and i <= u'\u005a')

def getCompanyIndex(text):
    list = [0] * len(text)
    # print (Loc_data)
    for i in company:
        # print(i)
        i = i.replace('）',')')
        i = i.replace('（', '(')
        t = re.search(i, text)
        if t:
            # print (t)
            index = t.span()
            for j in range(index[0], index[1]):
                list[j] = 1
    return list

def extractionFeature(inPath,outPath):
    reader = open(inPath, encoding='utf-8-sig')
    train_data = reader.readlines()
    time_label_data = []
    loc_label_data = []
    tech_label_data = []
    car_label_data = []
    company_label_data = []
    letter_label_data = []
    for i in range(len(train_data)):
        if (i % 2 == 0):
            print(int(i / 2))
            sen = train_data[i]
            sen = sen.replace(' ', '')
            sen = sen.replace('\n', '')
            # print(sen)
            time_label = getTimeIndex(sen)
            time_label_data.append(time_label)
            # print (time_label)
            loc_label = getLocIndex(sen)
            loc_label_data.append(loc_label)
            # print (loc_label)
            tech_label = getTechIndex(sen)
            tech_label_data.append(tech_label)
            # print (tech_label)
            car_label = getCarIndex(sen)
            car_label_data.append(car_label)
            # print (car_label)
            company_label = getCompanyIndex(sen)
            company_label_data.append(company_label)

            letter_label = getLetterIndex(sen)
            letter_label_data.append(letter_label)
            # print (company_label)

    with open("sentence_add_tec_add_label.txt", "w", encoding='utf-8-sig') as f:
        for i in range(len(train_data)):
            if (i % 2 == 0):
                print(int(i / 2))
                # print (time_label_data[i])
                # print (loc_label_data[i])
                f.write(train_data[i])
                f.write(" ".join(str(time_label_data[int(i / 2)])))
                f.write("\n")
                f.write(" ".join(str(loc_label_data[int(i / 2)])))
                f.write("\n")
                f.write(" ".join(str(tech_label_data[int(i / 2)])))
                f.write("\n")
                f.write(" ".join(str(car_label_data[int(i / 2)])))
                f.write("\n")
                f.write(" ".join(str(company_label_data[int(i / 2)])))
                f.write("\n")
                f.write(" ".join(str(letter_label_data[int(i / 2)])))
                f.write("\n")

# 传入一个字符串，用jieba分词获取时间
def getTimeByJieba(sentence):
    timeList=[]
    sentence_seged = jieba.posseg.cut(sentence.strip())
    for x in sentence_seged:
        if(x.flag=='t'):
            timeList.append(x.word)
    return timeList

# 传入一个字符串，用jieba分词获取地点
def getLocByJieba(sentence):
    locList = []
    sentence_seged = jieba.posseg.cut(sentence.strip())
    for x in sentence_seged:
        if (x.flag == 'ns'):
            locList.append(x.word)
    return locList

if __name__ == '__main__':
    # inPath = "../train_data/sentences.txt"
    # outPath = "sentence_add_tec_add_label.txt"
    # extractionFeature(inPath, outPath)

    test = "明天北京举办了奥运会"
    res = getTimeByJieba(test)
    print (res)
# outPath = "NewsCar_time/"








