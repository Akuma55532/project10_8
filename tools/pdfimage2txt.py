import os
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import re

def pdf_to_images(pdf_path):
    """将PDF文件转换为图像列表"""
    images = []
    pdf_document = fitz.open(pdf_path)
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)
    print("一本的images转化完成")
    return images


def image_to_text(image):
    """使用Tesseract OCR将图像转换为文本，并去除多余的换行符"""
    text = pytesseract.image_to_string(image, lang='chi_sim').replace(' ', '')
    # 去除多余的换行符
    text = re.sub(r'\n+', '\n', text).strip()
    return text


def process_pdfs_in_folder(folder_path, output_folder_path):
    """处理指定文件夹中的所有PDF文件，并将提取的文本保存为TXT文件"""
    if not os.path.exists(folder_path):
        print(f"错误：路径 {folder_path} 不存在")
        return

    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            file_path = os.path.join(folder_path, filename)
            print(f'正在处理: {filename}')

            # 将PDF文件转换为图像列表
            images = pdf_to_images(file_path)
            all_text = ""

            # num = 0

            # 对每个图像进行OCR处理
            for image in images:
                text = image_to_text(image)
                print("transform_text_once")
                all_text += text + "\n"
                # num += 1
                # if num == 10:
                #     break


            # 构建输出文件路径
            output_file = os.path.join(output_folder_path, f"{os.path.splitext(filename)[0]}.txt")

            # 将提取的文本写入输出文件
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(all_text)

        break




# 指定要操作的文件夹路径
folder_path = r"..\resource\resource_raw\image1.pdf"  # 替换为你的PDF文件所在的路径
output_folder_path = r"..\resource\resource_test\temp"  # 替换为你的输出文件夹路径

# 调用函数
process_pdfs_in_folder(folder_path, output_folder_path)

print("all done!!!!!It's so tired")