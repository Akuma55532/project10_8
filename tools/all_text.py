import os
import re

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


read_file(r'W:\python\EWD\resource\resource_temp2')

