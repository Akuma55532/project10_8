import os
import re


def read_file(input_file):
    all_words_dict = {}

    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            line_split = line.strip().split()  # 去除行末的换行符并分割
            if len(line_split) == 2:
                word, count = line_split[0], int(line_split[1])
                all_words_dict[word] = count
    return all_words_dict

def read_file_fromidf(input_file):
    all_words_dict = {}

    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            line_split = line.strip().split()  # 去除行末的换行符并分割
            if len(line_split) == 2:
                word, count = line_split[0], float(line_split[1])
                all_words_dict[word] = count
    return all_words_dict
def write_to_file(hebing_list, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for word, count, idf in hebing_list:
            file.write(f"{word} {count} {idf}\n")


def get_info(key):
    word = key
    count = count_dict_.get(word, 0)
    idf = idf_dict.get(word, 0)
    return count, idf

if __name__ == "__main__":

    file1 = r"..\resource\result_retry\count_all.txt"
    file2 = r"..\resource\result_retry\idf_all.txt"

    output_file = r"..\resource\result_retry\hebing.txt"

    count_dict_ = read_file(file1)
    idf_dict = read_file_fromidf(file2)

    hebing_list = []

    for key in count_dict_:
        count,idf = get_info(key)

        temp_wordset = (key, count, idf)

        hebing_list.append(temp_wordset)

    write_to_file(hebing_list,output_file)

