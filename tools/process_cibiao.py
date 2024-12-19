import re
import os
import pandas as pd
from pypinyin import lazy_pinyin
from collections import Counter

enen_filepath = r'W:\python\EWD\resource\result_retry\enen.txt'

one_five_filepath = r'W:\python\EWD\resource\result_retry\1-5.txt'

one_five_commmon_filepath = r'W:\python\EWD\resource\result_retry\one_five_common.txt'

six_nine_filepath = r'W:\python\EWD\resource\result_retry\6-9.txt'

six_nine_commmon_filepath = r'W:\python\EWD\resource\result_retry\six_nine_common.txt'

output_folder = r'W:\python\EWD\resource\result_retry'

common_enen = r'W:\python\EWD\resource\result_retry\通用.txt'

uncommon_enen = r'W:\python\EWD\resource\result_retry\技术.txt'

chubanshu_path = r'W:\python\EWD\resource\出版书\电气工程二校.txt'

def read_words_fromexcel(excel_path):
    # 使用pandas读取Excel文件
    data_frame = pd.read_excel(excel_path, engine='openpyxl', sheet_name=1)  # 确保使用正确的引擎

    column_data = data_frame['词语']

    cleaned_column_data = column_data.dropna()

    column_list = cleaned_column_data.tolist()

    return column_list

def read_words_from_excel(excel_path):
    # 使用pandas读取Excel文件
    # 读取所有需要的工作表
    sheets = [1, 2, 3, 4, 5]  # 指定需要读取的工作表索引
    data_frames = [pd.read_excel(excel_path, engine='openpyxl', sheet_name=sheet) for sheet in sheets]

    # 提取每个工作表中的 '词语' 列，并去除 NaN 值
    column_data = [df['词语'].dropna().tolist() for df in data_frames]

    # 将所有列的数据合并到一个列表中
    combined_list = [word for sublist in column_data for word in sublist]

    return combined_list


def readwordsfromtxt(path):
    words_list = []
    with open(path,'r',encoding='utf-8') as file:
        for line in file:
            line_strip = line.strip().split()
            if(len(line_strip) == 1):
                words_list.append(line_strip[0])
            if(len(line_strip) == 2):
                words_list.append(line_strip[0])
    return words_list




def process_single(input_folder,output_folder):
    all_words_list = []
    for filename in os.listdir(input_folder):
        excel_words_list = []
        if filename.endswith('.txt'):
            txtpath = os.path.join(input_folder, filename)

            txt_words_list = readwordsfromtxt(txtpath)

            print(len(txt_words_list))

            for word in txt_words_list:
                all_words_list.append(word)

    set_words_list = set(all_words_list)

    txtoutput = os.path.join(output_folder, f"6-9.txt")

    with open(txtoutput,'w',encoding='utf-8') as output:
        for word in set_words_list:
            output.write(f'{word}' + '\n')


def process_multi(input_folder,output_folder):
    for filename in os.listdir(input_folder):
        if filename == "七九级词.xlsx":
            excelpath = os.path.join(input_folder,filename)

            excel_words_list = read_words_from_excel(excelpath)

            base, ext = os.path.splitext(filename)

            exceloutput = os.path.join(output_folder, f"{base}.txt")

            with open(exceloutput, 'w', encoding='utf-8') as output:
                for word in excel_words_list:
                    output.write(f'{word}' + '\n')


def process_enen(input_file,output_folder = None):
    one_five_words_set = set(readwordsfromtxt(input_file))
    enen_words_set = set(readwordsfromtxt(enen_filepath))

    print(len(one_five_words_set))
    print(len(enen_words_set))

    common_words = one_five_words_set.intersection(enen_words_set)

    uncommon_words = one_five_words_set.difference(enen_words_set)

    # only_in_enen = enen_words_set.difference(one_five_words_set)

    output_file_common = os.path.join(output_folder,"six_nine_common.txt")

    with open(output_file_common,'w',encoding='utf-8') as output_file:
        for commonword in common_words:
            output_file.write(f"{commonword}" + "\n")

    output_file_uncmmon = os.path.join(output_folder, "six_nine_uncommon.txt")

    with open(output_file_uncmmon,'w',encoding='utf-8') as output_file:
        for uncommonword in uncommon_words:
            output_file.write(f"{uncommonword}" + "\n")

    # output_file_only_in_enen = os.path.join(output_folder,"one_five_only_in_enen.txt")
    #
    # with open(output_file_only_in_enen,'w',encoding='utf-8') as output_file:
    #     for only_in_enen_word in only_in_enen:
    #         output_file.write(f"{only_in_enen_word}" + "\n")


def do_freq():
    freq_10000 = []
    freq_10000_7500 = []
    freq_7500_5000 = []
    freq_5000_2500 = []
    freq_2500 = []
    enen_words_set = set(readwordsfromtxt(enen_filepath))
    for word,freq in enen_words_set:
        if freq > 10000:
            freq_10000.append(word)
        elif 10000 >= freq > 7500:
            freq_10000_7500.append(word)
        elif 7500 >= freq > 5000:
            freq_7500_5000.append(word)
        elif 5000 >= freq > 2500:
            freq_5000_2500.append(word)
        else:
            freq_2500.append(word)

    # print(freq_10000)
    # print(freq_10000_7500)
    # print(freq_7500_5000)
    # print(freq_5000_2500)
    # print(freq_2500)

    print(len(freq_10000))
    print(len(freq_10000_7500))
    print(len(freq_7500_5000))
    print(len(freq_5000_2500))
    print(len(freq_2500))

    output_file_10000 = os.path.join(output_folder, "freq_10000.txt")
    output_file_10000_7500 = os.path.join(output_folder, "freq_10000_7500.txt")
    output_file_7500_5000 = os.path.join(output_folder, "freq_7500_5000.txt")
    output_file_5000_2500 = os.path.join(output_folder, "freq_5000_2500.txt")
    output_file_2500 = os.path.join(output_folder, "freq_2500.txt")

    with open(output_file_10000,'w',encoding='utf-8') as output_file:
        for word in freq_10000:
            output_file.write(f"{word}" + "\n")

    with open(output_file_10000_7500,'w',encoding='utf-8') as output_file:
        for word in freq_10000_7500:
            output_file.write(f"{word}" + "\n")

    with open(output_file_7500_5000,'w',encoding='utf-8') as output_file:
        for word in freq_7500_5000:
            output_file.write(f"{word}" + "\n")

    with open(output_file_5000_2500,'w',encoding='utf-8') as output_file:
        for word in freq_5000_2500:
            output_file.write(f"{word}" + "\n")

    with open(output_file_2500,'w',encoding='utf-8') as output_file:
        for word in freq_2500:
            output_file.write(f"{word}" + "\n")


def findcommon_throughfreq(input_file):
    dengji_words_set = set(readwordsfromtxt(input_file))
    freq10000_set = set(readwordsfromtxt(os.path.join(output_folder, "freq_10000.txt")))
    freq10000_7500_set = set(readwordsfromtxt(os.path.join(output_folder, "freq_10000_7500.txt")))
    freq7500_5000_set = set(readwordsfromtxt(os.path.join(output_folder, "freq_7500_5000.txt")))
    freq5000_2500_set = set(readwordsfromtxt(os.path.join(output_folder, "freq_5000_2500.txt")))
    freq2500_set = set(readwordsfromtxt(os.path.join(output_folder, "freq_2500.txt")))

    common_10000 = dengji_words_set.intersection(freq10000_set)
    common_10000_7500 = dengji_words_set.intersection(freq10000_7500_set)
    common_7500_5000 = dengji_words_set.intersection(freq7500_5000_set)
    common_5000_2500 = dengji_words_set.intersection(freq5000_2500_set)
    common_2500 = dengji_words_set.intersection(freq2500_set)

    print(len(common_10000))
    print(len(common_10000_7500))
    print(len(common_7500_5000))
    print(len(common_5000_2500))
    print(len(common_2500))

def readfile_end(input_filepath):
    words_list = []
    with open(input_filepath, 'r', encoding='utf-8') as file:
        for line in file:
            line_strip = line.strip().split()
            if (len(line_strip) == 2):
                words_list.append(line_strip[1])
    return words_list

def pinyin():
    enen_list = readwordsfromtxt(enen_filepath)
    word_counts = Counter(enen_list)
    print(word_counts)

    print(f"enen_list:{len(enen_list)}")

    common_enen_list = readfile_end(common_enen)

    uncommon_enen_list = readfile_end(uncommon_enen)

    common_enen_set = set(common_enen_list)

    uncommon_enen_set = set(uncommon_enen_list)

    print(len(common_enen_list))
    print(len(common_enen_set))

    print(len(uncommon_enen_list))
    print(len(uncommon_enen_set))

    all_set = set(common_enen_list + uncommon_enen_list)

    common_enen_list = list(common_enen_set)

    uncommon_enen_list = list(uncommon_enen_set)

    all_list = list(all_set)

    print(len(all_set))

    sorted_commonwords = sorted(common_enen_list, key=lambda word: lazy_pinyin(word))

    sorted_uncommonwords = sorted(uncommon_enen_list, key=lambda word: lazy_pinyin(word))

    sorted_all_words = sorted(all_list, key=lambda word: lazy_pinyin(word))

    tongyong_path = os.path.join(output_folder, "通用_拼音.txt")

    with open(tongyong_path, 'w', encoding='utf-8') as output_file:
        for word in sorted_commonwords:
            output_file.write(f"{word}" + "\n")

    jishu_path = os.path.join(output_folder, "技术_拼音.txt")

    with open(jishu_path, 'w', encoding='utf-8') as output_file:
        for word in sorted_uncommonwords:
            output_file.write(f"{word}" + "\n")

    zongshu_path = os.path.join(output_folder, "总词_拼音.txt")

    with open(zongshu_path, 'w', encoding='utf-8') as output_file:
        for word in sorted_all_words:
            output_file.write(f"{word}" + "\n")

    # enen_common_uncommon = common_enen_list + uncommon_enen_list
    #
    # enen_set = set(enen_list)
    #
    # enen_common_uncommon_set = set(enen_common_uncommon)
    #
    # difference__ = enen_common_uncommon_set.difference(enen_set)
    #
    # print(difference__)
    #
    # print(f"enen_list:{len(set(enen_list))}")
    #
    # print(f"enen_common_uncommon_list:{len(set(enen_common_uncommon))}")
    #

    #
    # print(sorted_commonwords)
    #
    # print(sorted_uncommonwords)
    #

    #
    # print(word_counts)
    #


def read_chubanshu():
    chinese_lines = []
    # 定义一个正则表达式模式，用于匹配中文字符
    chinese_pattern = re.compile(r'^[\u4e00-\u9fff]+$')
    # 定义一个正则表达式模式，用于匹配需要剔除的特定短语
    exclude_patterns = re.compile(r'第一课|第二课|第三课|第四课|第五课|第六课')

    with open(chubanshu_path, "r", encoding='utf-8') as file:
        for line in file:
            # 去除行两端的空白字符（包括换行符）
            stripped_line = line.strip()
            # 检查这一行是否全为中文字符并且不包含要剔除的短语
            if chinese_pattern.match(stripped_line) and not exclude_patterns.search(stripped_line):
                chinese_lines.append(stripped_line)

    return chinese_lines


def chubanshu_commmon():

    chuban_set = set(read_chubanshu())

    enen_list = readwordsfromtxt(enen_filepath)

    enen_set = set(enen_list)

    print(len(chuban_set))

    print(len(enen_list))

    common_chuban_enen = enen_set.intersection(chuban_set)

    print(common_chuban_enen)

    print(len(common_chuban_enen))

    chuban_common_path = os.path.join(output_folder, "出版书中的共现词.txt")

    with open(chuban_common_path, 'w', encoding='utf-8') as output_file:
        for word in common_chuban_enen:
            output_file.write(f"{word}" + "\n")


def main():
    chubanshu_commmon()
    # pinyin()
    # findcommon_throughfreq(one_five_commmon_filepath)
    # do_freq()
    # process_enen(one_five_filepath,output_folder)
    # process_enen(six_nine_filepath,output_folder)
    # process_single(input_folder,output_folder)
    # process_multi(input_folder,output_folder)


main()
