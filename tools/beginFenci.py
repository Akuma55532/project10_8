import os
import re
from ltp import LTP
from collections import Counter

ltp = LTP("../ltp_model/base1")

input_folder_path = r"..\resource\resource_temp2 - 副本"
output_folder_path = r"..\resource\retry"

dict_path = "../resource/dict/end.txt"

def read_dict(input_file):
    words_dict = []
    with open(input_file,'r',encoding='utf-8') as file:
        for line in file:
            word = line.split()
            words_dict.append(word[0])
    return words_dict

words_dict = read_dict(dict_path)

print(words_dict)

# ltp.add_word(word='长江大桥',freq=10)

for word in words_dict:
    ltp.add_word(word,freq=10000)

def extract_number_from_filename(filename):
    """从文件名中提取数字"""
    match = re.search(r'_(\d+)\.txt$', filename)
    return int(match.group(1)) if match else 1


def process_txt_file(input_root, output_root):
    if not os.path.exists(input_root):
        print(f"错误：路径 {input_root} 不存在")
        return

    if not os.path.exists(output_root):
        os.makedirs(output_root)

    batch_size = 500  # 每个批次的字符数

    for filename in os.listdir(input_root):

        # 初始化一个空列表，用于存储所有批次的专有名词
        all_proper_nouns = []

        if filename.endswith('.txt'):
            file_path = os.path.join(input_root, filename)
            print(f'正在处理: {filename}')

            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()

            text = text.replace(" ", "")
            # 将文本分成多个小批次
            batches = [text[i:i + batch_size] for i in range(0, len(text), batch_size)]

            # 对每个批次进行分词和词性标注
            for batch in batches:
                # print(batch)2
                batch = batch.replace(" ", "")
                result = ltp.pipeline([batch], tasks=["cws","pos"])
                words = result.cws[0]
                pos_word = result.pos[0]
                # print(words)

                # 提取名词和动词，并根据文件名中的数字重复统计
                for word,pos in zip(words,pos_word):
                    if pos in ['n','v'] and len(word) < 20:
                        all_proper_nouns.append(word)

        word_counts = Counter(all_proper_nouns)

        new_filename = filename.removesuffix('.txt')

        result_path = os.path.join(output_root, f"{new_filename}_count.txt")

        with open(result_path, 'w', encoding='utf-8') as output_file:
            for word, count in word_counts.items():
                output_file.write(f"{word}\t{count}\n")



process_txt_file(input_folder_path, output_folder_path)
