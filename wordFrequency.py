import numpy as np
import pandas as pd
import csv
import re
import numpy as np
import jieba
import jieba.analyse
import codecs
import collections # 词频统计库
# 统计词频

stopwords = [line.strip() for line in codecs.open('中文停用词库.txt', 'r', 'utf-8').readlines()]

def wordFrequency(inPath):
    reader = open(inPath, encoding='utf-8-sig')
    train_data = reader.readlines()
    object_list = []
    for i in range(len(train_data[0:5000])):
        if (i % 2 == 0):
            sen = train_data[i]
            sen = sen.replace(' ', '')
            sen = sen.replace('\n', '')
            # TextRank 关键词抽取，只获取固定词性
            words = jieba.cut(sen, cut_all=False)  # 精确模式分词
            for word in words:
                # 停用词判断，如果当前的关键词不在停用词库中才进行记录
                if word not in stopwords:
                    object_list.append(word)
    word_counts = collections.Counter(object_list)  # 对分词做词频统计
    word_counts_top10 = word_counts.most_common(10)  # 获取前10最高频的词
    print (word_counts_top10)  # 输出检查
    with open(outPath, "w") as f:
        for i in word_counts_top10:
            f.writelines(i[0])
            f.write("\n")

if __name__ == '__main__':
    inPath = "../train_data/sentences.txt"
    outPath = "wordFrequency.txt"
    wordFrequency(inPath)