import os
import time


input_file = r"..\resource\result_retry\hebing.txt"
output_file = r"..\resource\result_retry\filter.txt"

def read_file(input_file):
    all_words_list = []

    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            line_split = line.strip().split()  # 去除行末的换行符并分割
            if len(line_split) == 3:
                word, count, idf = line_split[0], int(line_split[1]), float(line_split[2])
                if count > 100 and idf < 2:
                    temp_wordset = (word, count, idf)
                    all_words_list.append(temp_wordset)

    return all_words_list

def main(input_file,output_file):

    if not os.path.exists(input_file):
        print("路径不存在，请检查路径")
        return -1

    all_words = read_file(input_file)

    with open(output_file, 'w', encoding='utf-8') as file:
        for word, count, idf in all_words:
            file.write(f"{word} {count} {idf}\n")


main(input_file,output_file)
