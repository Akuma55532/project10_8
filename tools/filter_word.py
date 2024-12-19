from collections import Counter
import os
import re

def process_segmentation_results(input_root,output_root):
    if not os.path.exists(input_root):
        print(f"错误：路径 {input_root} 不存在")
        return

    if not os.path.exists(output_root):
        os.makedirs(output_root)

    for filename in os.listdir(input_root):
        if filename.endswith('.txt'):
            file_path = os.path.join(input_root, filename)
            # 读取分词结果文件
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            # 初始化一个字典，用于存储词及其频率
            word_freq_dict = {}

            # 处理每一行
            for line in lines:
                # 去除行尾的换行符
                line = line.strip()

                # 替换中文空格为英文空格
                line = line.replace('\u3000', ' ')

                # 替换制表符为英文空格
                line = line.replace('\t', ' ')

                # 去除多余的空格
                line = re.sub(r'\s+', ' ', line)

                # 检查是否有两个部分（词和词频）
                parts = line.split(' ')
                if len(parts) == 2:
                    word, freq_str = parts
                    try:
                        freq = int(freq_str)
                        # 过滤掉含有空格的词
                        if ' ' not in word:
                            if word in word_freq_dict:
                                word_freq_dict[word] += freq
                            else:
                                word_freq_dict[word] = freq
                    except ValueError:
                        # 如果词频不是整数，跳过这一行
                        continue

            # 按词频大小进行递减排序
            sorted_word_counts = sorted(word_freq_dict.items(), key=lambda x: x[1], reverse=True)

            output_file_path = os.path.join(output_root,filename)

            # 保存结果到文件
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                for word, count in sorted_word_counts:
                    output_file.write(f"{word} {count}\n")

input_file = r'..\resource\result_retry'
output_file = r'..\resource\result_retry'


# 调用函数处理分词结果
process_segmentation_results(input_file,output_file)
