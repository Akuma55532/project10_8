import os
import re
import itertools
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np


def read_count(file_path):
    word_count = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            word, count = line.strip().split()
            word_count.append((word,int(count)))
    return word_count

def read_count_dict(file_path):
    word_count = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            word, count = line.strip().split()
            word_count[word] = int(count)
    return word_count


def read_idf(file_path):
    word_idf = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            word, idf = line.strip().split()
            word_idf.append((word,float(idf)))
    return word_idf


def drawpic(file_count,file_idf):

    # word_count = read_count(file_count)
    #
    # word_count.reverse()
    #
    # count_max = int(word_count[-1][1] / 100) +1
    #
    # count_list = [0]*(count_max+1)
    #
    # for i in range(1,count_max+1):
    #     for word,count in word_count:
    #         if count < i*100 and count >= (i-1)*100:
    #             count_list[i-1] += 1*count
    #         elif count >= i*100:
    #             count_list[i] += 1*count
    #             break
    #
    # fenduan_count = list(range(0,len(count_list)*100,100))

    word_idf = read_idf(file_idf)

    word_count_dict = read_count(file_count)

    idf_max = float(word_idf[-1][1]) + 1

    word_list = [0] * int(idf_max)

    for i in range(1,int(idf_max+1)):
        for word,idf in word_idf:
            if idf < i and idf >= (i-1):
                word_list[i-1] += word_count_dict[]
            elif idf >= i:
                word_list[i] += word_count_dict[]
                break

    fenduan_idf = list(range(0, len(word_list)))

    print(fenduan_idf)

    # 创建柱状图
    plt.bar(fenduan_idf, word_list)

    # 显示图形
    plt.show()


file_count = r"..\resource\ful2\count_all.txt"
file_idf = r"..\resource\ful2\idf_all.txt"

drawpic(file_count,file_idf)

