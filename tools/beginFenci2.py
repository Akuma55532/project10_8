import os
import re
from collections import Counter

def read_file(file_path):
    """读取文件并返回字典，键为词语，值为词频"""
    word_to_freq = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            word, freq = line.strip().split()
            word_to_freq[word] = int(freq)
    return word_to_freq


def process_txt_file(input_root, output_root):
    if not os.path.exists(input_root):
        print(f"错误：路径 {input_root} 不存在")
        return

    if not os.path.exists(output_root):
        os.makedirs(output_root)

    all_proper_nouns = {}

    for filename in os.listdir(input_root):

        # 初始化一个空列表，用于存储所有批次的专有名词

        if filename.endswith('.txt'):
            file_path = os.path.join(input_root, filename)
            print(f'正在处理: {filename}')

            word_to_freq = read_file(file_path)

            # 提取名词和动词，并根据文件名中的数字重复统计
            for word, count in word_to_freq.items():
                if word in all_proper_nouns:
                    all_proper_nouns[word] += count
                else:
                    all_proper_nouns[word] = count

    # word_counts = Counter(all_proper_nouns)




    result_path = os.path.join(output_root, "count_all.txt")

    with open(result_path, 'w', encoding='utf-8') as output_file:
        for word, count in all_proper_nouns.items():
            output_file.write(f"{word}\t{count}\n")




input_folder_path = r"..\resource\retry"  # 替换为你的PDF文件所在的路径
output_folder_path = r"..\resource\result_retry"  # 替换为你的输出文件夹路径

process_txt_file(input_folder_path, output_folder_path)

