import re

def read_words(file_path):
    """从指定路径的文件中读取单词，并返回一个单词列表"""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        # 使用空格分割内容，得到单词列表
        words = content.split()
        # 过滤掉数字，只保留单词
        words = [word for word in words if not word.isdigit()]
    return set(words)  # 使用集合来去除重复项


def read_count_dict(file_path):
    word_count = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            word, count = line.strip().split()
            word_count[word] = int(count)
    return word_count



def find_common_words(file1, file2, output_file):
    """找到两个文件中的公共单词，并将结果写入新的文件"""
    words_set1 = read_words(file1)
    words_set2 = read_words(file2)

    words_dict1 = read_count_dict(file1)
    words_dict2 = read_count_dict(file2)

    common_words = words_set1.intersection(words_set2)

    # 使用正则表达式筛选出汉字
    hanzi_pattern = re.compile(r'[\u4e00-\u9fff]+')

    # 筛选出集合中的汉字
    filtered_set = set(filter(hanzi_pattern.fullmatch, common_words))

    common_list = []

    for word in filtered_set:
        temp = words_dict1[word] + words_dict2[word]
        common_list.append((word,temp))

    common_list = sorted(common_list, key=lambda x: x[1], reverse=True)

    print(common_list)

    with open(output_file, 'w', encoding='utf-8') as file:
        for word,count in common_list:
            file.write(f"{word}\t{count}\n")


def find_common_words2(file1, file2, output_file):
    """找到两个文件中的公共单词，并将结果写入新的文件"""
    words_set1 = read_words(file1)
    words_set2 = read_words(file2)

    # words_dict1 = read_count_dict(file1)
    # words_dict2 = read_count_dict(file2)

    common_words = words_set1.intersection(words_set2)

    print(common_words)


    print(len(common_words))
    print(len(words_set1))
    print(len(words_set2))
    print(words_set2)
    print(len(common_words)/len(words_set2))

    # # 使用正则表达式筛选出汉字
    # hanzi_pattern = re.compile(r'[\u4e00-\u9fff]+')
    #
    # # 筛选出集合中的汉字
    # filtered_set = set(filter(hanzi_pattern.fullmatch, common_words))
    #
    # common_list = []
    #
    # for word in filtered_set:
    #     temp = words_dict1[word] + words_dict2[word]
    #     common_list.append((word,temp))
    #
    # common_list = sorted(common_list, key=lambda x: x[1], reverse=True)

    with open(output_file, 'w', encoding='utf-8') as file:
        for word in common_words:
            file.write(f"{word}\n")

# 指定文件路径
file1 = r"..\resource\ful2\common.txt"
file2 = r"..\resource\ful2\filter.txt"
output_file = r"..\resource\ful2\common_2.txt"

# 调用函数
find_common_words2(file1, file2, output_file)