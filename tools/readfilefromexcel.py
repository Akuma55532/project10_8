import os
import re
import pandas as pd


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
    return set(words_return)

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

def main(input_folder,output_file = None):
    if not os.path.exists(input_folder):
        print("路径不存在，请检查路径")
        return -1

    filter_set = read_words(filter_path)

    uncommon_words = {}

    common = []

    for filename in os.listdir(input_folder):
        if filename.endswith('.xlsx'):
            excelpath = os.path.join(input_folder,filename)
            excel_set = set(read_words_fromexcel(excelpath))
            common_words = filter_set.intersection(excel_set)

            for word in common_words:
                common.append(word)

    uncommon = filter_set.difference(set(common))

            #
            #
            # fenzi = len(common_words)
            #
            # fenmu = len(excel_set)
            #
            # dengji_dict[filename] = fenzi / fenmu
            #
            # base_name, ext = os.path.splitext(filename)
            #
            # print(f"uncommon:{len(common_words)}")
            #
            # print(f"uncommon:{len(uncommon_words)}")
            #
            # print(f"uncommon:{len(excel_set)}")
            #
            # print(f"uncommon:{len(filter_set)}")
            # break
            #
            # dengji_path_common_words = os.path.join(input_folder,f'{base_name}.txt')

    # filter_set = filter_set2.intersection(filter_set)

    common_words_all = os.path.join(input_folder,'common.txt')

    uncommon_words_all = os.path.join(input_folder, 'uncommon.txt')

    with open(common_words_all,'w',encoding='utf-8') as outputfile:
        for word in common:
            outputfile.write(f'{word}\n')

    with open(uncommon_words_all,'w',encoding='utf-8') as outputfile:
        for word in uncommon:
            outputfile.write(f'{word}\n')





excel_path = r'../resource/七九级词.xlsx'
filter_path = r'../resource/result_retry/enen.txt'
input_folder = '../resource/词语等级'

output_file = r'../resource/词语等级/等级.txt'

output_file2 = r'../resource/词语等级/dengji.txt'
if __name__ == '__main__':
    main(input_folder)
    # words = []
    # set1 = set(read_words_from_excel(excel_path))
    # with open(output_file2, 'r', encoding='utf-8') as file:
    #     for line in file:
    #         word = line.strip()  # 去除每行末尾的换行符
    #         words.append(word)
    #
    # set2 = set(words)
    #
    # set2 = set2.difference(set1)
    #
    # dengji_path_common_words_all = os.path.join(input_folder, 'dengji.txt')
    #
    # with open(dengji_path_common_words_all, 'w', encoding='utf-8') as outputfile:
    #     for word in set2:
    #         outputfile.write(f'{word}\n')


