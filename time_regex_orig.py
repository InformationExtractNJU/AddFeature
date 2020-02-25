import re
import os

inPath = "sentences/sentences/"
outPath = "NewsCar_time/"


path = "NewsCar_time"
if not os.path.exists(path):
    os.makedirs(path)
for t in range(2015, 2020):
    p = outPath+str(t)
    if not os.path.exists(p):
        os.makedirs(p)
    for h in range(1, 13):
        p_dir = p+'/'+str(h)
        if not os.path.exists(p_dir):
            os.makedirs(p_dir)



# 正则取时间
def get_time(text):
    # 日期格式统一化 2019/12/25 ---> 2019-12-25
    # text = text.replace("年", "-").replace("月", "-").replace("日", " ").replace("/", "-").strip()
    list = []
    text = text.replace("/", "-").strip()
    text = re.sub("\s+", " ", text)
    t = ""
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
        t = re.search(regex, text)
        if t:
            t = t.group(1)
            list.append(t+';')
        # else:
        #     print("没有获取到有效日期")
    return list


def cut_time():

    # 要查找的文件夹地址
    for year in range(2015, 2020):
        for month in range(1, 13):
            dir = inPath+str(year)+"/"+str(month)
            number = 0
            # os.walk()方法是一个简单易用的文件、目录遍历器
            # root正在遍历的这个文件夹的本身的地址
            # dirname是一个list,内容是该文件夹中所有的目录的名字(不包括子目录)
            # filenames同样是list,内容是该文件夹中所有的文件名字(不包括子目录)
            for root, dirname, filenames in os.walk(dir):
                for filename in filenames:
                    # print(filename)
                    f1 = open(r''+dir+'/'+filename, 'r', encoding='UTF-8')
                    f2 = open(r''+outPath+str(year)+'/'+str(month)+'/'+filename, 'a', encoding='UTF-8')
                    i = 0
                    for lines in f1:
                        # 每个txt的一行截得time
                        line_time_list = []
                        i += 1
                        string = ''
                        line_time_list = get_time(lines)
                        for time in line_time_list:
                            string += time
                        # print('id:' + str(i) + ' time:'+string+'\r\n')
                        f2.write('id:' + str(i) + ' time:'+string+'\n')
                        # print(string)

                    # os.path.splitext()是一个元组,类似于('188739', '.txt')，索引1可以获得文件的扩展名
            #         if os.path.splitext(filename)[1] == '.txt':
            #             number += 1
            # print(str(year)+"_"+str(month)+"_"+str(number))


if __name__ == '__main__':
    cut_time()
    text1 = "8月，衢州元立金属制品有限公司仓储公司（以下简称元立仓储公司）成品仓库发生一起物体打击事故，给2019年造成直接经济损失95万元。"
    text2 = "12/28下达行政处罚决定书"
    text3 = "2015年发生一起物体打击事故"
    # for time in get_time(text3):
    #     print(time)
    # print(get_time(text1))
    # print(get_time(text2))
    # print(get_time(text3))




