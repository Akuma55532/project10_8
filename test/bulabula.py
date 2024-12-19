from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from openai import OpenAI
import re

# 定义过滤词文件路径
COMMON_PATH = r'..\resource\拼音排序\通用_remote.txt'

TECH_PATH = r'..\resource\拼音排序\技术_remote.txt'


def read_words_from_file(filepath):
    """
    从文件中读取词语列表
    :param filepath: 文件路径
    :return: 词语列表
    """
    words_list = []
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                line_split = line.strip().split('/')
                words_list.append(line_split)
    except FileNotFoundError:
        print(f"文件未找到: {filepath}")
    return words_list


print(read_words_from_file(COMMON_PATH))