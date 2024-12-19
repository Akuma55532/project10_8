def read_word_counts(filename):
    """读取文件，返回词语和计数的字典"""
    word_counts = {}
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 2:
                word, count = parts[0], int(parts[1])
                word_counts[word] = count
    return word_counts


def calculate_percentages(word_counts):
    """计算每个词语计数的百分比"""
    total_count = sum(word_counts.values())
    percentages = {word: (count / total_count) * 100 for word, count in word_counts.items()}
    return percentages


def write_percentages_to_file(percentages, output_filename):
    """将百分比结果写入新文件"""
    with open(output_filename, 'w', encoding='utf-8') as file:
        for word, percentage in percentages.items():
            file.write(f"{word} {percentage:.2f}%\n")


def main():
    input_filename = r'../resource/ful2/count_hexin.txt'
    output_filename = r'../resource/ful/rate_hexin.txt'

    # 读取词语计数
    word_counts = read_word_counts(input_filename)

    # 计算百分比
    percentages = calculate_percentages(word_counts)

    # 写入新的文件
    write_percentages_to_file(percentages, output_filename)

    print(f"百分比已计算完成，并保存到{output_filename}")


if __name__ == "__main__":
    main()