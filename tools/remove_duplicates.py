import os
import re

def remove_duplicates(input_file, output_file):

    # 使用集合存储每行的内容，自动过滤掉重复的行
    lines_seen = set()

    filename = os.path.basename(input_file)

    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            # 去除行尾的换行符
            line = line.strip()
            if line not in lines_seen:
                lines_seen.add(line)

    # 将无重复的行写入新文件
    with open(output_file, 'w', encoding='utf-8') as file:
        for line in lines_seen:
            file.write(line + '\n')

# 指定输入和输出文件路径
input_file_path = 'path/to/your/input.txt'
output_file_path = 'path/to/your/output.txt'
# 调用函数
remove_duplicates(input_file_path, output_file_path)