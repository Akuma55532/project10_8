#不要在pycharm终端执行，在windows

import os
import re


def process_png_folders(input_root, output_root):
    """处理指定文件夹中的所有包含PNG文件的子文件夹"""
    if not os.path.exists(input_root):
        print(f"错误：路径 {input_root} 不存在")
        return

    if not os.path.exists(output_root):
        os.makedirs(output_root)

    allowed_punctuation = r'[:，。()？！；]'

    for file_name in os.listdir(input_root):
        file_path = os.path.join(input_root, file_name)

        print(f'正在处理: {file_name}')

        output_file = os.path.join(output_root, f"re{file_name}")

        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        filtered_content = re.sub(r'[a-zA-Z0-9\{\}\[\]\#\$\%\^\&\*\(\)\\\,\.\+\-\_\=\'\:\;\"\°\/\<\>\≥\≤\：\（\）\“\”\】\【\／\、\、\?\~\—\@\·\［\～\］\；]', '', content)

        filtered_content = re.sub(r'\s+', ' ', filtered_content)

        filtered_content = re.sub(r'\n\s*\n', '\n\n', filtered_content).strip()

        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(filtered_content)


# 指定要操作的文件夹路径
input_root = r"W:\python\EWD\resource\emm"  # 替换为你的输入文件夹路径
output_root = r"W:\python\EWD\resource\emm"  # 替换为你的输出文件夹路径

# 调用函数
process_png_folders(input_root, output_root)

print("全部完成！！！")