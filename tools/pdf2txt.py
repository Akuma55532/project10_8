import os
import fitz  # PyMuPDF


def open_pdfs_in_folder(folder_path, output_folder_path):
    # 检查给定的路径是否存在
    if not os.path.exists(folder_path):
        print(f"错误：路径 {folder_path} 不存在")
        return

    # 确保输出文件夹存在
    os.makedirs(output_folder_path, exist_ok=True)

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        # 检查文件是否为PDF格式
        if filename.endswith('.pdf'):
            file_path = os.path.join(folder_path, filename)
            print(f'正在处理: {filename}')

            # 打开PDF文档
            doc = fitz.open(file_path)
            file_string = ""

            # 定义开始页码 (PyMuPDF索引从0开始)
            start_page_number = 440  # 如果你想从441页开始，则索引应为440

            # 获取文档总页数
            total_pages = len(doc)

            # 遍历文档的每一页，从start_page_number开始
            for page_num in range(start_page_number, total_pages):
                page = doc.load_page(page_num)  # 加载页面
                text = page.get_text("text")  # 获取纯文本格式的文本
                file_string += text + "\n"  # 将每页的文本添加到file_string中，并加上换行符

            # 创建输出文件名
            output_filename = os.path.join(output_folder_path,
                                           f"{os.path.splitext(filename)[0]}_extracted_from_page_441.txt")

            # 将提取的文本写入输出文件
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(file_string)

            doc.close()  # 关闭文档


# 指定要操作的文件夹路径
folder_path = r"..\resource\出版书"  # 替换为你的PDF文件所在的路径
output_folder_path = r"..\resource\出版书\电气工程二校.txt"  # 替换为你的输出文件夹路径

# 调用函数
open_pdfs_in_folder(folder_path, output_folder_path)