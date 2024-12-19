import os
from collections import defaultdict


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
                        try:
                            freq = int(freq_str)
                            word_freq[word] += freq
                        except ValueError:
                            print(f"Warning: Invalid frequency '{freq_str}' for word '{word}' in file {filename}")

    # 将结果写入输出文件
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for word, freq in sorted(word_freq.items(), key=lambda item: item[1], reverse=True):
            outfile.write(f"{word} {freq}\n")

def main(input_folder_overall,output_folder):
    for filename in os.listdir(input_folder_overall):
        if filename != 'result':
            folder_path = os.path.join(input_folder_overall,filename)
            output_file = os.path.join(output_folder,f"{filename}.txt")

            aggregate_word_frequencies(folder_path,output_file)





# 指定文件夹路径和输出文件名
folder_path = r'..\resource\resource_test\count'  # 替换为你的文件夹路径
output_folder = r'..\resource\resource_test\count\result'
# 调用函数
main(folder_path,output_folder)

print("聚合完成，结果已保存至")