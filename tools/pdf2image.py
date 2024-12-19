import os
import fitz  # PyMuPDF
from PIL import Image
import re


def sanitize_filename(filename):
    """将文件名中的特殊字符替换为下划线"""
    return re.sub(r'[\\/*?:"<>|]', "_", filename)


def pdf_to_images(pdf_path, output_folder):
    """将PDF文件转换为图像列表，并保存为PNG文件"""
    pdf_document = fitz.open(pdf_path)
    base_filename = os.path.splitext(os.path.basename(pdf_path))[0]
    sanitized_base_filename = sanitize_filename(base_filename)
    page_output_folder = os.path.join(output_folder, sanitized_base_filename)

    if not os.path.exists(page_output_folder):
        os.makedirs(page_output_folder)

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img.save(os.path.join(page_output_folder, f'{sanitized_base_filename}_page_{page_num + 1}.png'), 'PNG')
    print(f"转换完成: {sanitized_base_filename}")
    return page_output_folder


def process_pdfs_in_folder(folder_path, output_folder_path):
    """处理指定文件夹中的所有PDF文件，并将每页保存为PNG文件"""
    if not os.path.exists(folder_path):
        print(f"错误：路径 {folder_path} 不存在")
        return

    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            file_path = os.path.join(folder_path, filename)
            print(f'正在处理: {filename}')
            pdf_to_images(file_path, output_folder_path)
    print("所有PDF文件转换完成！")


# 指定要操作的文件夹路径
folder_path = r"..\resource\出版书"  # 替换为你的PDF文件所在的路径
output_folder_path = r"..\resource\出版书"  # 替换为你的输出文件夹路径

# 调用函数
process_pdfs_in_folder(folder_path, output_folder_path)

print("全部完成！！！")