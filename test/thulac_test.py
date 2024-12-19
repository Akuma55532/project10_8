import thulac
from docx import Document
import re
from sklearn.metrics import precision_score,recall_score,f1_score

original_text_filepath = r'../resource/resource_test/text/原文本.docx'

vaild_text_filepath = r'../resource/resource_test/text/验证文本.docx'

def read_word_file(file_path):
    # 打开Word文档
    doc = Document(file_path)

    # 初始化一个空列表来存储每一段的文本
    paragraphs_text = []

    # 遍历文档中的每一个段落
    for paragraph in doc.paragraphs:
        paragraphs_text.append(paragraph.text)

    # 返回所有段落的文本
    return paragraphs_text

def filter(words):
    new_words = []
    for word in words:
        temp = []
        # 使用正则表达式匹配汉字
        pattern = re.compile(r'^[\u4e00-\u9fff]+$')
        for token in word:
            if pattern.match(token):
                temp.append(token)
        new_words.append(temp)
    return new_words

original_text = read_word_file(original_text_filepath)

thu1 = thulac.thulac(seg_only=True)  #只进行分词，不进行词性标注

fenci_thulac = []



for sentence in original_text:

    seg_list = thu1.cut(sentence, text=True)

    temp = seg_list.split()

    fenci_thulac.append(temp)  # 精确模式)

words = filter(fenci_thulac)

print(words)

def reprocess(vaild_text):
    new_text = []
    for paragraph in vaild_text:
        temp = paragraph.split()
        new_text.append(temp)

    return new_text



vaild_text = read_word_file(vaild_text_filepath)

vaild_words = reprocess(vaild_text)


pre_list = []

recall_list = []

f1_list = []

# 将分词结果转换为字符级别的标签
def convert_to_bioes(text, words):
    bioes_labels = []
    index = 0
    for word in words:
        if len(word) == 1:
            bioes_labels.append('S')
        elif len(word) > 1:
            bioes_labels.append('B')
            for _ in range(1, len(word) - 1):
                bioes_labels.append('M')
            bioes_labels.append('E')
        index += len(word)
    return bioes_labels

for i in range(len(words)):

    true_labels = convert_to_bioes(vaild_text[i], vaild_words[i])
    pred_labels = convert_to_bioes(vaild_text[i], words[i])

    if len(true_labels) != len(pred_labels):
        continue

    print(i)

    precision = precision_score(true_labels, pred_labels,average='weighted')

    pre_list.append(precision)

    recall = recall_score(true_labels, pred_labels,average='weighted')

    recall_list.append(recall)

    f1 = f1_score(true_labels, pred_labels,average='weighted')

    f1_list.append(f1)

precision_avg = sum(pre_list) / len(pre_list)
recall_avg = sum(recall_list) / len(recall_list)
f1_avg = sum(f1_list) / len(f1_list)

print(f"precision:{precision_avg}")
print(f'recall:{recall_avg}')
print(f'f1_score:{f1_avg}')

output_filepath = r'../resource/resource_test/text/fenci_thulac.txt'

with open(output_filepath,'w',encoding='utf-8') as file:
    for word in words:
        file.write(f'{word}' + '\n----------------------------------\n')