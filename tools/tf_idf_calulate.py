import os
import math
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

def read_files(input_root):
    """读取所有文件，并返回一个字典，其中键是文件名，值是文件中的单词集合。"""
    files_content = {}
    for filename in os.listdir(input_root):
        file_path = os.path.join(input_root, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            words = set(word for word in content.split() if not word.isdigit())
            files_content[filename] = words
    return files_content

def calculate_idf(word, files_content):
    """计算给定单词的IDF值。"""
    total_files = len(files_content)
    count = sum(1 for words in files_content.values() if word in words)
    return math.log(((total_files+1) / (count + 1)))

def process_txt_file(result_file, input_folder, output_file):
    # 读取所有文件的内容
    files_content = read_files(input_folder)

    # 读取结果文件中的所有单词
    all_words = read_result(result_file)

    # 使用线程池并行计算IDF值
    word_idf_dict = {}
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(calculate_idf, word, files_content): word for word in all_words}
        for future in futures:
            word = futures[future]
            idf_value = future.result()
            print(f'words：{word}, value：{idf_value}')
            word_idf_dict[word] = idf_value

    # 对单词按IDF值降序排序
    sorted_word_counts = sorted(word_idf_dict.items(), key=lambda x: x[1], reverse=False)

    # 将结果写入输出文件
    with open(output_file, 'w', encoding='utf-8') as output:
        for word, count in sorted_word_counts:
            output.write(f"{word} {count}\n")

def read_result(file_path):
    """从指定路径读取文件内容，返回过滤后的单词列表。"""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        words = [word for word in content.split() if not word.isdigit()]
        return words

# 调用函数
all_words_file = r"..\resource\result_retry\count_all.txt"
input_folder = r"..\resource\retry"
output_file = r"..\resource\result_retry\idf_all.txt"

process_txt_file(all_words_file, input_folder, output_file)