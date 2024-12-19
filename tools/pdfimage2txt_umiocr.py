#不要在pycharm终端执行，在windows

import os
import re
import subprocess

def extract_number_from_filename(filename):
    """从文件名中提取数字"""
    match = re.search(r'(\d+)', filename)

    return match.group(1)


def run_umi_ocr(input_path, output_path):
    """运行 umi-ocr 命令并将结果保存到指定的输出文件"""

    filename_list = [0]*300

    for file_name in os.listdir(input_path):
        number = int(extract_number_from_filename(file_name))
    
        filename_list[number] = file_name

    for i in filename_list:
        if i != 0:
            file_path = os.path.join(input_path,i)

            base_name, ext = os.path.splitext(i)

            output = os.path.join(output_path,f'{base_name}.txt')

            with open(output, 'w') as file:
                pass  # 不写入任何内容

            command = f'umi-ocr --path "{file_path}" --output "{output}"'

            print(f"正在运行: {command}")

            subprocess.run(command, shell=True)

            

def process_png_folders(input_root, output_root):
    """处理指定文件夹中的所有包含PNG文件的子文件夹"""
    if not os.path.exists(input_root):
        print(f"错误：路径 {input_root} 不存在")
        return

    if not os.path.exists(output_root):
        os.makedirs(output_root)

    for folder_name in os.listdir(input_root):
        folder_path = os.path.join(input_root, folder_name)
        if os.path.isdir(folder_path):

            print(f'正在处理: {folder_name}')

            run_umi_ocr(folder_path, output_root)


# 指定要操作的文件夹路径
input_root = r"W:\python\EWD\resource\等级标准"   # 替换为你的输入文件夹路径
output_root = r"W:\python\EWD\resource\dengji\result"  # 替换为你的输出文件夹路径

# 调用函数
process_png_folders(input_root, output_root)

print("全部完成！！！")