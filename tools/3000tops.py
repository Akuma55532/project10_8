import os
import re


def read_result(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        # 使用空格分割内容，得到单词列表
        words = content.split()
        # 过滤掉数字，只保留单词
        words = [word for word in words if not word.isdigit()]

        return words[:3000]

def cipi_back(file_path,words_set):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        word_to_number = {}
        for line in content.strip().split('\n'):
            word, number = line.split()
            word_to_number[word] = int(number)

        result = {word: word_to_number.get(word, None) for word in words_set}

        return result

def read_file2(file_path):
    """读取文件并返回字典，键为词语，值为词频"""
    word_to_freq = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            word, freq = line.strip().split()
            word_to_freq[word] = int(freq)
    return word_to_freq


def cipin_back_chongfu(file1_path,file2_path,words_set):
    word_to_freq_A = read_file2(file1_path)
    word_to_freq_B = read_file2(file2_path)

    result = {}
    for word in words_set:
        total_freq = word_to_freq_A.get(word, 0) + word_to_freq_B.get(word, 0)
        result[word] = total_freq

    return result


def write_chongfu(file1_path,file2_path,output_file):
    jichu_3000tops = read_result(file1_path)
    hexin_3000tops = read_result(file2_path)

    jichu_3000tops_set = set(jichu_3000tops)
    hexin_3000tops_set = set(hexin_3000tops)

    common_words = jichu_3000tops_set.intersection(hexin_3000tops_set)

    only_in_jichu = jichu_3000tops_set - hexin_3000tops_set
    only_in_hexin = hexin_3000tops_set - jichu_3000tops_set

    only_in_jichu_withcount = cipi_back(file1_path,only_in_jichu)
    only_in_hexin_withcount = cipi_back(file2_path,only_in_hexin)

    sorted_word_to_number_jichu = sorted(only_in_jichu_withcount.items(), key=lambda item: item[1], reverse=True)
    sorted_word_to_number_hexin = sorted(only_in_hexin_withcount.items(), key=lambda item: item[1], reverse=True)

    output_file_only_in_jichu = os.path.join(output_file,"only_in_jichu.txt")
    output_file_only_in_hexin = os.path.join(output_file, "only_in_hexin.txt")

    # 将排序后的键值对写入到文件中
    with open(output_file_only_in_jichu, 'w', encoding='utf-8') as file:
        for word, number in sorted_word_to_number_jichu:
            file.write(f"{word} {number}\n")
    with open(output_file_only_in_hexin, 'w', encoding='utf-8') as file:
        for word, number in sorted_word_to_number_hexin:
            file.write(f"{word} {number}\n")

    common_words_withcount = cipin_back_chongfu(file1_path,file2_path,common_words)

    sorted_word_to_number_common = sorted(common_words_withcount.items(), key=lambda item: item[1], reverse=True)

    output_file_only_in_common = os.path.join(output_file, "common_3000tops.txt")

    with open(output_file_only_in_common, 'w', encoding='utf-8') as file:
        for word, number in sorted_word_to_number_common:
            file.write(f"{word} {number}\n")

    print(common_words_withcount)



file1 = r"..\resource\resource_test\temp\jichu_results.txt"
file2 = r"..\resource\resource_test\temp\hexin_results.txt"
output_file = r"..\resource\resource_test\result"

write_chongfu(file1,file2,output_file)
# cipi_back(file1)


