# 定义文件路径
file_path = '../resource/dict/电力dict.txt'  # 请将 'your_file.txt' 替换为你的实际文件路径

# 读取文件内容
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 确定要保留的行数
lines_to_keep = 46583

# 如果文件行数少于或等于46583行，则直接退出
if len(lines) <= lines_to_keep:
    print("文件行数少于或等于46583行，无需删除任何内容。")
else:
    # 截取前46583行
    lines = lines[:lines_to_keep]

    # 将截取后的内容写回文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

    print(f"已删除第46583行之后的所有内容。")