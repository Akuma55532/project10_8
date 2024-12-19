import os
from collections import defaultdict


def read_file(input_root):
    length = 0
    for filename in os.listdir(input_root):

        file_path = os.path.join(input_root,filename)

        with open(file_path, 'r', encoding='utf-8') as file:
            # 读取文件内容
            content = file.read()

            pattern = r'[^\u4e00-\u9fff]'
            # 将非中文字符替换为空字符串
            cleaned_text = re.sub(pattern, '', content)

            length += len(cleaned_text)

    print(length)


def aggregate_word_frequencies(folder_path,output_file):
    # 使用defaultdict来自动处理不存在的键
    word_freq = defaultdict(int)

    # 遍历指定文件夹下的所有文件
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    parts = line.strip().split()
                    if len(parts) == 2:
                        word, freq_str = parts


    # 将结果写入输出文件
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for word, freq in sorted(word_freq.items(), key=lambda item: item[1], reverse=True):
            outfile.write(f"{word} {freq}\n")


def read_file_length(input_root):
    length = 0
    for filename in os.listdir(input_root):

        file_path = os.path.join(input_root,filename)

        with open(file_path, 'r', encoding='utf-8') as file:
            # 读取文件内容
            content = file.read()

            pattern = r'[^\u4e00-\u9fff]'
            # 将非中文字符替换为空字符串
            cleaned_text = re.sub(pattern, '', content)

            length += len(cleaned_text)

    return


def read_words(file_path):
    """从指定路径的文件中读取单词，并返回一个单词列表"""
    words_return = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 2:
                word, freq_str = parts
                words_return.append(word)
            if len(parts) == 3:
                word, freq_str, idf_str = parts
                words_return.append(word)
    return set(words_return)  # 使用集合来去除重复项

def read_dict(file_path):
    """从指定路径的文件中读取单词，并返回一个单词列表"""
    words_return_dict = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 2:
                word, freq_str = parts
                words_return_dict[word] = int(freq_str)
    return words_return_dict  # 使用集合来去除重复项


def words_count(file_path):
    counts = 0
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 2:
                word, freq_str = parts
                counts += int(freq_str)
    return counts  # 使用集合来去除重复项


def main(input_folder_overall,output_file):

    words_filter = read_words(filter_path)

    dict_man = {}

    for filename in os.listdir(input_folder_overall):
        if filename.endswith('.txt'):
            filepath = os.path.join(input_folder_overall,filename)

            words_set = read_words(filepath)

            words_dict = read_dict(filepath)

            fenmu = words_count(filepath)

            print(len(words_set))
            print(len(words_filter))

            common_words = words_set.intersection(words_filter)

            fenzi = 0

            for word in common_words:
                fenzi += words_dict[word]

            dict_man[filename] = fenzi / fenmu

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for word, value in sorted(dict_man.items(), key=lambda item: item[1], reverse=True):
            outfile.write(f"{word}                {value}\n")

def main2(input_folder_overall,output_file):
    words_filter = read_words(filter_path)

    dict_man = {}

    for filename in os.listdir(input_folder_overall):
        if filename.endswith('.txt'):
            filepath = os.path.join(input_folder_overall,filename)

            words_set = read_words(filepath)

            words_dict = read_dict(filepath)

            fenmu = read_file_length(filepath)

            common_words = words_set.intersection(words_filter)

            fenzi = 0

            for word in common_words:
                fenzi += words_dict[word]

            dict_man[filename] = fenzi / fenmu

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for word, value in sorted(dict_man.items(), key=lambda item: item[1], reverse=True):
            outfile.write(f"{word}                {value}\n")


# 指定文件夹路径和输出文件名
folder_path = r'..\resource\resource_test\count\result'  # 替换为你的文件夹路径
filter_path = r'..\resource\ful2\filter.txt'  # 替换为你的文件夹路径
output_folder = r'..\resource\resource_test\十二个专业的语料\result.txt'

text_path = r'..\resource\resource_test\十二个专业的语料'  # 替换为你的文件夹路径

# 调用函数
# main(folder_path,output_folder)

main2(folder_path,output_folder)

print("聚合完成，结果已保存至")
